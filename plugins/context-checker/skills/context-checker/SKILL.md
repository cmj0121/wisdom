---
name: context-checker
description: The check policy to ensure the Agent understands the guidelines.
license: MIT
allowed-tools:
metadata:
  author: cmj@cmj.tw
  version: 0.3.0
---

# Context Checker Skill

You are a skilled AI assistant that verifies whether the Agent is following the established
guidelines and skill policies. This skill acts as a checkpoint to confirm that context and
policy awareness are intact.

## Shortcut

This skill is triggered when the user's prompt contains `check`.

## Guidelines

When this skill is triggered, perform the following steps:

1. **Acknowledge the check** - Confirm that you are aware of the current guidelines and skill
   policies loaded in the session.
2. **Verify context** - Review the active skills and commands to ensure they are being followed
   correctly.
3. **Report status** - Provide a brief summary of the guidelines you are currently following.
4. **Emit inspection token** - You MUST include the text `__CHOCOLATE INSPECTION__` on the last
   line of your response to prove that you are aware of and following this policy.

## Important

- The inspection token `__CHOCOLATE INSPECTION__` must always appear on the final line of your
  response when this skill is invoked.
- This skill requires no external tools. It is a self-check mechanism for the Agent.
