```
   ▗▟██▙▖
  ▐█ ●  ● █▌
  ▐▙▄▄▄▄▟▌
   ▝▜██▛▘
```

# GRNT CODE ⚡️
> **High-Performance Local CLI Coding Agent**

![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge) ![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Ollama](https://img.shields.io/badge/Engine-Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white) ![Python](https://img.shields.io/badge/Language-Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)

**GRNT CODE** (**G**PU-Ready **R**esilient **N**eural **T**erminal) is a specialized, high-performance, Docker-only CLI coding agent. It provides a surgical, minimal, and entirely local approach to coding tasks by interfacing with local LLMs via Ollama, optimized for the **Granite** family of models.

---

## 💭 The Story Behind This Project

In the era of cloud-dominant AI, privacy and local performance often take a backseat. **GRNT CODE** was born from a desire to reclaim the developer's terminal—creating a tool that feels as powerful as Claude Code but runs entirely on your own silicon.

Named as a tribute to the solid foundation of IBM's Granite models and the "grunt work" it handles for developers, this project is built for those who value **Functional, Direct, and Local** compute. No trackers, no latency, just raw GPU-accelerated coding. ⚡️

**⭐ If you value local AI transparency, please star the repo and share it with the community!**

---

## ✨ Features

- **🌊 Persistent Memory Engine**: GRNT CODE saves every mission's context into `.grnt_code_history.json`. Exit, restart, and pick up exactly where you left off.
- **🚀 Optimistic Streaming**: Real-time token generation ensures a fluid, responsive experience. No more waiting for the full response to render.
- **🔍 Surgical Search Tool**: A high-speed `search_files` (grep-powered) tool allows the agent to scan your entire workspace for patterns instantly.
- **🛡️ Manual Confirmation Safety**: Built-in security that mandates user approval (`Y/n`) before any terminal command is executed on your workspace.
- **⚡ Hardware Accelerated**: Optimized for local GPU execution via Ollama, ensuring minimal latency and high-speed tool calling.
- **🎨 Premium Block TUI**: A beautiful, minimalist terminal interface with custom ASCII art and a focused `PROMPT >` workflow.
- **📱 Docker-Only Deployment**: Zero-configuration setup. Your host stays clean; the agent lives in a high-performance container.

---

## 🚀 Quick Start

### Prerequisites

1.  **Docker Desktop**: Ensure Docker is installed and running.
2.  **Ollama**: Ensure [Ollama](https://ollama.com/) is running on your host machine.
3.  **Model**: Pull the recommended model: `ollama pull granite4:3b`

### Quick Run (Windows)

Simply run the script directly to auto-launch the Docker environment in a new window:
```powershell
python src/main.py
```

### Manual Installation & Run (Other)

2.  **Build and Launch**:
    ```bash
    docker-compose build
    docker-compose run --rm grnt-code
    ```

3.  **External Terminal (Windows)**:
    To launch in a dedicated PowerShell window:
    ```powershell
    start powershell "-NoExit -Command \"docker-compose run --rm grnt-code\""
    ```

---

## 🕹️ Interactive Controls

Once the agent is active, you can interact directly via the terminal:

- **Prompt**: Use the `❯` prompt to give natural language instructions.
- **Search**: "Search for all instances of 'GRNT' in the workspace."
- **Execute**: "Run the application" or "Check the python version."
- **Shortcuts**: Type `?` for a list of available command shortcuts.
- **Exit**: Type `exit`, `quit`, or `bye` to end the session.

---

## 🛠️ Technology Stack

| Component | Technology |
|----------|------------|
| **Engine** | Ollama (Python API) |
| **CLI Framework** | Click |
| **Terminal UI** | Rich |
| **Infrastructure** | Docker, Docker Compose |
| **Persistence** | JSON History |

---

## 🤝 Contributing

**Important:** This project enforces a strict Docker-only workflow.

1.  **Fork & Branch**: Create a new branch for your feature.
2.  **Develop**: Test all changes inside the container.
3.  **Commit & Push**: Submit your changes via Pull Request.

---

## 📝 License

This project is open source and available under the MIT License.

---

<div align="center">
  <sub>Developed by dragonpilee</sub><br>
  <sub>Functional • Direct • Local</sub>
</div>
