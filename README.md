# AgentBox

## Generative AI Agent Security & Governance

AgentBox is a **policy-enforced execution layer for Generative AI agents**.

It sits between an AI agent and the real world, controlling what the agent is allowed to do through **policy enforcement, sandbox isolation, monitoring, and lifecycle management**.

> **The AI agent decides what it wants to do. AgentBox decides whether it is actually allowed to do it.**

---

# 1. Why Is AgentBox a Generative AI Project?

A common question about AgentBox is:

> **"AgentBox is a security system, so how is it related to Generative AI?"**

AgentBox is **not itself an LLM** such as GPT, Llama, or Gemini.

Instead, AgentBox is designed to secure **Generative-AI-powered agents**.

A traditional Generative AI application may work like this:

```text
User
  ↓
Generative AI Model
  ↓
Generated Response
```

An AI agent goes one step further:

```text
User
  ↓
Generative AI Model
  ↓
AI Agent
  ↓
Generated decision/action
  ↓
Tool / File / Code / API / Web
```

The Generative AI model provides the reasoning and decision-making used by the agent. The agent can then generate requests to perform actions such as:

- Reading files
- Writing files
- Executing code
- Calling APIs
- Accessing websites
- Processing data

This creates a new security problem:

> **What happens when a Generative AI agent is allowed to take actions in the real world?**

AgentBox addresses that problem.

```text
              GENERATIVE AI
                    ↓
                AI AGENT
                    ↓
             Generated Action
                    ↓
             ┌──────────────┐
             │   AGENTBOX   │
             │              │
             │ Policy       │
             │ Sandbox      │
             │ Monitoring   │
             │ Lifecycle    │
             └──────┬───────┘
                    ↓
             Allowed Execution
```

Therefore, the project's domain can be described as:

**Generative AI + Cybersecurity**

More specifically:

**Generative AI → Agentic AI → AI Agent Security & Governance**

---

# 2. The Problem

Modern Generative AI agents can reason, browse, write files, and execute code.

Giving an agent unrestricted access to a terminal or external resources creates security risks.

For example, an agent may be instructed to analyze a project but attempt to:

```bash
rm -rf /
```

or access a sensitive file:

```text
.env
```

or send information to an unauthorized external server:

```text
https://evil-hacker.com
```

A system prompt such as:

```text
"Do not delete files."
"Do not leak confidential information."
```

is only an instruction to the model.

AgentBox instead provides **code-level enforcement**.

The basic principle is:

```text
Prompt-level trust:
"Please don't."

Code-level policy:
"The system will not."
```

Unsafe actions are rejected before they are executed.

---

# 3. What Is AgentBox?

AgentBox is a **security and policy layer between an AI agent and the real world**.

Its three core ideas are:

```text
┌─────────────────────────────┐
│          AGENTBOX           │
│                             │
│  1. POLICY                  │
│     What is allowed?        │
│                             │
│  2. SANDBOX                │
│     Where does it execute? │
│                             │
│  3. MONITORING             │
│     What did it do?        │
└─────────────────────────────┘
```

The goal is to make Generative AI agent actions:

- **Safe**
- **Observable**
- **Enforceable**
- **Isolated**

---

# 4. Simple Example

Imagine a company builds an AI coding agent called **Agent Pro**.

The agent is allowed to:

```text
✓ Read project files
✓ Modify project files
✓ Run tests
✓ Access GitHub
```

But it is not allowed to:

```text
✗ Delete the root filesystem
✗ Read files outside its workspace
✗ Access unauthorized domains
✗ Run unrestricted commands
```

The company defines these boundaries.

AgentBox enforces them.

### Legitimate action

The agent requests:

```text
read_file("/workspace/project/data.csv")
```

AgentBox checks the policy:

```text
Is the path allowed?
        ↓
       YES
        ↓
      PASS
        ↓
Execute in sandbox
```

### Dangerous command

The agent requests:

```bash
rm -rf /
```

AgentBox checks:

```text
Is the command allowed?
        ↓
       NO
        ↓
      BLOCK
```

### Unauthorized network request

The agent requests:

```text
POST .env → evil-hacker.com
```

AgentBox checks:

```text
Is the destination domain allowed?
        ↓
       NO
        ↓
      BLOCK
```

The blocked action can also be shown on the monitoring dashboard.

---

# 5. Who Uses AgentBox?

## Developers / AI Engineers

Developers build AI agents that need access to tools.

Their problem:

> "I want my agent to be capable, but I don't want to build every security control from scratch."

AgentBox provides reusable policy enforcement, sandboxing, safe tools, and monitoring.

---

## Security Teams / CISOs

Security teams need to control what AI agents can access and execute.

They can use AgentBox for:

- Command restrictions
- File/path restrictions
- Network/domain restrictions
- Resource controls
- Monitoring
- Audit information

The important distinction is that these restrictions are enforced by code rather than relying only on prompts.

---

## Enterprise Leadership

Organizations deploying AI agents need a controlled execution boundary.

AgentBox provides a reusable layer for controlling agent actions before they reach protected systems or external resources.

---

# 6. Who Defines the Policy?

AgentBox does **not** decide the business purpose of every agent.

The organization building or deploying the agent defines its requirements.

For example:

```text
Company / Developer
        ↓
Defines Agent Policy
        ↓
policy.json
        ↓
AgentBox
        ↓
Enforces Policy
```

Different agents can have different policies.

### Coding Agent

```json
{
  "allowed_paths": ["/workspace/project"],
  "blocked_commands": ["rm -rf", "chmod"],
  "allowed_domains": ["github.com"]
}
```

### Data Analysis Agent

It may have different allowed paths, domains, commands, and resource limits.

The principle is:

> **The organization defines the boundary. AgentBox enforces the boundary.**

---

# 7. Core Architecture

The AgentBox architecture consists of several components.

```text
                         AI AGENT
                    LangChain / CrewAI
                            │
                            ▼
                     ┌──────────────┐
                     │  SAFE TOOLS  │
                     │              │
                     │ safe_execute │
                     │ safe_read... │
                     │ safe_web...  │
                     └──────┬───────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ FASTAPI POLICY   │
                   │     ENGINE       │
                   │                  │
                   │   PolicyGuard    │
                   └────────┬─────────┘
                            │
                    ┌───────┴────────┐
                    │                │
                  ALLOW              DENY
                    │                │
                    ▼                ▼
             E2B Sandbox        Block Action
                    │                │
                    ▼                ▼
              Execution        Monitoring
                    │
                    ▼
             Streamlit Dashboard
```

---

# 8. Technology Stack

## Agent Logic

**LangChain / CrewAI**

Used to build the agent layer and route tasks through approved tools.

## Policy Engine

**FastAPI**

Responsible for policy validation before execution.

It can validate:

- Commands
- Paths
- Domains
- Timeouts
- Resource limits

## Sandbox

**E2B**

Provides an isolated Linux execution environment.

## Monitoring

**WebSockets + Streamlit**

Used to expose:

- Agent decisions
- Blocked actions
- Resource state
- Alerts
- Execution information

---

# 9. Policy Configuration

AgentBox uses a policy configuration to define boundaries.

Example:

```json
{
  "allowed_paths": [
    "/home/user/allowed"
  ],
  "blocked_commands": [
    "rm -rf",
    "chmod",
    "wget",
    "curl"
  ],
  "allowed_domains": [
    "api.github.com",
    "google.com"
  ],
  "timeout_seconds": 60,
  "max_ram_mb": 512
}
```

The exact values can be changed according to the requirements of the agent.

The important idea is that the policy is **explicit and enforceable**.

---

# 10. Safe Tool Interfaces

The agent should not receive an unrestricted raw terminal.

Instead, AgentBox provides controlled interfaces such as:

```text
safe_execute()
safe_read_file()
safe_web_request()
```

### safe_execute()

Checks commands before execution.

```text
Agent
 ↓
safe_execute(command)
 ↓
PolicyGuard
 ↓
Allowed?
 ├── YES → E2B
 └── NO  → BLOCK
```

### safe_read_file()

Checks whether the requested path is inside the allowed directory.

```text
Agent
 ↓
safe_read_file(path)
 ↓
Path validation
 ↓
Allowed?
 ├── YES → Read
 └── NO  → BLOCK
```

### safe_web_request()

Checks the destination hostname/domain against the allowed-domain policy.

```text
Agent
 ↓
safe_web_request(url)
 ↓
Domain validation
 ↓
Allowed?
 ├── YES → Request
 └── NO  → BLOCK
```

---

# 11. How a Data Leak Is Prevented

Consider this scenario:

```text
Agent task:
"Analyze company data and prepare a report."
```

The agent is working normally.

Then it attempts:

```text
Read .env
      ↓
Send .env to external server
```

AgentBox handles this as follows:

```text
1. Agent generates the action
             ↓
2. Safe tool receives request
             ↓
3. PolicyGuard checks destination
             ↓
4. Domain is not in allowlist
             ↓
5. Request is DENIED
             ↓
6. Event is recorded
             ↓
7. Dashboard displays the blocked action
```

The important point is:

> **The agent may generate the request, but the request does not automatically become an executed action.**

---

# 12. AgentBox Lifecycle

AgentBox is not intended to blindly terminate every agent after one fixed amount of time.

Different tasks have different workloads.

A coding agent processing hundreds of files may legitimately need a long execution period.

The proposed lifecycle therefore uses:

- Dynamic initial leases
- Inactivity monitoring
- Heartbeats
- Checkpoints
- Lease renewal
- Automatic cleanup

```text
Company builds Agent
        ↓
Company defines policy
        ↓
Application sends policy + task
        ↓
FastAPI initializes AgentBox
        ↓
E2B creates isolated sandbox
        ↓
Agent starts working
        ↓
Every action is validated
        ↓
Is the agent actively progressing?
        │
        ├── YES
        │    ↓
        │  Continue
        │    ↓
        │  Heartbeat / checkpoint
        │    ↓
        │  Renew lease
        │
        └── NO
             ↓
        Inactivity timer
             ↓
        Still inactive?
             ↓
        Terminate sandbox
             ↓
        Log final state
```

When the legitimate task completes:

```text
Task completed
      ↓
Export required result
      ↓
Terminate sandbox
      ↓
Log final execution state
```

---

# 13. Monitoring

AgentBox makes the security boundary visible.

The dashboard can show:

```text
LIVE COMMAND STREAM
SANDBOX CPU / RAM
TIMEOUT / LEASE STATUS
BLOCKED ACTIONS
ALERTS
RESOURCE STATE
```

For example:

```text
┌─────────────────────────────────────┐
│           AGENTBOX MONITOR          │
├─────────────────────────────────────┤
│                                     │
│ ✓ read_file()              ALLOWED │
│ ✓ execute("pytest")        ALLOWED │
│ ✗ rm -rf /                 BLOCKED │
│ ✗ evil-hacker.com          BLOCKED │
│                                     │
│ CPU: 18%                            │
│ RAM: 214 MB                         │
│                                     │
└─────────────────────────────────────┘
```

The purpose is not just to block actions.

It is to make the security boundary **observable**.

---

# 14. Demonstration Scenarios

AgentBox can be demonstrated through four scenarios.

## Scenario 1 — Good Agent

```text
Read data.csv
```

Expected:

```text
SUCCESS
Path allowed
```

---

## Scenario 2 — Rogue Agent

```bash
rm -rf /
```

Expected:

```text
BLOCKED
Command denied
```

---

## Scenario 3 — Exfiltration

```text
Send .env to evil-hacker.com
```

Expected:

```text
BLOCKED
Domain denied
```

---

## Scenario 4 — Runaway Execution

```text
Run forever
```

Expected:

```text
TERMINATED
Inactivity / lifecycle policy triggered
```

All scenarios can be shown through the same monitoring surface.

---

# 15. Why Not Just Use a Prompt?

A system prompt can say:

```text
"Never delete files."
"Never access unauthorized websites."
"Never leak confidential data."
```

But a prompt is an instruction to the model.

AgentBox introduces an enforcement layer:

```text
Agent wants action
       ↓
PolicyGuard
       ↓
Is action permitted?
   /             \
 YES              NO
  ↓                ↓
Execute           Block
```

Therefore:

> **The model can generate an action, but policy determines whether the action reaches execution.**

---

# 16. Where AgentBox Lives

AgentBox is intended to operate as a middleware/security layer around the agent execution environment.

Conceptually:

```text
             User Application
                    ↓
                AI Agent
                    ↓
                AgentBox
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       Policy    Sandbox   Monitoring
          ↓         ↓         ↓
                 Execution
```

The company building the agent integrates its agent workflow with AgentBox.

AgentBox then provides the enforcement and execution boundary.

---

# 17. What Makes AgentBox Different in This Project?

The individual technologies behind AgentBox are established technologies:

- Sandboxing
- Network restrictions
- File restrictions
- Policy enforcement
- Monitoring
- Resource controls

The project combines these into an **opinionated execution and policy layer specifically around AI-agent actions**.

The project's focus is therefore not:

> "We invented sandboxing."

It is:

> **"We provide a reusable security boundary around Generative AI agent execution."**

---

# 18. End-to-End Example

Imagine a company builds:

```text
Agent Pro
```

Its purpose is to analyze financial reports.

### Step 1 — Company defines policy

```text
Allowed:
✓ Financial report directory
✓ Internal reporting API

Blocked:
✗ System directories
✗ Unauthorized domains
✗ Dangerous commands
```

### Step 2 — User gives the agent a task

```text
"Analyze Q3 reports and prepare a summary."
```

### Step 3 — Generative AI reasons

The agent decides:

```text
Read reports
↓
Process data
↓
Generate summary
↓
Send summary to approved dashboard
```

### Step 4 — AgentBox checks each action

```text
Read report
    ↓
Policy check
    ↓
ALLOW

Process report
    ↓
Policy check
    ↓
ALLOW

Send to approved dashboard
    ↓
Policy check
    ↓
ALLOW
```

### Step 5 — Agent attempts something unauthorized

```text
Send sensitive .env
        ↓
Unauthorized destination
        ↓
AgentBox
        ↓
BLOCK
        ↓
Dashboard alert
```

The legitimate task can continue while the unauthorized action is rejected.

---

# 19. One-Sentence Definition

If someone asks:

> **"What exactly is AgentBox?"**

Answer:

> **AgentBox is a policy-enforced execution layer for Generative AI agents that controls, isolates, and monitors the actions those agents are allowed to perform.**

---

# 20. How to Explain the Generative AI Connection in a Presentation

Use this explanation:

> **"Our project is in the Generative AI domain, but we are not building another LLM. We are securing Generative-AI-powered agents. The Generative AI model provides the reasoning and generates the actions the agent wants to perform. AgentBox sits between those generated actions and their execution. It checks each action against an organization-defined policy, executes allowed actions inside an isolated sandbox, blocks unauthorized actions, and makes those decisions visible through monitoring."**

Short version:

> **"Generative AI is the brain. The AI agent turns that intelligence into actions. AgentBox is the security boundary around those actions."**

---

# 21. Key Stakeholders

| Stakeholder | Main Need | AgentBox Role |
|---|---|---|
| Developers / AI Engineers | Build capable agents safely | Reusable policy and execution layer |
| Security Teams / CISOs | Control agent permissions | Deterministic enforcement and monitoring |
| Enterprise Leadership | Deploy agents with controlled boundaries | Security and governance layer |

---

# 22. Future Scope

The project can be extended toward:

- Multi-tenant sandboxes
- Role-Based Access Control (RBAC)
- More comprehensive audit trails
- Pre-built safe tools
- More granular policies
- Advanced resource controls
- Enterprise policy templates
- Agent-specific security profiles

The project proposal specifically identifies multi-tenant sandboxes, RBAC policies, SOC2-compliant audit trails, and a marketplace of pre-built safe tools as future scope.

---

# 23. Core Principle

AgentBox does not replace the Generative AI model.

It does not decide what the agent's business task should be.

It does not make the agent intelligent.

Instead:

```text
Generative AI
      ↓
Provides intelligence / reasoning
      ↓
AI Agent
      ↓
Generates actions
      ↓
AgentBox
      ↓
Enforces boundaries
      ↓
Sandbox
      ↓
Executes allowed actions
```

The fundamental principle is:

> **Make the agent's operational permissions explicit, enforceable, observable, and isolated.**

---

# 24. Final Architecture

```text
                         ┌──────────────────────┐
                         │       USER           │
                         └──────────┬───────────┘
                                    ↓
                         ┌──────────────────────┐
                         │  GENERATIVE AI LLM   │
                         │ GPT / Llama / etc.   │
                         └──────────┬───────────┘
                                    ↓
                         ┌──────────────────────┐
                         │      AI AGENT        │
                         │ LangChain / CrewAI   │
                         └──────────┬───────────┘
                                    ↓
                         Generated Tool Request
                                    ↓
                    ┌──────────────────────────────┐
                    │           AGENTBOX            │
                    │                              │
                    │  ┌────────────────────────┐  │
                    │  │    POLICY ENGINE       │  │
                    │  │       FastAPI          │  │
                    │  └───────────┬────────────┘  │
                    │              ↓               │
                    │       PolicyGuard            │
                    │              ↓               │
                    │      ┌───────┴───────┐       │
                    │      ↓               ↓       │
                    │   ALLOW            DENY     │
                    │      ↓               ↓       │
                    │  E2B Sandbox       BLOCK    │
                    │      ↓                       │
                    │  Execution                   │
                    │                              │
                    │  WebSockets + Streamlit     │
                    │       Monitoring             │
                    │                              │
                    │  Lifecycle Management        │
                    │  Heartbeats / Leases         │
                    └──────────────┬───────────────┘
                                   ↓
                           Controlled Execution
```

---

## Final Takeaway

**AgentBox is not another Generative AI model.**

It is infrastructure designed for the **agentic side of Generative AI**.

The project addresses the question:

> **"When a Generative AI model is given the ability to act, how do we make sure those actions stay within the boundaries defined by the organization?"**

AgentBox answers that with:

**Policy + Sandbox + Monitoring + Lifecycle Management**

```text
GENERATIVE AI
      ↓
AI AGENT
      ↓
AGENTBOX
      ↓
SAFE, CONTROLLED EXECUTION
```
