# AetherVox - AetherPro AI Voice Agent v1.0

Production-grade enterprise voice agent with full AetherOS integration capabilities. Voice-first interface with standalone operation and seamless platform connectivity.

## Overview

AetherVox is an enterprise-grade voice AI agent designed as the foundation for the AetherPro AI ecosystem. It combines:

- **Voice-First Interface**: STT → Intent Detection → Action → TTS workflow
- **Standalone Operation**: Works independently without external dependencies
- **AetherOS Integration**: Full platform connectivity with agent coordination
- **Tool System**: Web search, file operations, code execution, and more
- **Memory Management**: Persistent conversation history and context
- **Real-Time Communication**: WebSocket support for instant interactions

## Architecture

```
AetherVox
├── Backend (FastAPI)
│   ├── Voice Processing (Minimax STT/TTS)
│   ├── Tool System (Web, File, Shell, Code, AetherOS Proxy)
│   ├── Memory Manager (SQLite + JSON)
│   ├── AetherOS Client (REST API)
│   └── Redis Bus (Inter-Agent Pub/Sub)
├── Frontend (React/Vanilla JS)
│   ├── Voice-First UI
│   ├── WebSocket Real-Time Chat
│   └── Status Dashboard
└── Docker
    ├── FastAPI Container
    └── Redis Container
```

## Features

### Voice Capabilities
- Speech-to-Text using Minimax API with confidence scoring
- Text-to-Speech with voice customization and personality
- Web Speech API fallback for browser-native STT
- Low-confidence clarification prompts
- Real-time voice streaming via WebSocket

### Tool System
- **Web Search**: DuckDuckGo integration for web queries
- **File Operations**: Read, write, list files with safety checks
- **Shell Execution**: Sandboxed command execution with whitelisting
- **Code Runner**: Execute Python, JavaScript, and Bash code
- **AetherOS Proxy**: Route tasks to other agents via Redis

### AetherOS Integration
- Agent registration and heartbeat
- Task polling and submission
- Inter-agent communication via Redis pub/sub
- State synchronization
- Graceful fallback to standalone mode

### Memory & Context
- SQLite database for persistent storage
- Conversation history with session management
- User preferences and context
- Task tracking and results
- Importance-based memory prioritization

## Installation

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (recommended)
- Minimax API credentials

### Quick Start with Docker

1. **Clone and setup**:
```bash
cd aethervox
cp .env.example .env
```

2. **Configure environment**:
Edit `.env` and add your Minimax API credentials:
```env
MINIMAX_API_KEY=your_api_key_here
MINIMAX_GROUP_ID=your_group_id_here
```

3. **Run with Docker Compose**:
```bash
docker-compose up -d
```

4. **Access the application**:
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Local Development Setup

1. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Create data directory**:
```bash
mkdir -p data
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run the application**:
```bash
cd backend
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. **Open frontend**:
Open `frontend/index.html` in your browser or serve via:
```bash
cd frontend
python -m http.server 8080
```

## Configuration

### Standalone Mode
For local operation without AetherOS:
```env
AETHEROS_MODE=standalone
```

### Platform Mode
To connect to AetherOS platform:
```env
AETHEROS_MODE=platform
AETHEROS_URL=https://aetheros.yourdomain.com/api
AETHEROS_API_KEY=your_aetheros_api_key
REDIS_ENABLED=true
REDIS_AETHEROS_URL=redis://your-redis-server:6379
```

### Voice Settings
```env
VOICE_CONFIDENCE_THRESHOLD=0.7  # Minimum confidence for STT
TTS_VOICE=male-qn-qingse        # Minimax voice ID
```

## Usage

### Web Interface

1. **Voice Input**:
   - Click the microphone button
   - Speak your request
   - Agent processes and responds with voice

2. **Text Input**:
   - Type in the text box
   - Press Enter or click Send
   - Agent responds with text and optional voice

3. **Quick Commands**:
   - `brief` - Get project summary
   - `dev` - Activate developer mode
   - `search [query]` - Web search
   - `aether-task` - Route to AetherOS

### API Endpoints

#### Health Check
```bash
GET /health
```

#### Speech-to-Text
```bash
POST /api/voice/stt
{
  "audio_data": "base64_encoded_audio",
  "format": "wav",
  "language": "en"
}
```

#### Text-to-Speech
```bash
POST /api/voice/tts
{
  "text": "Hello, I'm AetherVox",
  "voice": "male-qn-qingse",
  "speed": 1.0
}
```

#### Voice Interaction
```bash
POST /api/voice/interact
{
  "audio_data": "base64_encoded_audio",  // or "text": "message"
  "session_id": "unique_session_id"
}
```

#### Execute Tool
```bash
POST /api/tools/execute
{
  "tool_name": "web_search",
  "parameters": {
    "query": "latest AI news",
    "max_results": 5
  }
}
```

### WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/voice');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};

// Send text message
ws.send(JSON.stringify({
  type: 'text',
  text: 'Hello AetherVox'
}));

// Send voice message
ws.send(JSON.stringify({
  type: 'voice',
  audio_data: 'base64_audio'
}));
```

## AetherOS Integration

### Agent Registration
On startup, AetherVox automatically registers with AetherOS:
```json
{
  "agent_id": "voice_agent",
  "agent_type": "voice-specialist",
  "capabilities": ["stt", "tts", "intent_detection", "multi_modal_tasks"],
  "max_concurrent_tasks": 3
}
```

### Task Flow
1. AetherOS assigns task to AetherVox
2. AetherVox polls via `/tasks/poll/voice_agent`
3. Processes task using voice and tools
4. Submits result via `/tasks/{id}/result`

### Inter-Agent Communication
```python
# Route task to another agent
{
  "tool_name": "route_to_agent",
  "parameters": {
    "target_agent": "aletheia",
    "task_description": "Research latest AI trends",
    "task_type": "research"
  }
}
```

Message is published to Redis:
```
Channel: agent:aletheia:inbox
Message: {
  "from_agent": "voice_agent",
  "to_agent": "aletheia",
  "message_type": "task_request",
  "content": {...}
}
```

## Development

### Project Structure
```
aethervox/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── database.py          # SQLite database
│   ├── voice/
│   │   ├── stt.py          # Speech-to-text
│   │   └── tts.py          # Text-to-speech
│   ├── tools/
│   │   ├── web_search.py
│   │   ├── file_ops.py
│   │   ├── shell.py
│   │   ├── code_runner.py
│   │   └── aetheros_proxy.py
│   ├── memory/
│   │   ├── manager.py
│   │   └── schema.py
│   └── aetheros/
│       ├── client.py        # AetherOS API client
│       └── redis_bus.py     # Redis pub/sub
├── frontend/
│   ├── index.html
│   └── app.js
├── data/                    # SQLite database and files
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

### Adding New Tools

1. Create tool module in `backend/tools/`:
```python
async def my_new_tool(param1: str, param2: int) -> Dict:
    """Tool description"""
    try:
        # Implementation
        return {
            "success": True,
            "result": "..."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

2. Register in `backend/tools/__init__.py`

3. Add to tool execution in `backend/main.py`

### Adding Memory Types

1. Define in `backend/memory/schema.py`:
```python
@staticmethod
def create_my_memory(session_id: str, data: Dict) -> Dict[str, Any]:
    return {
        "session_id": session_id,
        "type": MemoryType.MY_TYPE,
        "content": data,
        "importance": MemoryImportance.MEDIUM
    }
```

2. Use in `memory/manager.py`

## Testing

### Local Testing
```bash
# Backend
cd backend
pytest  # If tests are added

# Manual API testing
curl http://localhost:8000/health
```

### Docker Testing
```bash
docker-compose up -d
docker-compose logs -f aethervox
```

### WebSocket Testing
Use browser console or tools like `wscat`:
```bash
npm install -g wscat
wscat -c ws://localhost:8000/ws/voice
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG=false`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure production `AETHEROS_URL` and `AETHEROS_API_KEY`
- [ ] Set up persistent volume for `/app/data`
- [ ] Configure CORS for production domains
- [ ] Enable HTTPS/WSS
- [ ] Set up monitoring and logging
- [ ] Configure Redis password

### Environment Variables for Production
```env
DEBUG=false
SECRET_KEY=use-a-secure-random-string-here
AETHEROS_MODE=platform
AETHEROS_URL=https://aetheros.production.com/api
AETHEROS_API_KEY=prod_key_here
REDIS_ENABLED=true
REDIS_AETHEROS_URL=redis://:password@redis-server:6379
```

### Scaling
- Use Redis for distributed task queue
- Deploy multiple AetherVox instances behind load balancer
- Use external PostgreSQL instead of SQLite for production
- Implement caching layer (Redis)

## Troubleshooting

### Common Issues

**WebSocket Connection Failed**
- Check firewall allows port 8000
- Ensure WebSocket upgrade headers are allowed
- Verify CORS settings

**Voice Recognition Not Working**
- Use Chrome, Edge, or Safari (Firefox has limited support)
- Allow microphone permissions
- Check HTTPS requirement for production

**AetherOS Connection Failed**
- Verify `AETHEROS_URL` is correct
- Check `AETHEROS_API_KEY` is valid
- Ensure network connectivity
- Check AetherOS platform is running

**Redis Connection Error**
- Verify Redis is running: `docker-compose ps`
- Check `REDIS_AETHEROS_URL` is correct
- Ensure Redis port 6379 is accessible

### Logs
```bash
# Docker logs
docker-compose logs -f aethervox

# Application logs (local)
tail -f logs/aethervox.log
```

## Security

- API keys stored in environment variables only
- File operations restricted to allowed directories
- Shell commands whitelisted with blocklist for dangerous operations
- WebSocket authentication (implement JWT for production)
- SQL injection protection via parameterized queries
- Input validation on all endpoints

## License

Proprietary - AetherPro Technologies LLC

## Support

For issues, questions, or feature requests, contact the AetherPro development team.

---

**AetherPro AI Voice Agent v1.0 - Powered by AetherGrid/AetherOS**

Built with enterprise ambitions. Ready to scale.
