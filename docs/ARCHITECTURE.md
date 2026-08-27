# PhD Xpert Solver - Architecture

## System Design

### Core Principle: Profile-Aware Intelligence
Every search query, AI response, and OSINT investigation is contextualized by the logged-in user's profile:
- **Identity**: Email, phone, verified status
- **Organization**: Company, department, job title, team
- **Role**: Admin, Manager, Analyst, User, Guest
- **Preferences**: Industry, domains, search history, saved queries
- **Subscription**: Tier, quota, features

### Data Flow
1. User authenticates (OAuth2/SAML/MFA/WebAuthn)
2. Profile context is loaded into session
3. Search query is enriched with user context
4. Hybrid search engine routes to ES/Vector/Graph
5. Results are re-ranked by profile relevance
6. AI model auto-selected based on complexity + role
7. Response is tailored to user's department/role
8. All activity logged for enterprise audit

### Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, Tailwind, Framer Motion |
| Backend | FastAPI, Python 3.11, AsyncIO |
| Auth | JWT, OAuth2, SAML, WebAuthn, RBAC |
| Databases | PostgreSQL+pgvector, Redis, ES, Neo4j, Weaviate |
| AI | GPT-4o, Claude 3.5, Gemini 1.5, Ollama, CrewAI |
| OSINT | Shodan, Censys, VirusTotal, DNS, WHOIS |
| Infra | Docker, K8s, Grafana, Prometheus |
