# Dev Workflow Checklist (Daily Execution System)

## Purpose

This checklist ensures consistent, structured progress on the project using a **procedural, step-by-step approach**.

The focus is:
- Small wins daily
- Zero chaos
- Continuous improvement without burnout

---

## 🟢 Phase 0: Session Setup (5 mins)

- [ ] Define ONE clear goal for this session  
  (Example: "Add logging to file read section")

- [ ] Identify exact file/module to work on  
  (Example: `data_loader.py`)

- [ ] Open only required files (avoid distractions)

---

## 🟡 Phase 1: Understand (10–15 mins)

- [ ] Read the relevant code section fully
- [ ] Identify:
  - Inputs
  - Outputs
  - Dependencies

- [ ] If unclear:
  - [ ] Ask AI for explanation
  - [ ] Break logic into steps

✅ Output of this phase:  
“I clearly understand what this part does”

---

## 🔵 Phase 2: Plan (5–10 mins)

- [ ] Write step-by-step plan (max 3–5 steps)

Example:
1. Add logging setup
2. Replace print with logging
3. Test execution

- [ ] Validate plan (mentally or with AI)

❗ Rule: No coding before plan is clear

---

## 🟠 Phase 3: Implement (30–60 mins)

- [ ] Code ONE step at a time
- [ ] After each step:
  - [ ] Run the code
  - [ ] Check output

- [ ] Use AI only for:
  - Small code snippets
  - Debugging specific issues

❗ Rules:
- No big rewrites
- No jumping between files randomly

---

## 🔴 Phase 4: Verify (10–15 mins)

- [ ] Run full flow (if possible)
- [ ] Check:
  - [ ] No crashes
  - [ ] Output is correct
  - [ ] Existing functionality still works

- [ ] Test at least one edge case

Example:
- Missing file
- Empty data

---

## 🟣 Phase 5: Improve (Optional, 10 mins)

- [ ] Can this be simplified?
- [ ] Any duplicate logic?
- [ ] Add:
  - [ ] Logging (if missing)
  - [ ] Error handling (if missing)

---

## ⚫ Phase 6: Document (5–10 mins)

- [ ] Update README / SOP if needed
- [ ] Add short comment in code (if logic is tricky)

- [ ] Write 1–2 lines of what was done today

Example:
"Added logging and error handling to CSV loading step"

---

## ⚪ Phase 7: Close Session (2 mins)

- [ ] Confirm goal is completed ✅
- [ ] Define next step for tomorrow

Example:
"Next: Move file paths to config.ini"

---

# 🔁 Weekly Checkpoint (once a week)

- [ ] What did I improve this week?
- [ ] What is still messy?
- [ ] What is breaking or risky?
- [ ] Pick ONE thing to improve next week

---

# 🚫 Anti-Patterns (Avoid These)

- [ ] Jumping between multiple features
- [ ] Writing code without understanding
- [ ] Copy-pasting large AI outputs blindly
- [ ] Trying to refactor everything at once
- [ ] Skipping testing

---

# ✅ Golden Rules

- One task at a time
- One file at a time
- One improvement at a time

Consistency > intensity

---

# 🧠 Mental Model

Understand → Plan → Implement → Verify → Improve

Repeat daily.

---

# 📌 Example Daily Session

Goal: Add error handling to Excel write

1. Understand Excel write logic  
2. Plan try/except block  
3. Implement error handling  
4. Test with file open scenario  
5. Log error message  
6. Document change  

Done.

---

## Final Note

Progress is not about doing more.

It’s about doing **one thing properly, every day**.
