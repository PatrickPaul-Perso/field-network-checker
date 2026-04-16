# Project Overview

## Name

Field Network Checker

## Product Summary

Field Network Checker is a local-first tool used to quickly assess live Ethernet state and supporting field metadata.

Its main job is to reduce uncertainty during field work by making network status obvious and fast to interpret.

## Core User Outcomes

The product should help a user do these things quickly:

- see whether Ethernet link is up or down
- see the active interface name
- see the current IP address
- determine whether the current IP matches a target legacy prefix
- capture field metadata without slowing down the operator
- trust that the displayed state matches reality

## Design Principles

### Local first
The tool must remain useful even with limited or no external connectivity.

### Field ready
The interface should be fast to read, easy to operate, and resilient in less-than-ideal environments.

### Minimal friction
The operator should not need to interpret multiple low-level indicators to answer a simple question.

### Clear state
Visual states must be obvious and map directly to operational meaning.

### Safe defaults
Behavior should favor predictable and conservative outcomes.

## Current Product Direction

The product emphasizes:
- live Ethernet visibility
- simple visual status signaling
- configurable detection of a target network prefix
- lightweight metadata capture
- practical deployment on small field devices

## Important Domain Concepts

### Link up
The physical Ethernet link is active.

### Link down
The physical Ethernet link is not active.

### Legacy network match
The assigned IP matches a configured target prefix used to identify a legacy network context.

### Non-legacy network
The assigned IP does not match the configured target prefix.

## User Experience Priorities

In order:
1. Immediate readability
2. Correct network interpretation
3. Minimal clicks and typing
4. Stable behavior
5. Maintainable implementation

## Constraints

- The product must stay understandable by non-developers in the field.
- UI changes must preserve quick visual scanning.
- Network logic must stay explicit and testable.
- Config behavior must remain predictable.

## Notes For Codex

When working in this repo:
- prefer small changes
- explain network-related behavior clearly
- avoid adding layers of abstraction without strong benefit
- preserve field usability
- document any new operator-visible behavior