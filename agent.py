"""Demo agent used to prove the Agent Box filesystem boundary."""

from pathlib import Path


def read_file(label: str, path: str) -> None:
    try:
        content = Path(path).read_text(encoding="utf-8").strip()
    except OSError as error:
        print(f"BLOCKED {label}: {path} ({error})")
        return
    print(f"ALLOWED {label}: {path}")
    print(content)


print("Agent started")
read_file("workspace input", "workspace/input.txt")
read_file("protected secret", "program_files/secret.txt")
