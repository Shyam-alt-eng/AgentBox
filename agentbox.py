"""Agent Box MVP command-line security runtime.

The Docker container is the enforcement boundary. Only the agent source and
the explicitly selected workspace are mounted into the container.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_POLICY = {
    "filesystem": {
        "read": ["/workspace"],
        "write": ["/workspace/output"],
    },
    "network": {"enabled": False},
    "shell": {"enabled": False},
    "environment": {"allowed": ["APP_MODE"]},
}

LOG_FILE = Path(".agentbox/events.jsonl")
CONTAINER_NAME = "agentbox-runner"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log_event(operation: str, resource: str, decision: str, reason: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": now(),
        "operation": operation,
        "resource": resource,
        "decision": decision,
        "reason": reason,
    }
    with LOG_FILE.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event) + "\n")


def parse_policy(path: Path) -> dict:
    """Parse the small policy shape used by the MVP without extra packages."""
    if not path.exists():
        return DEFAULT_POLICY

    policy = json.loads(json.dumps(DEFAULT_POLICY))
    section = None
    key = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        text = line.strip()
        if indent == 0 and text.endswith(":"):
            section = text[:-1]
            key = None
        elif indent == 2 and text.endswith(":"):
            key = text[:-1]
            policy.setdefault(section, {})[key] = []
        elif indent == 4 and text.startswith("-") and section and key:
            value = text[1:].strip().strip("'\"")
            policy[section][key].append(value)
        elif indent == 2 and ":" in text and section:
            name, value = (part.strip() for part in text.split(":", 1))
            policy.setdefault(section, {})[name] = value.lower() == "true"
    return policy


def scan_agent(agent: Path) -> int:
    patterns = {
        "Filesystem access": r"open\s*\(|pathlib|os\.path|shutil",
        "Shell execution": r"subprocess|os\.system|os\.popen|shell\s*=\s*True",
        "Network access": r"requests|urllib|httpx|socket|aiohttp",
        "Environment variables": r"os\.environ|getenv\s*\(",
    }
    files = [agent] if agent.is_file() else list(agent.rglob("*.py"))
    source = "\n".join(file.read_text(encoding="utf-8", errors="ignore") for file in files)
    findings = [name for name, pattern in patterns.items() if re.search(pattern, source)]
    print("Agent Box Security Scan\n-----------------------")
    print(f"Agent: {agent}")
    for name in patterns:
        print(f"{name:<24}: {'DETECTED' if name in findings else 'not detected'}")
    risk = "HIGH" if len(findings) >= 3 else "MEDIUM" if findings else "LOW"
    print(f"\nRisk Level: {risk}")
    return 0


def print_policy(policy: dict) -> None:
    print(json.dumps(policy, indent=2))


def run_agent(agent: Path, workspace: Path, policy_path: Path) -> int:
    docker = shutil.which("docker")
    if not docker:
        print("Agent Box requires Docker for runtime enforcement.", file=sys.stderr)
        return 1
    if not agent.exists():
        print(f"Agent not found: {agent}", file=sys.stderr)
        return 1

    workspace = workspace.resolve()
    agent = agent.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    image = os.environ.get("AGENTBOX_IMAGE", "python:3.12-slim")
    command = [
        docker,
        "run",
        "--rm",
        "--name",
        CONTAINER_NAME,
        "--network", "none",
        "--read-only",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges:true",
        "--pids-limit", "128",
        "-e", "PYTHONDONTWRITEBYTECODE=1",
        "-v", f"{agent}:/agent/{agent.name}:ro",
        "-v", f"{workspace}:/workspace:rw",
        "-w", "/",
        image,
        "python",
        f"/agent/{agent.name}",
    ]

    policy = parse_policy(policy_path)
    log_event("START", str(agent), "ALLOWED", "Agent started in restricted Docker runtime")
    print(f"[Agent Box] Running {agent} in restricted container")
    print(f"[Agent Box] Allowed read paths: {', '.join(policy['filesystem']['read'])}")
    print("[Agent Box] Network: disabled")
    try:
        result = subprocess.run(command, check=False)
    except KeyboardInterrupt:
        log_event("STOP", str(agent), "ALLOWED", "Agent interrupted by operator")
        return 130
    decision = "ALLOWED" if result.returncode == 0 else "BLOCKED"
    log_event("STOP", str(agent), decision, f"Container exited with code {result.returncode}")
    return result.returncode


def stop_agent() -> int:
    docker = shutil.which("docker")
    if not docker:
        print("Docker is not installed or not on PATH.", file=sys.stderr)
        return 1
    result = subprocess.run([docker, "stop", CONTAINER_NAME], check=False)
    if result.returncode == 0:
        log_event("STOP", CONTAINER_NAME, "ALLOWED", "Agent terminated by kill switch")
        print("Agent terminated successfully.")
    else:
        print("No running Agent Box container found.")
    return result.returncode


def show_logs() -> int:
    if not LOG_FILE.exists():
        print("No Agent Box events recorded.")
        return 0
    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        print(f"{event['timestamp']} {event['operation']:<5} {event['resource']} {event['decision']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agentbox", description="Run AI agents inside a restricted runtime.")
    commands = parser.add_subparsers(dest="command", required=True)

    scan = commands.add_parser("scan", help="Scan agent source for risky capabilities")
    scan.add_argument("agent", type=Path)

    run = commands.add_parser("run", help="Run an agent in Docker with restricted mounts")
    run.add_argument("agent", type=Path)
    run.add_argument("--workspace", type=Path, default=Path("workspace"))
    run.add_argument("--policy", type=Path, default=Path("policy.yaml"))

    policy = commands.add_parser("policy", help="Display the active policy")
    policy.add_argument("path", type=Path, nargs="?", default=Path("policy.yaml"))
    commands.add_parser("logs", help="Display runtime security events")
    commands.add_parser("stop", help="Stop the running agent")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "scan":
        return scan_agent(args.agent)
    if args.command == "run":
        return run_agent(args.agent, args.workspace, args.policy)
    if args.command == "policy":
        print_policy(parse_policy(args.path))
        return 0
    if args.command == "logs":
        return show_logs()
    if args.command == "stop":
        return stop_agent()
    return 1


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    raise SystemExit(main())