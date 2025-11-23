# Persi - Personal Intelligence Agent

**Cory's Personal Intelligence Agent for Day-to-Day AetherPro Operations**

Persi is an enterprise-grade, always-on AI assistant designed for autonomous and semi-autonomous execution of business operations, system management, and daily workflows.

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- MiniMax API Key

### Installation

1. **Clone and setup:**
```bash
cd ~/projects
git clone [repo-url] persi
cd persi

# Modern way with UV (recommended - 100x faster!)
uv sync

# Or traditional way
python -m venv venv
source venv/bin/activate
pip install -e .
```

2. **Setup PostgreSQL database:**
```bash
# Copy the database setup script
cp setup_postgres_db.sh .
cp .env.template .env

# Edit .env with your database credentials
nano .env

# Run the setup script
chmod +x setup_postgres_db.sh
./setup_postgres_db.sh
```

3. **Configure Persi:**
```bash
# Copy default settings
mkdir -p ~/.persi
cp config/settings.default.json ~/.persi/settings.json

# Edit with your API key and preferences
nano ~/.persi/settings.json
```

4. **Run database migrations:**
```bash
alembic upgrade head
```

5. **Start Persi:**
```bash
# CLI mode
python -m persi chat

# Server mode (for remote access)
python -m persi serve
```

## Features

- **Always-On Access**: Hit Persi from anywhere - work, phone, home
- **Autonomous Execution**: Semi-autonomous and fully autonomous modes
- **Tool Integration**: Shell, file ops, browser control, computer use, voice
- **Business Intelligence**: Project tracking, task management, status reports
- **Agent Coordination**: Delegates to specialist agents (Mini-Flux, Aletheia_Flux, etc.)
- **AetherOS Integration**: Connects to your AetherOS infrastructure
- **Model Agnostic**: Start with MiniMax M2, swap to any model later

## Architecture

See [PERSI_ARCHITECTURE.md](./PERSI_ARCHITECTURE.md) for full technical specification.

## Configuration

### Settings File (~/.persi/settings.json)
```json
{
  "model": {
    "provider": "minimax",
    "name": "MiniMax-M2",
    "api_key_env": "MINIMAX_API_KEY",
    "base_url": "https://api.minimax.io/anthropic"
  },
  "execution_mode": "semi_autonomous",
  "database": {
    "url": "postgresql://persi_user:password@localhost:5432/persi_db"
  },
  "redis": {
    "url": "redis://localhost:6379"
  },
  "tools": {
    "enabled": ["shell", "file", "browser", "computer_use"]
  }
}
```

## Usage Examples

### CLI Mode
```bash
# Start interactive chat
persi chat

# Execute a single command
persi exec "What's the status of AetherInterface?"

# Get project updates
persi projects

# Check tasks
persi tasks
```

### API Mode
```bash
# Start server
persi serve --host 0.0.0.0 --port 8000

# In another terminal
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "Give me an update on all projects"}'
```

## Development

### Project Structure
```
persi/
├── core/           # Core agent logic
├── tools/          # Tool implementations
├── api/            # FastAPI server
├── cli/            # CLI interface
├── config/         # Configuration
├── memory/         # Memory system
├── tests/          # Test suite
├── migrations/     # Alembic migrations
└── scripts/        # Utility scripts
```

### Running Tests
```bash
pytest tests/
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Deployment

### Systemd Service
```bash
# Copy service file
sudo cp persi.service /etc/systemd/system/

# Enable and start
sudo systemctl enable persi
sudo systemctl start persi

# Check status
sudo systemctl status persi
```

### Docker
```bash
docker-compose up -d
```

## Roadmap

- [x] Architecture design
- [ ] Phase 1: Foundation (FastAPI, MiniMax, PostgreSQL, CLI)
- [ ] Phase 2: Core Tools (Shell, Files, Browser, Computer Use)
- [ ] Phase 3: Business Intelligence (Projects, Tasks, Reports)
- [ ] Phase 4: Advanced (Voice, Vision, Agent Coordination)
- [ ] Phase 5: Production (Apriel model, Self-hosted, Multi-user)

## License

Proprietary - AetherPro Technologies LLC

## Contact

Cory - Founder & CEO, AetherPro Technologies LLC
