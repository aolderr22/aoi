# AOI Project Roadmap

## Goal
Build a practical AI engineering project demonstrating RAG, tool integration, agent orchestration, evaluation, and deployment with Python and Azure.

## Current Baseline
- Azure AI Foundry model access from Python
- Character JSON stored in Azure Blob Storage
- FastAPI endpoints for health, character data, and questions
- MCP server exposing a character-retrieval tool
- Notebook connecting the model to MCP tools

**Terminology:** The current MCP workflow is retrieval-augmented in a broad sense because it supplies external data to the model. It is not yet conventional **vector RAG**, which embeds data and retrieves semantically relevant records.

## Project Milestones

### 1. Build a Small Vector RAG Pipeline
- Load and normalize the character JSON.
- Convert each character into a useful text document.
- Generate embeddings and store them in local FAISS.
- Retrieve the top relevant records for each question.
- Send retrieved context to the Foundry model and ground the answer in that context.

**Complete when:** The system retrieves relevant records instead of passing the entire dataset to the model.

### 2. Add LangGraph
- Represent the question-answering flow as a small graph.
- Add retrieval and answer-generation nodes.
- Add a decision or retry path only if it provides value.
- Keep the existing MCP tool as a separate data-access option.

**Complete when:** The graph runs end-to-end and each step is understandable and testable.

### 3. Evaluate and Compare
- Compare the existing MCP approach, basic vector RAG, and LangGraph RAG.
- Create representative test questions and identify the evidence expected for each.
- Check retrieval relevance, answer correctness, evidence quality, latency, and cost.
- Record failures and improve the weakest part.

**Complete when:** Repeatable tests show where each approach succeeds or fails.

### 4. Improve Maintainability
- Separate configuration, data access, retrieval, graph logic, and API routes.
- Add tests for data loading, retrieval, and key API behavior.
- Handle missing data, model errors, and malformed requests.
- Keep secrets out of source control.

**Complete when:** The core workflow can be tested locally without manual notebook steps.

### 5. Deploy and Document
- Containerize the application with Docker.
- Deploy to Azure Container Apps once the local version is stable.
- Configure identity and permissions securely.
- Document architecture, setup, sample questions, evaluation results, and limitations in the README.

**Complete when:** Another developer can run and evaluate the project using the documentation.

## Parallel Learning Track: PyTorch
Keep PyTorch as a separate learning exercise, not an AOI dependency for now.

1. Practice tensor shapes, indexing, and arithmetic.
2. Use autograd to calculate gradients.
3. Train a tiny neural network with a loss function and optimizer.
4. Connect these concepts to how pretrained embedding models support semantic search.

Use an existing embedding model for RAG. Do not train a custom embedding model just to add complexity.

## Suggested Order
**Vector RAG → LangGraph → evaluation → refactoring and tests → deployment.**

Work in small increments, commit each working milestone, and keep the scope focused on reliable AI application engineering rather than adding tools for their own sake.