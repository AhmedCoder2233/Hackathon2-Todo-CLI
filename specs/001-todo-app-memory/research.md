# Research for Todo App Memory-Based Specification

## Decision: Primary Dependencies

For the initial implementation, no external libraries will be used for core functionality. The standard Python library is sufficient. The `uv` package manager will be used for dependency management as specified in the constitution.

- **Decision**: No external dependencies for core logic.
- **Rationale**: The application is simple enough to be built with the standard library, which reduces complexity and improves portability. External libraries can be added later if needed for features like browser notifications.
- **Alternatives considered**:
    - `rich` for CLI styling: Rejected for now to keep the initial implementation simple.
    - `plyer` for notifications: Rejected as it adds complexity and platform dependencies that are not required for the core functionality.
