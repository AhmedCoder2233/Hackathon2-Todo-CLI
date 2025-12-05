# Testable Tasks: Intermediate Task Features for Todo App

**Feature Branch**: `002-intermediate-task-features` | **Date**: 2025-12-04 | **Spec**: specs/002-intermediate-task-features/spec.md
**Plan**: specs/002-intermediate-task-features/plan.md

## Implementation Strategy

The implementation will follow an incremental approach, prioritizing foundational changes and core user stories first. Each user story will be developed and tested independently where possible. The project's existing structure will be extended to accommodate new features. Test-Driven Development (TDD) will be applied during the implementation of new functionalities and bug fixes.

## Phase 1: Setup

**Goal**: Verify and ensure the basic project structure and core components are in place.

- [X] T001 Ensure `src/models/task.py` exists and is importable.
- [X] T002 Ensure `src/services/task_service.py` exists and is importable.
- [X] T003 Ensure `src/cli/main.py` exists and is importable.
- [X] T004 Ensure `tests/unit/test_task_service.py` exists and is runnable.

## Phase 2: Foundational (Blocking prerequisites for all user stories)

**Goal**: Implement the core data model changes and update the service layer to support priority and tags.

- [X] T005 Update `src/models/task.py` to add `priority` and `tags` attributes to the `Task` class.
- [X] T006 Add validation logic for `priority` in `src/models/task.py`.
- [X] T007 Update `TaskService` in `src/services/task_service.py` to handle persistence and retrieval of `priority` and `tags` for tasks.
- [X] T008 Update `tests/unit/test_task_service.py` to add unit tests for `Task` model changes (priority, tags validation) and `TaskService` persistence of these new attributes.

## Phase 3: User Story 1 - Manage Task Priorities and Tags (P1)

**Goal**: Allow users to assign and view priorities and tags for tasks via the CLI.
**Independent Test**: A user can create a task with a priority and tags, then view the task, confirming the priority and tags are correctly displayed. A user can also update an existing task's priority and tags and verify the changes.

- [X] T009 [US1] Modify the CLI task creation command in `src/cli/main.py` to accept `--priority` and `--tags` arguments.
- [X] T010 [US1] Modify the CLI task update command in `src/cli/main.py` to allow updating `--priority` and `--tags` arguments.
- [X] T011 [US1] Update the task display logic in `src/cli/main.py` to clearly show task priority and tags.
- [X] T012 [US1] Update `tests/unit/test_task_service.py` to add integration tests for CLI interaction with priority and tags in task creation/update.

## Phase 4: User Story 2 - Search and Filter Tasks (P1)

**Goal**: Enable users to search for tasks by keyword and filter by various criteria via the CLI.
**Independent Test**: A user can perform searches and apply various filters (status, priority, tags, due date range) individually and combined, verifying that the task list is correctly narrowed down.

- [X] T013 [US2] Add a search method to `TaskService` in `src/services/task_service.py` to find tasks by keyword in title/description.
- [X] T014 [US2] Add filtering methods to `TaskService` in `src/services/task_service.py` for status, priority, tags, and due date range.
- [X] T015 [US2] Implement logic in `TaskService` in `src/services/task_service.py` to combine multiple filter criteria.
- [X] T016 [US2] Modify the CLI in `src/cli/main.py` to expose search functionality (e.g., `todo search <keyword>`).
- [X] T017 [US2] Modify the CLI in `src/cli/main.py` to expose filtering options (e.g., `todo list --status pending --priority High`).
- [X] T018 [US2] Update `tests/unit/test_task_service.py` with unit tests for search and filter methods in `TaskService`.
- [ ] T019 [US2] Update `tests/unit/test_task_service.py` with integration tests for CLI search and filter commands.

## Phase 5: User Story 3 - Sort Task List (P1)

**Goal**: Provide users with options to sort their task list by due date, priority, or alphabetically via the CLI.
**Independent Test**: A user can apply different sort options (due date, priority, alphabetical) and verify that the task list is reordered correctly according to the selected criteria.

- [ ] T020 [US3] Add sorting methods to `TaskService` in `src/services/task_service.py` for due date, priority, and alphabetical by title.
- [ ] T021 [US3] Modify the CLI in `src/cli/main.py` to expose sorting options (e.g., `todo list --sort due_date asc`).
- [ ] T022 [US3] Update `tests/unit/test_task_service.py` with unit tests for sort methods in `TaskService`.
- [ ] T023 [US3] Update `tests/unit/test_task_service.py` with integration tests for CLI sort commands.

## Phase 6: User Story 4 - Default Priority Display (P2)

**Goal**: Ensure tasks are displayed by priority by default, with custom sorts overriding this.
**Independent Test**: Load the task list without any explicit sort, confirming the default priority order. Then, apply a custom sort and verify it overrides the default.

- [ ] T024 [US4] Implement default sorting by priority (High → Medium → Low) in `src/cli/main.py` when no explicit sort is provided.
- [ ] T025 [US4] Ensure explicit sort commands in `src/cli/main.py` override the default priority sorting.
- [ ] T026 [US4] Update `tests/unit/test_task_service.py` with unit tests for default and overridden sorting logic.

## Final Phase: Polish & Cross-Cutting Concerns

**Goal**: Enhance user experience, update documentation, and ensure code quality across the new features.

- [ ] T027 Review CLI output for all new features to ensure clarity and user-friendliness in `src/cli/main.py`.
- [ ] T028 Update `README.md` with instructions on how to use the new priority, tags, search, filter, and sort features.
- [ ] T029 Ensure all new code adheres to the project's clean code standards (constitution principles).

## Dependency Graph (User Story Completion Order)

The following order represents a logical progression for development:

1.  **Phase 1: Setup** (Blocking for all subsequent phases)
2.  **Phase 2: Foundational** (Blocking for all user story phases)
3.  **Phase 3: User Story 1 (Manage Task Priorities and Tags)**
4.  **Phase 4: User Story 2 (Search and Filter Tasks)**
5.  **Phase 5: User Story 3 (Sort Task List)**
6.  **Phase 6: User Story 4 (Default Priority Display)**
7.  **Final Phase: Polish & Cross-Cutting Concerns**

## Parallel Execution Opportunities

-   **User Story 1 (T009, T010, T011)**: After foundational service changes are complete (T007), CLI modifications for creation, update, and display can be worked on concurrently, as they touch different parts of the `src/cli/main.py` and are relatively independent.
-   **User Story 2 (T013, T014, T015)**: The core search and filtering logic within `TaskService` can be developed in parallel as separate methods.
-   **User Story 2 (T016, T017)**: Once the `TaskService` search and filter methods are stable, their respective CLI integrations can be developed in parallel.
-   **User Story 3 (T020, T021)**: The `TaskService` sorting logic and its CLI integration can be approached with some degree of parallelism.

## Suggested MVP Scope

The Minimum Viable Product (MVP) for this feature set includes **User Story 1: Manage Task Priorities and Tags**. This provides immediate value by allowing users to better organize their tasks with two critical new attributes. This can be followed by User Story 2 and 3 for search/filter/sort, then User Story 4 for default display, and finally polish.
