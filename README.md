# PhD Xpert Solver - AI-Powered OSINT Search Browser

> The world's first AI-native search browser built for intelligence professionals, enterprises, and power users. Combines multi-model AI orchestration, real-time OSINT, user-profile-aware search, and enterprise-grade security.

## Architecture

```
phdxpert-browser/
├── frontend/          # Next.js 14 + React 18 + Tailwind + Framer Motion
├── backend/           # FastAPI + Python 3.11 + AsyncIO
├── osint/             # Open Source Intelligence engines & modules
├── ai_models/         # Multi-provider AI orchestration (GPT-4o, Claude, Gemini, Local)
├── auth/              # Identity, SSO, MFA, WebAuthn, RBAC
├── search/            # Elasticsearch + Vector + Graph hybrid search
├── skills/            # Reusable AI skill templates & workflows
├── enterprise/        # Billing, teams, reports, integrations
├── docker/            # Container orchestration
├── k8s/               # Kubernetes manifests
└── docs/              # Full documentation
```

## Core Features

- **Profile-Aware Search**: Every search is contextualized by user profile (company, role, industry, preferences)
- **Multi-Model AI**: GPT-4o, Claude 3.5, Gemini 1.5, Ollama local models with automatic routing
- **OSINT Suite**: 50+ intelligence gathering modules (Shodan, Censys, VirusTotal, social media, dark web)
- **Skill Templates**: Pre-built AI workflows for legal, finance, security, research, healthcare
- **Enterprise SSO**: SAML, OIDC, OAuth2, WebAuthn/FIDO2, SCIM provisioning
- **Real-time Graph**: Neo4j-powered relationship mapping for OSINT findings
- **Vector Search**: pgvector + Weaviate hybrid semantic search
- **Agent Teams**: CrewAI-powered multi-agent research teams

## Quick Start

```bash
# Clone and setup
git clone https://github.com/phdxpert/phdxpert-browser.git
cd phdxpert-browser

# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Or local dev
conda env create -f environment.yml
conda activate phdxpert
pip install -r backend/requirements.txt
cd frontend && npm install && npm run dev
cd ../backend && uvicorn app.main:app --reload
```

## License
MIT License - See LICENSE file
