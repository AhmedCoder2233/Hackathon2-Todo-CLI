# API Contracts

No specific external API contracts (e.g., OpenAPI, GraphQL schemas) have been generated for the "Add Advanced Features to Todo App" feature at this time.

**Rationale:**

*   **Current Project Scope**: The application is primarily designed as a single-user CLI/desktop tool with in-memory or file-based storage. It does not expose any external APIs or services that would require formal API contract definitions for third-party integration.
*   **Internal Interactions**: Interactions between application components (e.g., CLI parsing to `TaskService` methods) are considered internal and will be governed by the functional requirements, data model, and clean code principles outlined in `spec.md`, `data-model.md`, and the project `constitution.md`.

Should the project evolve to include web services, microservices, or external integrations in the future, this directory would then be utilized to house appropriate API contract specifications.