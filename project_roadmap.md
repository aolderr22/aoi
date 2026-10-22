# AOI AI Engineering Project Roadmap

**Purpose:** Turn the existing AOI experiment into a well-engineered AI
application while building practical, employer-relevant skills. This
roadmap separates work that belongs in the project from skills to study
independently.

**Guiding principle:** Build in small, verifiable increments. Keep the
app working, test each new capability, and record what you learned. Do
not add a framework just to use it; be able to explain what problem it
solves.

------------------------------------------------------------------------

## Current baseline

The project has demonstrated these building blocks:

-   Python code running locally on a Mac.
-   Azure AI Foundry project/model access using
    `DefaultAzureCredential`.
-   Azure Blob Storage holding a JSON character dataset.
-   FastAPI endpoints, including a character-data endpoint.
-   An MCP server that exposes a `list_characters` tool.
-   A Jupyter notebook that discovers MCP tools and asks a Foundry model
    to use them.

Before expanding the system, verify that the model actually calls the
MCP tool and that the answer is supported by the returned data. A
plausible answer alone does not prove that retrieval occurred.

## Target architecture

A reasonable target is:

``` text
Client / API caller
       |
       v
FastAPI application --------------------> Azure AI Foundry model
       |                                           ^
       |                                           |
       v                                           |
Application/service layer                         |
       |                                           |
       +--> retrieval service --> vector store ----+
       |
       +--> MCP client --> MCP server --> approved tools/APIs
       |
       +--> logging, evaluation, validation, metrics

Azure Blob Storage: source documents / JSON
Configuration and secrets: environment / managed identity / secret store
Deployment: Docker -> Azure Container Apps
Quality gates: tests -> CI pipeline -> deployment
```

This is a target, not a requirement to build every box immediately. In
particular, do not make the API call an MCP server and do not assume
that MCP replaces ordinary REST APIs. They serve different interfaces
and use cases.

------------------------------------------------------------------------

# Part I --- Project roadmap

## Phase 1 --- Stabilize the current MCP prototype

**Goal:** Prove the current end-to-end path works and fails clearly when
a dependency is unavailable.

### Build

-   [ ] Confirm FastAPI `/health` and `/characters` work.
-   [ ] Confirm the MCP endpoint is reachable and `list_tools()`
    discovers `list_characters`.
-   [ ] Call `list_characters` directly from the notebook and inspect
    its returned content.
-   [ ] Run a model question and log whether a function/tool call was
    requested.
-   [ ] Verify that the tool result---not merely model prior
    knowledge---is used in the final answer.
-   [ ] Test invalid tool names, malformed arguments, empty data, and a
    stopped MCP server.
-   [ ] Return clear, non-sensitive errors rather than raw internal
    exceptions to API clients.

### Learn

-   MCP client/server concepts, tool schemas, request/response
    lifecycle.
-   Function calling with the Responses API.
-   Async Python, exceptions, timeouts, and logging.

### Done when

A repeatable test shows the question, selected tool, tool result, and
final answer. Failures are understandable and do not expose secrets.

## Phase 2 --- Make the codebase maintainable

**Goal:** Move reusable application logic out of notebook cells.

### Build

-   [ ] Keep notebooks for exploration and demonstrations, not as the
    only home for business logic.
-   [ ] Separate configuration, Azure clients, Blob data access, AI
    service, API routes, and MCP tools into modules.
-   [ ] Add typed request/response schemas with Pydantic.
-   [ ] Load configuration in one place and validate required settings
    at startup.
-   [ ] Inject dependencies where practical instead of creating cloud
    clients throughout the code.
-   [ ] Add `.env.example` with placeholder values; ensure `.env`,
    credentials, and local caches are ignored by Git.
-   [ ] Pin or constrain dependencies and document the supported Python
    version.
-   [ ] Add a README with setup, run, test, architecture, and
    troubleshooting instructions.

### Learn

-   Python package structure, type hints, Pydantic, dependency
    injection, configuration management.
-   API design, HTTP status codes, idempotency, and backwards
    compatibility.

### Done when

A fresh environment can be set up from the README and run the app
without relying on notebook state or undocumented local configuration.

## Phase 3 --- Add automated tests and quality gates

**Goal:** Make changes safer and demonstrate normal software engineering
discipline.

### Build

-   [ ] Add `pytest` tests for configuration validation and data
    parsing.
-   [ ] Test FastAPI routes with a test client and mocked cloud
    dependencies.
-   [ ] Test the MCP tool contract and its success/error behavior.
-   [ ] Mock model responses for deterministic unit tests; do not
    require live Azure calls for every test.
-   [ ] Add a small opt-in integration test suite that uses real Azure
    resources.
-   [ ] Add formatting/linting and type checks, such as Ruff and
    optionally mypy or Pyright.
-   [ ] Run tests and checks automatically in GitHub Actions on pull
    requests.

### Learn

-   Unit vs. integration vs. end-to-end tests, fixtures, mocks, contract
    tests, CI.
-   How to avoid flaky tests and how to test code that calls
    nondeterministic models.

### Done when

A clean checkout can run local checks, and a failing test prevents a
broken change from being merged.

## Phase 4 --- Build a real retrieval-augmented generation (RAG) pipeline

**Goal:** Retrieve relevant evidence instead of passing the entire
dataset to the model.

### Build

-   [ ] Define a document/record schema and stable IDs for records.
-   [ ] Create an ingestion process that reads source data from Blob
    Storage, validates it, and normalizes it.
-   [ ] Decide how to turn each record into searchable text; preserve
    structured fields and metadata.
-   [ ] Choose an embedding model and generate embeddings.
-   [ ] Start with one vector store; reasonable learning options include
    FAISS for a local prototype or Azure AI Search for an Azure-oriented
    implementation.
-   [ ] Store metadata such as source ID, document title, category, and
    update time.
-   [ ] Retrieve the top relevant records for a question and pass only
    those records to the model.
-   [ ] Return source IDs or citations with answers where possible.
-   [ ] Handle no-result questions by saying the evidence is
    insufficient rather than inventing an answer.
-   [ ] Make ingestion repeatable and avoid duplicating records when it
    runs again.

### Learn

-   Embeddings, vector similarity, chunking, metadata filtering, top-k
    retrieval, hybrid search, reranking.
-   Vector-store trade-offs: local vs. managed, persistence, filtering,
    scaling, operational cost.
-   RAG is a data/retrieval design, not a synonym for every LLM
    application.

### Evaluate

-   [ ] Create a small fixed set of representative questions and
    relevant source records.
-   [ ] Measure whether relevant records appear in the retrieved
    results.
-   [ ] Compare answers with and without retrieval.
-   [ ] Test exact lookups, broad questions, missing information, and
    misleading queries.

### Done when

The app retrieves relevant records for a known test set and can show
where its answers came from. Record the retrieval settings and known
failure cases.

## Phase 5 --- Add evaluation, tracing, and cost awareness

**Goal:** Measure quality and diagnose failures instead of relying on a
few successful demos.

### Build

-   [ ] Create a versioned evaluation dataset with questions, expected
    facts, and expected supporting sources.
-   [ ] Track retrieval quality separately from answer quality.
-   [ ] Record latency, model deployment, token usage where available,
    tool calls, and errors.
-   [ ] Use structured logs and correlation/request IDs across API,
    model, and MCP calls.
-   [ ] Redact secrets and sensitive content from logs.
-   [ ] Compare prompts, retrieval settings, and model deployments using
    the same evaluation set.
-   [ ] Add timeouts, bounded retries for transient errors, and clear
    failure behavior.
-   [ ] Estimate per-request cost and set reasonable limits.

### Learn

-   LLM-as-judge limitations, human review, groundedness, answer
    relevance, retrieval recall/precision.
-   OpenTelemetry concepts and distributed tracing.
-   Latency budgets, token economics, caching, and retry/backoff design.

### Done when

You can explain whether a poor answer came from retrieval, the model,
tool execution, or application logic, using logs and test results.

## Phase 6 --- Introduce LangGraph for explicit workflow orchestration

**Goal:** Learn graph-based stateful workflows only after the simpler
tool-calling loop is understood.

### Build

-   [ ] Reimplement a small, existing workflow in LangGraph rather than
    replacing everything at once.
-   [ ] Define typed state: user question, retrieved evidence, tool
    results, answer, and error/status information.
-   [ ] Add nodes for request validation, retrieval, tool execution,
    answer generation, and final validation.
-   [ ] Add conditional edges for cases such as "evidence found," "call
    a tool," "retry allowed," and "insufficient evidence."
-   [ ] Set recursion/iteration limits to prevent infinite loops.
-   [ ] Add explicit timeouts and error paths.
-   [ ] Compare the LangGraph implementation with the original simpler
    implementation on the same tests.
-   [ ] Add checkpointing or durable state only if the use case benefits
    from resuming workflows.

### Learn

-   Graph state, nodes, edges, conditional routing, reducers,
    checkpointing, interrupts, human approval, and bounded loops.
-   When a normal Python function or simple state machine is sufficient
    versus when LangGraph adds value.
-   Agent workflows should have clear stop conditions and permissions.

### Done when

The graph has documented states and transitions, passes the same
evaluations as the simpler workflow, and is easier to inspect or extend
for a specific reason.

## Phase 7 --- Expand MCP tools safely

**Goal:** Practice tool integration without making the model an
unrestricted operator.

### Build

-   [ ] Add one or two useful read-only tools, such as searching records
    or fetching a record by ID.
-   [ ] Give every tool a narrow purpose, clear description, typed input
    schema, and predictable output.
-   [ ] Validate tool arguments and limit result sizes.
-   [ ] Add timeouts and handle unavailable downstream services.
-   [ ] Keep authentication and authorization in the tool/application
    layer; do not rely on prompt instructions as security controls.
-   [ ] Log which tool ran and whether it succeeded.
-   [ ] If adding write/action tools later, require authorization and
    explicit confirmation for consequential actions.
-   [ ] Document which capabilities are available through REST and which
    are available through MCP, and why.

### Learn

-   MCP transports, discovery, tool contracts, server boundaries,
    authorization, and least privilege.
-   Prompt injection and untrusted tool output; treat retrieved
    documents as data, not instructions.
-   The difference between an agent deciding to call a tool and the tool
    being allowed to perform the action.

### Done when

Each tool has tests, a clear contract, bounded behavior, and only the
permissions it needs.

## Phase 8 --- Add data freshness and ingestion operations

**Goal:** Keep the index and application data consistent as source data
changes.

### Build

-   [ ] Define how updates to Blob Storage trigger or schedule
    ingestion.
-   [ ] Record source version, ingestion time, and processing status.
-   [ ] Handle malformed files and partial failures without silently
    corrupting the index.
-   [ ] Make ingestion idempotent and support reprocessing.
-   [ ] Add deletion/update behavior so stale records do not remain
    searchable.
-   [ ] Document a rebuild/recovery procedure.

### Learn

-   Batch processing, data validation, schema evolution, idempotency,
    event-driven architecture, and data lineage.

### Done when

You can update a source record, reprocess it, and demonstrate that
retrieval reflects the new version.

## Phase 9 --- Containerize and deploy to Azure

**Goal:** Run the service independently of the laptop and notebook.

### Build

-   [ ] Create and test a Docker image locally.
-   [ ] Use a small, reproducible base image and a non-root user where
    practical.
-   [ ] Keep secrets out of the image and source control.
-   [ ] Push the image to Azure Container Registry.
-   [ ] Deploy to Azure Container Apps with health probes, appropriate
    ingress, and a deliberate scaling configuration.
-   [ ] Prefer managed identity and least-privilege role assignments
    where supported.
-   [ ] Configure endpoints and secrets through deployment
    configuration, not hard-coded values.
-   [ ] Verify outbound connectivity to Foundry, Blob Storage, and any
    vector store.
-   [ ] Test the deployed `/health` and question-answering endpoints.
-   [ ] Review logs, resource usage, scaling, and cost; delete unused
    billable resources when finished practicing.

### Learn

-   Docker layers, image tags, environment variables, networking,
    identity, RBAC, ingress, probes, scaling, and cloud troubleshooting.
-   Difference between deploying a web API, an MCP server, and a
    background ingestion job.
-   Kubernetes concepts later; do not add Kubernetes until you can
    identify a requirement that Container Apps cannot meet economically
    or technically.

### Done when

A deployed endpoint can answer a test question using the intended data
path, and you can explain how it authenticates, scales, and is
monitored.

## Phase 10 --- Production-minded security and resilience

**Goal:** Demonstrate that you can think beyond a successful demo.

### Build

-   [ ] Define data sensitivity and access boundaries, even for sample
    data.
-   [ ] Validate and limit request sizes, input lengths, and retrieved
    context.
-   [ ] Add authentication and authorization appropriate to the
    deployment.
-   [ ] Apply rate limits and quotas where appropriate.
-   [ ] Test prompt injection through user inputs and retrieved content.
-   [ ] Avoid executing arbitrary code or unrestricted actions based on
    model output.
-   [ ] Define safe fallback behavior when a model, tool, storage
    service, or vector store fails.
-   [ ] Document known limitations and a basic incident/debugging
    procedure.

### Learn

-   Threat modeling, secrets management, least privilege, tenant/data
    isolation, OWASP guidance for LLM applications, and secure API
    design.

### Done when

The README explains the threat boundaries, permissions, failure
behavior, and remaining risks.

## Phase 11 --- Portfolio polish

**Goal:** Make the project easy for another engineer or hiring manager
to evaluate.

### Build

-   [ ] Write a clear problem statement and architecture overview.
-   [ ] Include a diagram, setup instructions, example
    requests/responses, and test commands.
-   [ ] Explain why you chose the vector store, model interface, MCP,
    and LangGraph (if used).
-   [ ] Include evaluation results and known limitations, not only
    screenshots.
-   [ ] Add a short demo script or recording if useful.
-   [ ] Remove credentials, private endpoints, and unnecessary resource
    identifiers from public files.
-   [ ] Record a few design decisions in Architecture Decision Records
    (ADRs).
-   [ ] Update the project progress log after each milestone.

### Done when

A reviewer can understand the architecture, reproduce the tests, see the
evidence for quality claims, and identify what you personally
implemented.

------------------------------------------------------------------------

# Part II --- Skills to study separately from the project

These are worthwhile even when they do not immediately become features
in AOI. Choose depth based on the kinds of AI engineering jobs you
target.

## A. Python and software engineering

-   [ ] Async Python: coroutines, event loops, cancellation,
    concurrency, and resource cleanup.
-   [ ] Type hints, protocols, dataclasses, Pydantic, and clean module
    boundaries.
-   [ ] Pytest fixtures, mocks, integration tests, and test design.
-   [ ] HTTP, REST, authentication, API versioning, pagination, and
    error contracts.
-   [ ] Git workflows, code review, packaging, dependency locking, and
    CI.
-   [ ] SQL, relational modeling, transactions, and query optimization.

**Practice independently:** Build a small typed Python service with
tests, configuration validation, structured logs, and a CI pipeline.

## B. ML and mathematical foundations

-   [ ] Vectors, matrices, tensors, shapes, broadcasting, and matrix
    multiplication.
-   [ ] Derivatives, partial derivatives, chain rule, gradients, and
    computational graphs.
-   [ ] Loss functions, gradient descent, learning rates, optimizers,
    and regularization.
-   [ ] Probability, statistics, distributions, sampling, and
    uncertainty.
-   [ ] Train/validation/test splits, overfitting, leakage, and metrics.
-   [ ] Neural network forward passes and backpropagation at a
    conceptual and mathematical level.
-   [ ] Transformer attention, embeddings, tokenization, and positional
    information.
-   [ ] Fine-tuning concepts and when not to fine-tune.

**Practice independently:** Implement linear regression and a tiny
neural network with NumPy; compare your gradients with finite-difference
checks. This builds understanding beyond calling hosted models.

## C. LLM application engineering

-   [ ] Tokens, context windows, structured outputs, and prompt design.
-   [ ] Function/tool calling, tool schemas, and tool-result handling.
-   [ ] RAG architecture, chunking, embeddings, hybrid search,
    reranking, and citations.
-   [ ] Evaluation sets, groundedness, retrieval metrics, regression
    testing, and human review.
-   [ ] Conversation state, memory design, summarization, and context
    management.
-   [ ] Caching, batching, streaming, rate limits, retries, and
    cost/latency trade-offs.
-   [ ] Safety, prompt injection, data leakage, and trust boundaries.

**Practice independently:** Compare two chunking strategies and two
retrieval methods on the same fixed evaluation set. Record quality,
latency, and cost rather than relying on intuition.

## D. Agentic systems and orchestration

-   [ ] When to use direct model calls, deterministic workflows, tool
    calling, or agents.
-   [ ] LangGraph state, nodes, edges, conditional routing,
    checkpointing, and interrupts.
-   [ ] MCP client/server lifecycle, tool discovery, schemas, and
    transports.
-   [ ] Multi-agent coordination trade-offs; understand why more agents
    can add latency and failure modes.
-   [ ] Human approval, permission boundaries, loop limits, and recovery
    behavior.
-   [ ] Workflow tracing and replayable test scenarios.

**Practice independently:** Implement the same bounded workflow using
plain Python and LangGraph, then compare complexity, observability, and
failure handling.

## E. Data and search systems

-   [ ] SQL and data modeling.
-   [ ] JSON schema validation and schema evolution.
-   [ ] Data ingestion, normalization, deduplication, and idempotency.
-   [ ] Vector-store fundamentals: indexing, similarity metrics,
    filtering, persistence, and update/delete behavior.
-   [ ] Search concepts: lexical search, vector search, hybrid
    retrieval, reranking, and relevance evaluation.
-   [ ] Batch vs. streaming/event-driven processing.
-   [ ] Data quality, provenance, and freshness.

**Practice independently:** Benchmark a small dataset using keyword
search, vector search, and hybrid search. Record where each succeeds or
fails.

## F. Cloud, deployment, and operations

-   [ ] Linux and shell fundamentals.
-   [ ] Docker images, layers, networking, volumes, and non-root
    execution.
-   [ ] Azure identity, managed identity, RBAC, secrets, and networking.
-   [ ] Azure Container Apps, registry workflows, health probes,
    scaling, and logs.
-   [ ] CI/CD, environment separation, deployment rollback, and
    configuration management.
-   [ ] Observability: logs, metrics, traces, correlation IDs, and
    alerts.
-   [ ] Cost estimation and resource cleanup.
-   [ ] Kubernetes fundamentals after gaining deployment experience with
    a simpler platform.

**Practice independently:** Deploy a small non-AI API first, then deploy
a model-backed API. This separates cloud deployment problems from model
behavior problems.

## G. System design and professional skills

-   [ ] Service boundaries, synchronous vs. asynchronous processing,
    queues, and background jobs.
-   [ ] Reliability, availability, backpressure, rate limiting, and
    graceful degradation.
-   [ ] Caching, consistency, data ownership, and failure isolation.
-   [ ] Threat modeling, access control, auditability, and privacy.
-   [ ] Writing design docs and ADRs.
-   [ ] Explaining trade-offs, estimating costs, reviewing code, and
    communicating limitations.

**Practice independently:** Design a service that ingests documents,
indexes them, answers questions, and supports reprocessing. Explain
bottlenecks, failure modes, security, and scaling choices.

------------------------------------------------------------------------

# Part III --- Suggested learning order

Use this as a flexible sequence, not a deadline-driven schedule.

1.  **Stabilize what exists:** MCP tool calls, FastAPI contracts, tests,
    and logs.
2.  **Strengthen Python engineering:** modules, types, configuration,
    test automation, and CI.
3.  **Build RAG:** ingestion, embeddings, a vector store, citations, and
    a fixed evaluation set.
4.  **Measure quality:** retrieval metrics, answer checks, tracing,
    latency, and cost.
5.  **Learn LangGraph:** reproduce one bounded workflow and compare it
    with plain Python.
6.  **Deploy:** Docker, Azure Container Registry, Azure Container Apps,
    identity, and monitoring.
7.  **Harden the system:** security, limits, error handling, data
    freshness, and recovery.
8.  **Polish the portfolio:** documentation, demo, evaluation evidence,
    and design decisions.
9.  **Continue independent study:** ML math, neural networks,
    transformers, SQL, and system design alongside project work.

A practical learning rhythm is to spend most of a session implementing
and testing one feature, then spend a smaller portion studying the
underlying concept and writing down what you learned.

## Scope control: what not to add yet

-   Do not add multi-agent architecture until a single-agent workflow
    has a clear limitation.
-   Do not add Kubernetes just because it appears in job descriptions;
    first understand Docker and a managed container service.
-   Do not build a custom model or fine-tune one unless the use case and
    evaluation results justify it.
-   Do not call the application "production-ready" merely because it
    runs in Azure.
-   Do not treat a successful answer as proof of quality without
    repeatable evaluation.

## Definition of success

AOI will be a strong learning and portfolio project when you can
demonstrate that it:

1.  Retrieves relevant evidence and identifies its sources.
2.  Uses MCP tools through explicit, validated contracts.
3.  Has tested, maintainable Python and API code.
4.  Measures retrieval and answer quality on a repeatable evaluation
    set.
5.  Has understandable logs, bounded failures, and reasonable cost
    controls.
6.  Is containerized and deployed with secure cloud identity and
    configuration.
7.  Has clear documentation that explains the architecture and its
    trade-offs.

The aim is not to collect the most frameworks. The aim is to demonstrate
that you can design, implement, evaluate, deploy, and explain a reliable
AI application.
