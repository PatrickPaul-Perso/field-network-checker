# Architecture

## Status

This is a living document. Update it as the codebase stabilizes.

## High-Level Shape

Field Network Checker is expected to have these layers:

1. Network state collection
2. Application logic
3. UI rendering and interaction
4. Configuration and persistence
5. Packaging or deployment

## Likely Code Areas

Update this section to match the real repository structure.

### Backend
Expected responsibilities:
- collect link state
- collect interface and IP details
- apply legacy-prefix matching logic
- expose status data to the UI
- persist config and readings if supported

Typical files:
- `app/src/app.py`
- helpers under a backend or utilities module
- config or persistence modules

### Frontend
Expected responsibilities:
- render live Ethernet state
- display interface and IP clearly
- apply clear visual states
- handle user input for metadata and settings
- refresh status without confusing transitions

Typical files:
- HTML templates
- CSS assets
- JavaScript for polling and state updates

### Deployment
Expected responsibilities:
- local app launch
- container setup
- environment configuration

Typical files:
- `compose.yml` or `docker-compose.yml`
- Dockerfile
- service or startup scripts

## Core Data Flow

1. Read current network state from the host
2. Normalize the raw values
3. Determine link state
4. Determine IP state
5. Compare IP against configured target prefix
6. Return a compact model for UI display
7. Persist operator-entered data if the workflow requires it

## Architectural Rules

- Keep the network-state path simple and observable.
- Keep UI state mapping deterministic.
- Do not bury operator-visible logic inside scattered helpers.
- Keep config loading and saving explicit.
- Prefer one clear source of truth for live status.
- Avoid mixing field metadata rules with raw network polling logic.

## Extension Points

Possible future additions:
- more explicit persistence layer
- export workflows
- richer diagnostics
- hardware-specific integrations
- offline sync workflows
- additional device profiles

## Non-Goals

Unless explicitly requested:
- do not introduce unnecessary frameworks
- do not split the app into services
- do not optimize for scale before clarity
- do not redesign the UI around novelty

## Code Map To Complete

Replace these placeholders with the actual repository map.

### Entry points
- main application entry:
- local run command:
- container run command:

### Key modules
- network state:
- config:
- persistence:
- UI template:
- frontend logic:
- styling:

### Critical behaviors to protect
- link up and link down reporting
- IP display
- legacy-prefix detection
- config persistence
- form defaults and saved values
