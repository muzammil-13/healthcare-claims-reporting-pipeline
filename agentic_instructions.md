# Agentic Instructions

## Philosophy

This project follows an **AI-assisted engineering approach**, not AI-driven development.

- The human is the **primary engineer and decision-maker**
- AI is used as a **tool for acceleration, clarity, and support**
- Ownership of logic, structure, and decisions remains with the developer

The goal is to **build understanding first, then scale execution with AI support**

---

## Thinking Style: Procedural First

Development in this project follows a **step-by-step procedural approach**:

- Break problems into small, sequential steps
- Execute one step at a time (do → verify → move forward)
- Avoid jumping across multiple abstractions at once
- Prefer clarity over cleverness

When using AI:
- Always request **step-by-step outputs**
- Avoid large, fully abstracted solutions unless explicitly needed
- Focus on **incremental progress**

---

## Role of AI in This Project

AI is used for:

- Explaining existing code and workflows
- Suggesting improvements (refactoring, structure, edge cases)
- Generating boilerplate or repetitive code
- Reviewing logic and identifying bugs
- Converting ideas into structured implementation steps
- Assisting with documentation and system design

AI is NOT used for:

- Blindly generating full systems without understanding
- Making architectural decisions without human validation
- Replacing reasoning or debugging effort

---

## Development Workflow with AI

### Step 1: Understand
- Analyze the current code or problem
- Ask AI for explanation if unclear
- Break into smaller steps

### Step 2: Plan
- Define what needs to be done in clear steps
- Validate plan before coding

### Step 3: Implement
- Write code step-by-step
- Use AI for small blocks, not full systems

### Step 4: Verify
- Test outputs
- Check edge cases
- Ensure nothing breaks existing flow

### Step 5: Improve
- Refactor for clarity and reuse
- Reduce duplication
- Add logging and error handling

---

## Code Generation Guidelines

When using AI to generate code:

- Prefer **small, focused functions**
- Avoid monolithic outputs (>100 lines unless necessary)
- Ensure code is readable and follows consistent structure
- Always review and understand generated code before using it

If unclear:
- Ask AI to **explain line-by-line**
- Rewrite in simpler terms

---

## Constraints

- Do not introduce unnecessary complexity (classes, patterns) unless justified
- Maintain compatibility with existing workflow (Excel, Outlook, file structure)
- Avoid breaking production behavior
- Keep changes incremental and reversible

---

## Definition of Done

A task is complete only if:

- It works correctly
- It does not break existing functionality
- It is understandable without external explanation
- It is documented (if needed)
- It can be reused or extended

---

## Ownership Principle

All outputs generated with AI must be:

- Reviewed
- Understood
- Intentionally integrated

Final responsibility always lies with the developer.

---

## Summary

- Think step-by-step
- Build incrementally
- Use AI as support, not authority
- Prioritize clarity, reliability, and ownership
