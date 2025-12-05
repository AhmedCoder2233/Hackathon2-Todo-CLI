---

description: "Task list for Add Advanced Features to Todo App feature implementation"
---

# Tasks: Add Advanced Features to Todo App

**Input**: Design documents from `/specs/003-todo-advanced-features/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: This plan will generate test tasks, as the project constitution mandates TDD.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description with file path`

-   **[P]**: Can run in parallel (different files, no dependencies)
-   **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
-   Include exact file paths in descriptions

## Path Conventions

-   **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Project Structure & Environment)

**Purpose**: Initialize the project structure and ensure the environment is ready for development.

- [x] T001 Create `src/lib/` directory for utility functions.
- [x] T002 Create `tests/contract/` directory for contract tests.
- [x] T003 Create `tests/integration/` directory for integration tests.

---

## Phase 2: Foundational (Core Model & Service Extensions)

**Purpose**: Implement core extensions to the `Task` model and `TaskService` that are prerequisites for both user stories.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Tests for Foundational Phase ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T004 [P] Create initial unit test for extended Task model attributes in `tests/unit/test_task_model_extensions.py`.
- [x] T005 [P] Create initial unit test for TaskService methods related to new attributes in `tests/unit/test_task_service_extensions.py`.

### Implementation for Foundational Phase

- [x] T006 Extend `Task` model in `src/models/task.py` with `due_date`, `due_time`, `recurrence_type`, `reminder_minutes_before_due`, `original_recurring_task_id`.
- [x] T007 Implement validation logic for `due_date` (not in past) and `due_time` (24-hour format) in `src/models/task.py` or a dedicated validation utility in `src/lib/`.
- [x] T008 Update `TaskService` constructor/initialization to handle new Task attributes in `src/services/task_service.py`.
- [x] T009 Create `Notification` model in `src/models/notification.py` with `id`, `message`, `trigger_time`, `task_id`, `is_delivered`, `delivered_at`.
- [x] T010 Create `NotificationService` in `src/services/notification_service.py` to manage `Notification` entities.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Create and Manage Recurring Tasks (P1) 🎯 MVP

**Goal**: Users can define tasks that repeat and new instances are generated automatically upon completion.

**Independent Test**: A user can create a daily recurring task, mark it complete, and verify that a new instance for the next day with correct details is generated.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T011 [P] [US1] Unit test for `Task` model's recurrence logic (e.g., `get_next_recurrence_date`) in `tests/unit/test_task_recurrence.py`.
- [x] T012 [P] [US1] Unit test for `TaskService.create_recurring_task` in `tests/unit/test_task_service_recurring.py`.
- [x] T013 [P] [US1] Unit test for `TaskService.handle_task_completion_recurrence` (auto-generation) in `tests/unit/test_task_service_recurring.py`.
- [x] T014 [P] [US1] Unit test for preventing duplicate recurring instances (FR-005) in `tests/unit/test_task_service_recurring.py`.
- [x] T015 [US1] Integration test for full recurring task lifecycle (create, complete, auto-generate) in `tests/integration/test_recurring_tasks.py`.

### Implementation for User Story 1

- [x] T016 [US1] Implement `TaskService.create_recurring_task` to set `recurrence_type` and `due_date` (FR-001).
- [x] T017 [US1] Implement `TaskService.get_next_recurrence_date` logic (daily, weekly, monthly) in `src/services/task_service.py` or `src/lib/recurrence_util.py`.
- [x] T018 [US1] Modify `TaskService.mark_as_complete` to trigger new instance generation for recurring tasks (FR-002).
- [x] T019 [US1] Implement `TaskService.generate_next_recurring_instance` to inherit attributes and adjust due date (FR-003, FR-004).
- [x] T020 [US1] Implement `TaskService.prevent_duplicate_recurring_instances` logic (FR-005).
- [x] T021 [US1] Update CLI `main.py` to support `add`/`update` commands with `--recurrence` options.

**Checkpoint**: User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Set Due Dates and Receive Reminders (P1)

**Goal**: Users can set due dates/times for tasks, view overdue tasks, and receive notifications.

**Independent Test**: A user can create a task with a future due date and reminder, then (simulating time passing) verify that the task becomes overdue and a notification is triggered.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T022 [P] [US2] Unit test for `Task` model's due date/time handling (e.g., `is_overdue`) in `tests/unit/test_task_duedate.py`.
- [x] T023 [P] [US2] Unit test for `NotificationService.schedule_notification` in `tests/unit/test_notification_service.py`.
- [x] T024 [P] [US2] Unit test for overdue task detection logic in `tests/unit/test_task_service_overdue.py`.
- [x] T025 [P] [US2] Unit test for due date/time validation (FR-009, FR-010) in `tests/unit/test_task_duedate.py`.
- [x] T026 [US2] Integration test for task with due date/reminder lifecycle (create, check overdue, trigger notification) in `tests/integration/test_reminders_overdue.py`.

### Implementation for User Story 2

- [x] T027 [US2] Implement/refine `TaskService.add_due_date_time` (FR-006) including validation (FR-009, FR-010).
- [x] T028 [US2] Implement `TaskService.get_overdue_tasks` and update CLI display logic in `src/cli/main.py` (FR-007).
- [x] T029 [US2] Implement `NotificationService.schedule_reminder` to create `Notification` entities with correct `trigger_time` (FR-008).
- [x] T030 [US2] Implement mechanism to periodically check `Notification` entities and trigger browser/app notifications (e.g., a background process or CLI command) in `src/lib/notification_manager.py` and `src/cli/main.py`.
- [x] T031 [US2] Update CLI `main.py` to support `add`/`update` commands with `--due`, `--time`, `--remind` options.

**Checkpoint**: User Stories 1 AND 2 should both work independently.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories or general project quality.

- [x] T032 Code cleanup and refactoring in `src/models/`, `src/services/`, `src/lib/`.
- [x] T033 Update documentation in `README.md` and `quickstart.md` to reflect new features.
- [x] T034 Run quickstart.md validation by manually testing scenarios described in `specs/003-todo-advanced-features/quickstart.md`.
-   [X] T035 Ensure memory usage is within <100MB constraint (profile and optimize) in `src/`.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately.
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
-   **User Stories (Phase 3 & 4)**: Both depend on Foundational phase completion.
    *   User Story 1 (P1) and User Story 2 (P1) can proceed in parallel once foundational tasks are done.
-   **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2). No dependencies on User Story 2.
-   **User Story 2 (P1)**: Can start after Foundational (Phase 2). No dependencies on User Story 1, though it may interact with the same `Task` model extensions.

### Within Each User Story

-   Tests MUST be written and FAIL before implementation.
-   Models/Utilities before services.
-   Services before CLI integration.
-   Core implementation before integration.
-   Story complete before moving to next priority (or marking as ready for parallel work).

### Parallel Opportunities

-   All Setup tasks can run in parallel.
-   Initial test creation for Foundational phase (`T004`, `T005`) can run in parallel.
-   Once Foundational phase completes, User Story 1 and User Story 2 can be developed in parallel by different team members.
-   Within User Story 1, tasks `T011` to `T014` (tests) can be parallelized.
-   Within User Story 2, tasks `T022` to `T025` (tests) can be parallelized.
-   Polish tasks `T032`, `T033`, `T034`, `T035` can be worked on concurrently if independent areas.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done:
    *   Developer A: User Story 1
    *   Developer B: User Story 2
3.  Stories complete and integrate independently

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
