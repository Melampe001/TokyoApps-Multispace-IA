# 📖 Glossary

Technical terms, acronyms, and concepts used throughout Tokyo-IA documentation.

## A

**Agent**  
A specialized AI assistant powered by an LLM, designed for specific development tasks. Tokyo-IA has five agents: Akira, Yuki, Hiro, Sakura, and Kenji.

**Agent Orchestrator**  
The Python-based system that coordinates multiple agents, manages workflows, and handles inter-agent communication.

**Agent Registry**  
The central database and API that tracks all agents, their capabilities, and performance metrics.

**Akira (侍)**  
Code review and security analysis agent powered by Claude Opus 4.1.

**Anthropic**  
Company that develops Claude LLM models. Used by Akira.

**API**  
Application Programming Interface. Tokyo-IA provides a REST API for programmatic access.

**API Key**  
Authentication credential for accessing LLM provider APIs (Anthropic, OpenAI, etc.).

## B

**Backstory**  
The personality description and background for each agent that guides their behavior and responses.

**Base Agent**  
The parent class that all specialized agents inherit from, providing common functionality.

**Burst**  
The maximum number of requests allowed above the rate limit in a short period.

## C

**CI/CD**  
Continuous Integration/Continuous Deployment. Automated testing and deployment pipeline.

**Claude**  
LLM family developed by Anthropic. Used by Akira (Claude Opus 4.1).

**CodeQL**  
Static analysis tool used for security scanning in CI/CD pipeline.

**Context Window**  
The maximum number of tokens an LLM can process in a single request. Varies by model (128K - 2M tokens).

**CORS**  
Cross-Origin Resource Sharing. Security feature that controls which domains can access the API.

**Cost Optimization**  
Strategies to reduce LLM API costs through prompt engineering, caching, and model selection.

## D

**Database Schema**  
The structure of tables, columns, and relationships in the PostgreSQL database.

**Deployment**  
The process of making Tokyo-IA available in a production environment.

**Docker**  
Containerization platform used to package and run Tokyo-IA.

**Docker Compose**  
Tool for defining and running multi-container Docker applications.

## E

**E2E Testing**  
End-to-End testing. Testing complete user workflows from start to finish.

**Environment Variable**  
Configuration value stored outside the code (e.g., API keys, database URLs).

**ER Diagram**  
Entity-Relationship Diagram. Visual representation of database schema.

## F

**Foreign Key**  
Database constraint that links tables together, ensuring referential integrity.

## G

**Gemini**  
LLM family developed by Google. Used by Sakura (Gemini 3.0 Ultra).

**Go**  
Programming language used for Tokyo-IA's high-performance API server.

**GPT**  
Generative Pre-trained Transformer. LLM architecture used by OpenAI models.

**Groq**  
Company providing fast LLM inference. Used by Hiro for Llama models.

## H

**Health Check**  
Endpoint (usually `/health`) that reports service status.

**Hiro (🛡️)**  
SRE and DevOps agent powered by Llama 4 405B via Groq.

**Horizontal Scaling**  
Adding more instances of a service to handle increased load.

## I

**Integration Testing**  
Testing how different components work together.

**Inter-Agent Communication**  
Messages and data exchange between agents during workflow execution.

## J

**JSONB**  
PostgreSQL's binary JSON data type. Used for flexible metadata storage.

**JWT**  
JSON Web Token. Authentication standard (planned for future release).

## K

**Kenji (🏗️)**  
System architecture agent powered by OpenAI o3.

**Kubernetes (K8s)**  
Container orchestration platform for deploying and scaling containerized applications.

## L

**Latency**  
Time between request and response. Measured in milliseconds.

**LLM**  
Large Language Model. AI model trained on text data (e.g., GPT, Claude, Llama).

**Llama**  
Open-source LLM family developed by Meta. Used by Hiro (Llama 4 405B).

**Load Balancer**  
Distributes incoming requests across multiple server instances.

## M

**Mermaid**  
Diagramming tool that uses text to create diagrams. Used throughout documentation.

**Metrics**  
Performance measurements (latency, tokens, cost, success rate).

**Migration**  
Database schema change script that modifies table structure.

**Mock Agent**  
Simulated agent that returns fake responses without calling LLM APIs. Useful for testing.

**Model**  
The specific LLM used by an agent (e.g., "claude-opus-4.1", "openai-o3").

**Multi-Agent Workflow**  
Task execution involving multiple agents working together.

## O

**o3**  
OpenAI's advanced reasoning model. Used by Yuki and Kenji.

**OpenAI**  
Company that develops GPT models. Used by Yuki and Kenji.

**OpenAPI**  
Standard specification format for REST APIs.

**Orchestration**  
Coordination of multiple agents and tasks to complete complex workflows.

**ORM**  
Object-Relational Mapping. Technique for database interaction using objects.

## P

**Partitioning**  
Dividing large database tables into smaller pieces for better performance.

**Personality**  
The unique character and behavior pattern of each agent.

**PostgreSQL**  
Open-source relational database used by Tokyo-IA.

**Prompt Engineering**  
Crafting effective prompts to get desired responses from LLMs.

**Prometheus**  
Monitoring system and time-series database. Used for metrics collection.

## Q

**Query**  
Database request to retrieve or manipulate data.

**Queue**  
System for managing pending tasks in order.

## R

**Railway**  
Cloud platform recommended for deploying Tokyo-IA.

**Rate Limiting**  
Restricting the number of API requests a client can make.

**Read Replica**  
Copy of database that handles read-only queries, reducing load on primary database.

**Redis**  
In-memory data store used for caching and session management.

**Registry API**  
Go-based REST API server that provides programmatic access to Tokyo-IA.

**REST**  
Representational State Transfer. Architectural style for web APIs.

**Retry Logic**  
Automatic re-attempt of failed operations with exponential backoff.

## S

**Sakura (🌸)**  
Documentation and technical writing agent powered by Gemini 3.0 Ultra.

**Schema**  
Database structure definition including tables, columns, and relationships.

**SDK**  
Software Development Kit. Library for interacting with Tokyo-IA (Python, JS/TS planned).

**Sentry**  
Error tracking and monitoring service.

**Sequence Diagram**  
Visual representation of interactions between components over time.

**Specialty**  
Area of expertise for an agent (e.g., "security", "testing", "documentation").

**SRE**  
Site Reliability Engineering. Hiro's area of expertise.

**SSL/TLS**  
Secure Sockets Layer/Transport Layer Security. Encryption for web traffic.

## T

**Task**  
Single unit of work executed by an agent.

**Temperature**  
LLM parameter controlling randomness (0 = deterministic, 1 = creative).

**Token**  
Unit of text processed by LLMs. Roughly 4 characters or 0.75 words.

**Token Limit**  
Maximum tokens an LLM can process in one request.

## U

**Unit Testing**  
Testing individual functions or components in isolation.

**UUID**  
Universally Unique Identifier. Used for task and workflow IDs.

## V

**Vertical Scaling**  
Increasing resources (CPU, RAM) of existing instances.

**Virtual Environment (venv)**  
Isolated Python environment for managing dependencies.

## W

**Webhook**  
HTTP callback that sends notifications when events occur.

**Workflow**  
Multi-step process involving one or more agents.

**Workflow Type**  
Category of workflow (e.g., "code_review", "new_feature", "deployment").

## X

**XSS**  
Cross-Site Scripting. Security vulnerability that Akira can detect.

## Y

**YAML**  
Human-readable data serialization format. Used for configuration files.

**Yuki (❄️)**  
Test engineering agent powered by OpenAI o3.

---

## Acronyms Quick Reference

| Acronym | Full Form |
|---------|-----------|
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| CI/CD | Continuous Integration/Continuous Deployment |
| CORS | Cross-Origin Resource Sharing |
| CPU | Central Processing Unit |
| DB | Database |
| DSN | Data Source Name |
| E2E | End-to-End |
| ER | Entity-Relationship |
| FK | Foreign Key |
| HTTP | HyperText Transfer Protocol |
| HTTPS | HTTP Secure |
| JSON | JavaScript Object Notation |
| JSONB | JSON Binary (PostgreSQL) |
| JWT | JSON Web Token |
| K8s | Kubernetes |
| LLM | Large Language Model |
| ORM | Object-Relational Mapping |
| PK | Primary Key |
| REST | Representational State Transfer |
| SDK | Software Development Kit |
| SQL | Structured Query Language |
| SRE | Site Reliability Engineering |
| SSL | Secure Sockets Layer |
| TLS | Transport Layer Security |
| TTL | Time To Live |
| UI | User Interface |
| URL | Uniform Resource Locator |
| UUID | Universally Unique Identifier |
| XSS | Cross-Site Scripting |
| YAML | YAML Ain't Markup Language |

---

## LLM Model Reference

| Model | Provider | Context | Best For |
|-------|----------|---------|----------|
| Claude Opus 4.1 | Anthropic | 200K | Code review, analysis |
| OpenAI o3 | OpenAI | 128K | Reasoning, testing, architecture |
| Llama 4 405B | Meta/Groq | 128K | DevOps, cost-effective tasks |
| Gemini 3.0 Ultra | Google | 2M | Documentation, large context |

---

## Common File Extensions

| Extension | Type | Usage |
|-----------|------|-------|
| `.go` | Go source | API server code |
| `.py` | Python source | Agent code |
| `.ts` | TypeScript | Web frontend |
| `.kt` | Kotlin | Android app |
| `.sql` | SQL script | Database schema/queries |
| `.md` | Markdown | Documentation |
| `.yaml/.yml` | YAML config | Configuration files |
| `.json` | JSON data | Data files, configs |
| `.env` | Environment | Environment variables |
| `.toml` | TOML config | Railway, package config |

---

## Database Table Reference

| Table | Purpose |
|-------|---------|
| `agents` | Agent registry and metadata |
| `workflows` | Multi-agent workflow records |
| `agent_tasks` | Individual task execution records |
| `agent_metrics` | Performance time-series data |
| `agent_interactions` | Inter-agent communications |
| `user_sessions` | User session tracking |

---

## Port Reference

| Port | Service |
|------|---------|
| 8080 | Registry API (default) |
| 5432 | PostgreSQL |
| 6379 | Redis (optional) |
| 3000 | Web dashboard (optional) |
| 9090 | Prometheus metrics |

---

*Last updated: 2025-12-23*
