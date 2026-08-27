# API Documentation

## Authentication
All endpoints require Bearer token except `/auth/register`, `/auth/login`, `/health`.

```
Authorization: Bearer <access_token>
```

## Endpoints

### Auth
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (OAuth2 form)
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Invalidate session
- `GET /api/v1/auth/me` - Get current user
- `GET /api/v1/auth/oauth/google` - Google OAuth URL
- `GET /api/v1/auth/oauth/github` - GitHub OAuth URL
- `GET /api/v1/auth/oauth/microsoft` - Microsoft OAuth URL

### Search
- `POST /api/v1/search/?query=...&search_type=hybrid` - Profile-aware search
- `GET /api/v1/search/suggest?q=...` - Query suggestions
- `POST /api/v1/search/save` - Save search query

### OSINT
- `POST /api/v1/osint/investigate?target=...&target_type=domain` - Start investigation
- `GET /api/v1/osint/reports` - List reports
- `GET /api/v1/osint/reports/{id}` - Get report details

### AI
- `POST /api/v1/ai/chat` - AI chat completion
- `POST /api/v1/ai/analyze` - Content analysis
- `WS /api/v1/ai/ws/chat` - Real-time WebSocket chat

### Skills
- `GET /api/v1/skills/` - List available skills
- `POST /api/v1/skills/{id}/invoke` - Invoke skill agent

### Enterprise
- `GET /api/v1/enterprise/company` - Get company info
- `POST /api/v1/enterprise/teams` - Create team
- `GET /api/v1/enterprise/billing` - Billing status
- `GET /api/v1/enterprise/reports/usage` - Usage analytics
