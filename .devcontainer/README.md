# Development Environment

This project includes a dev container setup for consistent development across different machines, with support for both Docker and Podman container runtimes.

## Quick Start

1. **Using Workspace File**: Open `field-network-checker.code-workspace` in VS Code
2. **Choose Runtime**: VS Code will prompt you to select a dev container configuration
3. **Select Environment**: Pick either Docker or Podman version

## Manual Setup

1. Install VS Code and the "Dev Containers" extension
2. Install either Docker or Podman (or both) on your system
3. Open the project in VS Code

## Choosing Container Runtime

### Option 1: Using VS Code's Dev Container Picker
When you open the project, VS Code will show available dev container configurations:

- **"Field Network Checker Dev (Docker)"** - Uses Docker runtime
- **"Field Network Checker Dev (Podman)"** - Uses Podman runtime

Choose the one that matches your installed container runtime.

### Option 2: Manual Runtime Configuration
You can also configure the runtime in VS Code settings:

**For Docker:**
```json
{
  "dev.containers.dockerPath": "docker",
  "dev.containers.dockerComposePath": "docker compose"
}
```

**For Podman:**
```json
{
  "dev.containers.dockerPath": "podman",
  "dev.containers.dockerComposePath": "podman-compose"
}
```

## Usage

Once in the dev container:

- **Run Tests**: Ctrl+Shift+P → "Tasks: Run Task" → "Run Tests"
- **Install Dependencies**: Ctrl+Shift+P → "Tasks: Run Task" → "Install Dependencies"
- **Run App**: Ctrl+Shift+P → "Tasks: Run Task" → "Run App"

## Architecture

- `fnc-app`: Production application container
- `fnc-dev`: Development container with full workspace access
- Both containers run simultaneously for testing integration

## Requirements

- **Docker**: Docker Engine installed and running
- **Podman**: Podman installed with `podman-compose` for compose file support

## Files

- `field-network-checker.code-workspace`: VS Code workspace file with default Docker settings
- `.devcontainer/devcontainer.json`: Docker dev container configuration
- `.devcontainer/devcontainer.podman.json`: Podman dev container configuration
- `.devcontainer/docker-compose.dev.yaml`: Development service definition
- `.vscode/tasks.json`: VS Code tasks for common operations
- `.vscode/settings.json`: Default VS Code settings (can be overridden)