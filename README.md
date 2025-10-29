# Adopt Streamlit Chat Interface

A professional Streamlit-based chat interface for the [Adopt AI platform](https://www.adopt.ai). Execute platform actions through natural language conversations with an intuitive, user-friendly UI.

## Features

- 🔐 Secure authentication with Adopt credentials
- 💬 Natural language command interface
- 🎨 Organized response formatting with categories
- 🚀 Quick-start action buttons
- 🔄 Optional LLM enhancement via Groq
- 💾 Export chat history
- ⚙️ Customizable settings

## Prerequisites

- Python 3.8+
- [AdoptXchange SDK](https://github.com/adoptai/AdoptXchange) (required dependency)
- Adopt AI account with API credentials
- Platform configuration (e.g., Shiprocket)

## Installation

### 1. Install AdoptXchange SDK

```bash
git clone https://github.com/adoptai/AdoptXchange.git
cd AdoptXchange
poetry install
```

### 2. Install adopt-streamlit

```bash
git clone https://github.com/adoptai/adopt-streamlit.git
cd adopt-streamlit
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
ADOPT_CLIENT_ID=your_client_id_here
ADOPT_CLIENT_SECRET=your_client_secret_here
GROQ_API_KEY=your_groq_key_here  # Optional
```

**Get credentials:** [Adopt Platform](https://www.adopt.ai) → Settings → Profile → Personal Tokens

### 4. Configure Platform Profile

```bash
cp examples/adopt_profile.json.example examples/adopt_profile.json
# Edit with your platform details (base_url, session cookie, etc.)
```

**Get session cookie:** Browser DevTools (F12) → Network → Request Headers → cookie

## Usage

### Running the Application

**Recommended method (from AdoptXchange directory):**
```bash
cd /path/to/AdoptXchange
poetry run streamlit run /path/to/adopt-streamlit/app.py
```

**Alternative (set PYTHONPATH):**
```bash
export PYTHONPATH="/path/to/AdoptXchange:$PYTHONPATH"  # Mac/Linux
# or
$env:PYTHONPATH="C:\path\to\AdoptXchange"  # Windows

streamlit run app.py
```

The app opens at `http://localhost:8501`

### Getting Started

1. Enter your Adopt Client ID and Secret
2. Click **Connect**
3. Use quick-start buttons or type commands:
   - "Show me all the available actions"
   - "Get All Pickup Locations"
   - "Filter orders from last week"

### Demo Mode

Test the UI without credentials:
1. Set `DEMO_MODE = True` in `app.py` (line 33)
2. Enter any credentials to see simulated responses

## Project Structure

```
adopt-streamlit/
├── app.py                          # Main application
├── response_formatter.py           # Response formatting
├── llm_enhancer.py                # LLM enhancement
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
└── examples/
    └── adopt_profile.json.example # Platform config template
```

## Configuration

### LLM Enhancement

Enable conversational responses with Groq:
1. Get API key from [Groq Console](https://console.groq.com)
2. Add `GROQ_API_KEY` to `.env`
3. Enable in app sidebar

### Platform Profile

Example `adopt_profile.json` for Shiprocket:

```json
{
    "base_url": "https://app.shiprocket.in",
    "application_base_url": "https://app.shiprocket.in",
    "workflow_params": {},
    "security_params": {
        "cookie": "your_session_cookie_here",
        "authorization": ""
    }
}
```

**Note:** Session cookies expire (~24 hours). Refresh from browser DevTools when needed.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Required module not found" | Run from AdoptXchange directory or set PYTHONPATH |
| "Profile file not found" | Copy `adopt_profile.json.example` to `adopt_profile.json` |
| "Connection failed" | Verify credentials are correct |
| Cookie-related errors | Refresh session cookie from browser |

## Security

⚠️ **Never commit:**
- `.env` (contains API keys)
- `examples/adopt_profile.json` (contains session cookies)

Both are excluded in `.gitignore` for safety.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Documentation:** [Adopt AI Docs](https://docs.adopt.ai)
- **Issues:** [GitHub Issues](https://github.com/adoptai/adopt-streamlit/issues)
- **Platform:** [Adopt AI](https://www.adopt.ai)

## Acknowledgments

Built by Atishay (IIT Kharagpur) for Adopt AI  
Powered by [Streamlit](https://streamlit.io) | [Adopt AI](https://www.adopt.ai) | [Groq](https://groq.com)

---

**Need help?** Open an [issue](https://github.com/adoptai/adopt-streamlit/issues) or check the [documentation](https://docs.adopt.ai).