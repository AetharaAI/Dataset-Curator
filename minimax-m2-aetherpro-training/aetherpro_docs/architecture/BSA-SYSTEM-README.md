# Business Strategist Agent (BSA) System

An enterprise-grade, production-ready multi-agent system that translates high-level business vision into actionable, investor-ready roadmaps, milestone tracking, and funding paths.

## Overview

The BSA System is a comprehensive platform featuring 6 specialized AI agents that work together to provide strategic business guidance, financial modeling, legal structuring, grant opportunities, operational planning, and investor communications.

## System Architecture

### Core Components

- **FastAPI Backend**: Modular routers for each agent/specialist
- **PostgreSQL Database**: Comprehensive schema for structured data
- **Redis Pub/Sub**: Async communication between agents
- **Vector Database (Chroma)**: Semantic search and document retrieval
- **React Frontend**: Modern UI with TypeScript and responsive design
- **Docker Containers**: Production-ready containerization

### Specialized Agents

1. **Finance Agent**: Financial modeling, cap table scenarios, SPV depreciation, IRR/MoM calculations
2. **Legal/Structuring Agent**: SPV templates, entity structure guidance, compliance checklists
3. **Grants & Incentives Agent**: Opportunity matching, application generation, deadline tracking
4. **Ops/Infra Agent**: Vendor management, BOM generation, infrastructure planning, permits
5. **Pitch/Comms Agent**: Investor presentations, one-pagers, due diligence preparation
6. **Form Filling Agent**: Automated form completion, document assembly, compliance paperwork

## Quick Start

### Prerequisites

- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (for local development)
- Python 3.11+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bsa-system
```

2. Create environment file:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. Start with Docker Compose:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3013
- API Documentation: http://localhost:8018/api/v1/docs
- Backend Health: http://localhost:8018/health

### Development Setup

#### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Features

### Multi-Agent Coordination

The BSA Orchestrator coordinates multiple specialized agents using an event-driven architecture:

- **Intake Pipeline**: Request analysis and intent classification
- **Context Retrieval**: Hybrid memory system (vector + structured)
- **Agent Routing**: Dynamic task delegation based on intent
- **Parallel Execution**: Async task processing when possible
- **Audit Logging**: Immutable logs for all major decisions

### Business Capabilities

#### Funding Route Analysis
```
"Generate 3 funding routes for a $500k GPU data center build"
```
Returns detailed analysis of:
- Venture Capital path
- SPV structure
- Blended grants + angels approach

#### SPV Formation
```
"Form fill SPV formation documents with current company data"
```
Generates complete package:
- Certificate of Formation
- Operating Agreement
- Subscription Agreement
- Private Placement Memorandum
- Form D filing documents

#### Grant Opportunities
```
"Create grant application checklist for DOE Energy Efficiency program"
```
Provides:
- Eligibility assessment
- Application requirements
- Timeline and effort estimates
- Success factors

#### Infrastructure Planning
```
"Generate BOM for GPU data center with 8 A100 GPUs"
```
Delivers:
- Detailed bill of materials
- Vendor recommendations
- Cost estimates
- Procurement timeline

## API Documentation

### Authentication Endpoints

#### POST /api/v1/auth/register
Register a new user

#### POST /api/v1/auth/login
Login and receive JWT tokens

#### GET /api/v1/auth/me
Get current user information

### Chat Endpoints

#### POST /api/v1/chat/message
Send message to BSA and get response

**Request:**
```json
{
  "message": "Generate 3 funding routes for $500k infrastructure",
  "session_id": "optional-session-id",
  "context": {}
}
```

**Response:**
```json
{
  "response": { /* Agent response data */ },
  "session_id": "uuid",
  "timestamp": "2025-11-05T12:00:00",
  "agent_used": "finance"
}
```

#### GET /api/v1/chat/history/{session_id}
Get chat history for a session

#### GET /api/v1/chat/capabilities
Get system capabilities and agent information

### Roadmap Endpoints

#### POST /api/v1/roadmaps/
Create a new roadmap

#### GET /api/v1/roadmaps/
List all roadmaps for user's company

#### GET /api/v1/roadmaps/{roadmap_id}
Get specific roadmap with milestones and tasks

#### PUT /api/v1/roadmaps/{roadmap_id}
Update a roadmap

## Database Schema

### Core Tables

- **users**: User accounts with RBAC
- **companies**: Company/organization information
- **roadmaps**: Strategic roadmaps
- **milestones**: Roadmap milestones with gating criteria
- **tasks**: Task breakdown for milestones
- **financial_scenarios**: Financial modeling data
- **grant_opportunities**: Grant tracking and applications
- **documents**: Generated documents and files
- **audit_logs**: Immutable audit trail
- **chat_history**: Conversation history

## Security Features

- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- Human-in-the-loop gating for sensitive outputs
- Immutable audit logging
- Request validation and sanitization

## Example Use Cases

### 1. Startup Funding Planning

User: "Generate 3 funding routes for a $500k GPU data center build"

BSA analyzes and returns:
- VC Series A route (20% dilution, 6 months)
- SPV structure (15% dilution, 4 months)
- Blended grants + angels (10% dilution, 8 months)

Each route includes:
- Structure details
- Pros and cons
- Milestone timeline
- Cost estimates
- Success probability

### 2. SPV Formation

User: "Form fill SPV formation documents"

BSA generates complete package:
- Certificate of Formation (Delaware LLC)
- Operating Agreement with waterfall structure
- Subscription Agreement template
- Private Placement Memorandum outline
- Form D filing checklist

### 3. Grant Application

User: "Find grants for renewable energy data center"

BSA returns:
- DOE EERE grant ($250k-$2M, 90 day deadline)
- State Economic Development grant ($100k-$500k, 60 days)
- NSF SBIR ($256k, 120 days)

With detailed eligibility, requirements, and success factors.

### 4. Investor Presentation

User: "Prep investor presentation with cap table"

BSA creates:
- 12-slide investor deck structure
- Cap table with dilution analysis
- Financial projections
- Due diligence checklist
- Pitch delivery guide

## Monitoring and Operations

### Health Checks

```bash
curl http://localhost:8018/health
```

### Logs

- Application logs: `docker-compose logs backend`
- Database logs: `docker-compose logs postgres`
- Redis logs: `docker-compose logs redis`

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Production Deployment

### Environment Variables

Set these in production:

```
SECRET_KEY=<strong-random-key>
DATABASE_URL=<production-db-url>
REDIS_URL=<production-redis-url>
OPENAI_API_KEY=<your-key>
ENVIRONMENT=production
DEBUG=False
```

### Kubernetes Deployment

Kubernetes configurations are provided in `/kubernetes` directory:

```bash
kubectl apply -f kubernetes/
```

## Development Guidelines

### Adding a New Agent

1. Create agent class in `backend/app/agents/`
2. Inherit from `BaseAgent`
3. Implement `process()` method
4. Register in orchestrator
5. Add API routes if needed

### Adding API Endpoints

1. Create router in `backend/app/api/routers/`
2. Define Pydantic schemas in `backend/app/schemas/`
3. Register router in `main.py`

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
docker-compose -f docker-compose.test.yml up
```

## License

Proprietary - All rights reserved

## Support

For support, email support@bsa-system.com or open an issue in the repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Changelog

### Version 1.0.0 (2025-11-05)
- Initial release
- 6 specialized agents
- Complete API implementation
- React frontend with chat interface
- Docker containerization
- PostgreSQL + Redis + Chroma integration
