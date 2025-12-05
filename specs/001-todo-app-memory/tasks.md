# Tasks: Todo App Memory-Based Specification

**Input**: Design documents from `/specs/001-todo-app-memory/`
**Prerequisites**: plan.md, spec.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure (`src/models`, `src/services`, `src/cli`, `tests/unit`)
- [X] T002 Initialize `uv` environment with `uv init`
- [X] T003 [P] Configure `.gitignore` for Python projects.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T004 [P] Create `Task` model in `src/models/task.py` based on `data-model.md`.
- [X] T005 Create `TaskService` in `src/services/task_service.py` to manage tasks in an in-memory dictionary. It should include basic CRUD methods.

---

## Phase 3: User Story 1 - Core Task Management (Priority: P1) 🎯 MVP

**Goal**: Implement adding, viewing, updating, deleting, and completing tasks.

**Independent Test**: A user can perform all core task management operations via the CLI.

### Tests for User Story 1 ⚠️

- [X] T006 [P] [US1] Write unit tests for `TaskService` in `tests/unit/test_task_service.py` for adding and retrieving tasks.
- [X] T007 [P] [US1] Write unit tests for `TaskService` in `tests/unit/test_task_service.py` for updating and deleting tasks.
- [X] T008 [P] [US1] Write unit tests for `TaskService` in `tests/unit/test_task_service.py` for completing tasks.

### Implementation for User Story 1

- [X] T009 [US1] Implement the `add` command in `src/cli/main.py`.
- [X] T010 [US1] Implement the `list` command in `src/cli/main.py`.
- [X] T011 [US1] Implement the `update` command in `src/cli/main.py`.
- [X] T012 [US1] Implement the `delete` command in `src/cli/main.py`.
- [X] T013 [US1] Implement the `complete` command in `src/cli/main.py`.

---

## Phase 4: User Story 2 - Task Prioritization and Organization (Priority: P2)

**Goal**: Implement setting priorities and tags for tasks.

**Independent Test**: A user can set a priority and add tags to a task via the CLI.

### Tests for User Story 2 ⚠️

- [X] T014 [P] [US2] Write unit tests in `tests/unit/test_task_service.py` for setting task priority.
- [X] T015 [P] [US2] Write unit tests in `tests/unit/test_task_service.py` for adding tags to a task.

### Implementation for User Story 2

- [X] T016 [US2] Implement the `priority` command in `src/cli/main.py` to set a task's priority.
- [X] T017 [US2] Implement the `tag` command in `src/cli/main.py` to add tags to a task.

---

## Phase 5: User Story 3 - Search, Filter, and Sort (Priority: P3)

**Goal**: Implement searching, filtering, and sorting of tasks.

**Independent Test**: A user can search, filter, and sort tasks via the CLI.

### Tests for User Story 3 ⚠️

- [X] T018 [P] [US3] Write unit tests in `tests/unit/test_task_service.py` for searching tasks by keyword.
- [X] T019 [P] [US3] Write unit tests in `tests/unit/test_task_service.py` for filtering tasks by status and priority.
- [X] T020 [P] [US3] Write unit tests in `tests/unit/test_task_service.py` for sorting tasks.

### Implementation for User Story 3

- [X] T021 [US3] Extend the `list` command in `src/cli/main.py` to support searching.
- [X] T022 [US3] Extend the `list` command in `src/cli/main.py` to support filtering.
- [X] T023 [US3] Extend the `list` command in `src/cli/main.py` to support sorting.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T024 [P] Add docstrings and type hints to all new code.
- [X] T025 [P] Update `README.md` with instructions on how to use the application.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed before all other phases.
- **Phase 2 (Foundational)** depends on Phase 1 and blocks all user story phases.
- **User Story Phases (3-5)** can be implemented sequentially after Phase 2 is complete.
- **Phase N (Polish)** can be done after all user stories are implemented.
