---
id: 0001
title: Establish Project Constitution and Principles
stage: constitution
date: 2025-12-03
surface: agent
model: gemini
feature: none
branch: master
user: Ahmed
command: /sp.constitution
labels: [constitution, principles, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
app_name: TodoApp

principles:
  - OOP + TDD (Red → Green → Refactor)
  - Clean, readable code with comments
  - Modular classes, single responsibility
  - All shell commands should use WSL

core_essentials:
  - AddTask: "Create new todo item with unique ID"
  - DeleteTask: "Remove task safely"
  - UpdateTask: "Edit task details"
  - ViewTaskList: "Show all tasks clearly"
  - MarkAsComplete: "Toggle complete/incomplete"

intermediate_features:
  - PrioritiesAndTags: "High/Medium/Low + user tags"
  - SearchAndFilter: "Search by keyword, filter by status/priority/date"
  - SortTasks: "Sort by date, priority, alphabetically"

advanced_features:
  - RecurringTasks: "Auto-reschedule repeating tasks"
  - DueDatesAndReminders: "Set deadlines + browser notifications"

testing_rules:
  - Unit tests for every feature
  - Red-Green-Refactor cycle
  - Test edge cases (empty title, duplicates, overdue tasks)

clean_code:
  - Comment why, not what
  - No magic numbers
  - DRY + small methods + meaningful names
```

## Response snapshot

I have updated the project constitution at `.specify/memory/constitution.md` based on your input. The new version is 1.0.0. I also verified that no other files required updates.

## Outcome

- ✅ Impact: Project constitution established with core principles, features, and standards.
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Suggest creating a feature spec with `/sp.specify`
- 🧠 Reflection: The initial constitution provides a strong foundation for the project.

## Evaluation notes (flywheel)

- Failure modes observed: Initial script execution failed to create the PHR file due to missing directory and incorrect command execution.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Ensure shell commands are executed with the correct interpreter (e.g., bash) and flags.