# GRNT CODE

```
   ______ ____   _   __ ______
  / ____// __ \ / | / //_  __/
 / / __ / /_/ //  |/ /  / /   
/ /_/ // _, _// /|  /  / /    
\____//_/ |_|/_/ |_/  /_/     
   ______ ____   ____   ______
  / ____// __ \ / __ \ / ____/
 / /    / / / // / / // __/   
/ /___ / /_/ // /_/ // /___   
\____/ \____//_____//_____/   
```

**GRNT CODE** is a specialized, high-performance, Docker-only CLI coding agent.
 It provides a surgical approach to coding tasks by interfacing with local LLMs via Ollama.

## Features

- **Tactical Performance**:
    - **Streaming Responses**: Real-time generation for a faster feel.
    - **Persistent Memory**: Saves history in `.grnt_code_history.json` so you can resume sessions.
    - **Search Engine**: New `search_files` tool for finding code patterns instantly.
    - **Manual Confirmation**: Built-in safety for terminal commands.
- **Direct Persona**: A clean, professional system prompt focused on code.
- **Ollama Integration**: Uses locally hosted models (defaults to `granite4:3b`).
- **Modern TUI**: A beautiful terminal interface with clean block ASCII art.

## Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose.
- [Ollama](https://ollama.com/) running on your host machine.

## Getting Started

1. **Verify Ollama is running**:
   Ensure `ollama serve` is active and you have the `granite4:3b` model downloaded (`ollama pull granite4:3b`).

2. **Clone and Build**:
   ```powershell
   docker-compose build
   ```

3. **Deploy the Agent**:
   ```powershell
   docker-compose run agent48
   ```

## Usage

Once active, use the `MISSION >` prompt to give instructions.

- **Filesystem**: "List the files in the src folder" or "Read main.py".
- **Creation**: "Create a new Python script that calculates fibonacci numbers".
- **Execution**: "Run the tests" or "Check the python version".

## Mission Control

You can specify a different model at runtime:
```powershell
docker-compose run agent48 --model llama3.2:3b
```

---
*Functional. Direct. Local.*
