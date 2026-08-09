<!-- GENERATED FILE — edit data/entries.tsv and run `python3 scripts/build_readme.py`, do not edit sections below by hand. -->

# Awesome Self-Hosted AI

> Open-source, self-hostable replacements for AI SaaS tools — **machine-checked**.
> Most awesome lists rot. This one can't: CI re-validates every entry weekly,
> flags anything dead, archived, or without a commit in the last 12 months,
> and opens an issue automatically.

[![CI](https://github.com/sophie-nguyenthuthuy/awesome-selfhosted-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/sophie-nguyenthuthuy/awesome-selfhosted-ai/actions/workflows/ci.yml)
[![Weekly health check](https://github.com/sophie-nguyenthuthuy/awesome-selfhosted-ai/actions/workflows/health.yml/badge.svg)](https://github.com/sophie-nguyenthuthuy/awesome-selfhosted-ai/actions/workflows/health.yml)
![Entries](https://img.shields.io/badge/entries-46-blue)

**Adding a tool is a one-line PR** — append one line to
[`data/entries.tsv`](data/entries.tsv) and CI does the rest
(schema check, liveness check, README regeneration).
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Contents

- [Instead of ChatGPT](#instead-of-chatgpt)
- [Instead of the OpenAI API](#instead-of-the-openai-api)
- [Instead of GitHub Copilot](#instead-of-github-copilot)
- [Instead of Cursor and Devin](#instead-of-cursor-and-devin)
- [Instead of Midjourney](#instead-of-midjourney)
- [Instead of ElevenLabs](#instead-of-elevenlabs)
- [Instead of the Whisper API](#instead-of-the-whisper-api)
- [Instead of Pinecone](#instead-of-pinecone)
- [Instead of LangSmith](#instead-of-langsmith)
- [Instead of Zapier](#instead-of-zapier)
- [Instead of Perplexity](#instead-of-perplexity)
- [Instead of Glean](#instead-of-glean)
- [Instead of NotebookLM](#instead-of-notebooklm)

## Instead of ChatGPT

*Chat UIs you run yourself, for local or API-hosted models.*

- **[AnythingLLM](https://github.com/Mintplex-Labs/anything-llm)** — All-in-one desktop and server chat with built-in RAG over your documents
- **[Jan](https://github.com/menloresearch/jan)** — Offline-first desktop assistant that runs open models locally
- **[Khoj](https://github.com/khoj-ai/khoj)** — Personal AI second brain that chats over your notes and documents
- **[LibreChat](https://github.com/danny-avila/LibreChat)** — Multi-provider ChatGPT-style web UI with agents, auth and search
- **[Lobe Chat](https://github.com/lobehub/lobe-chat)** — Polished chat framework with plugins, knowledge base and multi-user support
- **[Open WebUI](https://github.com/open-webui/open-webui)** — Feature-rich web UI for Ollama and OpenAI-compatible backends

## Instead of the OpenAI API

*Inference servers exposing OpenAI-compatible APIs for open models.*

- **[llama.cpp](https://github.com/ggml-org/llama.cpp)** — Plain C/C++ inference for GGUF models with a built-in OpenAI-compatible server
- **[LocalAI](https://github.com/mudler/LocalAI)** — Drop-in OpenAI API replacement running LLMs, TTS and image models
- **[Ollama](https://github.com/ollama/ollama)** — One-command local model runner with a simple HTTP API
- **[SGLang](https://github.com/sgl-project/sglang)** — High-throughput serving engine with fast structured generation
- **[vLLM](https://github.com/vllm-project/vllm)** — High-throughput, memory-efficient LLM serving with PagedAttention

## Instead of GitHub Copilot

*In-editor code completion backed by models you host.*

- **[Continue](https://github.com/continuedev/continue)** — Open-source IDE extension for chat, edit and autocomplete with any model
- **[Tabby](https://github.com/TabbyML/tabby)** — Self-hosted code completion server with IDE integrations

## Instead of Cursor and Devin

*Autonomous and pair-programming coding agents.*

- **[Aider](https://github.com/Aider-AI/aider)** — Terminal pair-programmer that edits your git repo with any LLM
- **[Cline](https://github.com/cline/cline)** — VS Code agent that plans, edits files and runs commands with approval
- **[OpenHands](https://github.com/All-Hands-AI/OpenHands)** — Autonomous development agent platform, formerly OpenDevin
- **[SWE-agent](https://github.com/SWE-agent/SWE-agent)** — Research-grade agent that fixes GitHub issues autonomously

## Instead of Midjourney

*Image generation pipelines you control end to end.*

- **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)** — Node-based diffusion workflow engine with full pipeline control
- **[InvokeAI](https://github.com/invoke-ai/InvokeAI)** — Professional creative studio for Stable Diffusion and FLUX

## Instead of ElevenLabs

*Speech synthesis and voice cloning.*

- **[Chatterbox](https://github.com/resemble-ai/chatterbox)** — Production-grade open TTS with emotion control and voice cloning
- **[Coqui TTS](https://github.com/idiap/coqui-ai-TTS)** — Maintained fork of the classic Coqui toolkit with XTTS voice cloning
- **[Fish Speech](https://github.com/fishaudio/fish-speech)** — Multilingual TTS with strong zero-shot voice cloning
- **[Piper 1](https://github.com/OHF-Voice/piper1-gpl)** — Fast local neural TTS optimized for low-end hardware

## Instead of the Whisper API

*Local transcription, timestamps and diarization.*

- **[faster-whisper](https://github.com/SYSTRAN/faster-whisper)** — CTranslate2 reimplementation of Whisper, up to 4x faster
- **[Speaches](https://github.com/speaches-ai/speaches)** — OpenAI-compatible speech API server for transcription and TTS
- **[whisper.cpp](https://github.com/ggml-org/whisper.cpp)** — Plain C/C++ Whisper inference that runs anywhere
- **[WhisperX](https://github.com/m-bain/whisperX)** — Whisper with word-level timestamps and speaker diarization

## Instead of Pinecone

*Vector databases and similarity search.*

- **[Chroma](https://github.com/chroma-core/chroma)** — Developer-friendly embedded and server vector database
- **[Milvus](https://github.com/milvus-io/milvus)** — Distributed vector database built for billion-scale search
- **[pgvector](https://github.com/pgvector/pgvector)** — Vector similarity search inside Postgres
- **[Qdrant](https://github.com/qdrant/qdrant)** — Rust vector database with filtering and hybrid search
- **[Weaviate](https://github.com/weaviate/weaviate)** — Vector database with hybrid search and built-in vectorizers

## Instead of LangSmith

*Tracing, evals and prompt management for LLM apps.*

- **[Helicone](https://github.com/Helicone/helicone)** — LLM gateway with logging, caching and cost tracking
- **[Langfuse](https://github.com/langfuse/langfuse)** — Traces, evals, prompt management and metrics for LLM apps
- **[OpenLLMetry](https://github.com/traceloop/openllmetry)** — OpenTelemetry-based instrumentation for LLM applications
- **[Phoenix](https://github.com/Arize-ai/phoenix)** — LLM tracing and evaluation platform from Arize

## Instead of Zapier

*Workflow automation and visual LLM app builders.*

- **[Activepieces](https://github.com/activepieces/activepieces)** — Zapier-style automation with AI pieces and MCP support
- **[Dify](https://github.com/langgenius/dify)** — LLM app platform with visual workflows, RAG and agents
- **[Flowise](https://github.com/FlowiseAI/Flowise)** — Drag-and-drop LLM flow builder on LangChain
- **[Langflow](https://github.com/langflow-ai/langflow)** — Visual builder for agentic and RAG pipelines
- **[n8n](https://github.com/n8n-io/n8n)** — Source-available workflow automation with native AI nodes

## Instead of Perplexity

*AI answer engines with web search and citations.*

- **[Morphic](https://github.com/miurla/morphic)** — AI answer engine with a generative UI
- **[Perplexica](https://github.com/ItzCrazyKns/Perplexica)** — AI search that cites the web, backed by SearXNG

## Instead of Glean

*Enterprise search and RAG over your org's documents.*

- **[Onyx](https://github.com/onyx-dot-app/onyx)** — Enterprise search and chat over 40+ connectors, formerly Danswer
- **[RAGFlow](https://github.com/infiniflow/ragflow)** — Deep-document-understanding RAG engine with citations

## Instead of NotebookLM

*Research notebooks grounded in your own sources.*

- **[Open Notebook](https://github.com/lfnovo/open-notebook)** — Notebook research assistant with podcast generation

## How the machine-checking works

- Entries live in [`data/entries.tsv`](data/entries.tsv) — one line per tool. This README is
  generated from it by [`scripts/build_readme.py`](scripts/build_readme.py); CI fails if they drift.
- [`scripts/validate.py`](scripts/validate.py) enforces the schema on every PR.
- [`scripts/check_health.py`](scripts/check_health.py) runs weekly against the GitHub API:
  a repo that 404s, is archived, or has had no push in **12 months** gets reported in an
  auto-filed issue. PRs that add a dead repo fail immediately.

## License

[CC0 1.0](LICENSE) — public domain.
