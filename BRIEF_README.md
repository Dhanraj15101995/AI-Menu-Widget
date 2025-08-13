## AI Menu Intelligence Widget — Brief README

### Tools used
- **Frontend**: React 19, Vite 7, @vitejs/plugin-react, ESLint
- **Backends**:
  - Python: FastAPI, Uvicorn, Pydantic, python-dotenv
  - Node.js (optional alternative): Express, CORS, dotenv, OpenAI SDK
- **AI**: OpenAI API (config via `OPENAI_API_KEY`) with JSON-only output contract
- **Dev/OS**: Windows batch starters (`start-python.bat`, `start.bat`)

### How the prompt was designed
- **Goals**:
  - Generate short (≤30 words), appetizing menu descriptions
  - Provide exactly one complementary upsell suggestion
  - Enforce JSON-only output for reliable parsing
- **Structure**:
  - System prompt defines role, tone, constraints, and output format
  - User prompt template inserts the item name and re-states constraints clearly
  - Backend validates/parses the JSON and falls back to heuristic parsing if needed
- **Iterations**:
  - Added explicit JSON schema in the prompt to reduce formatting drift
  - Implemented `validate_ai_response` to sanitize, truncate, and recover from malformed outputs
  - Added `simulate` mode to work without an API key and during outages

### Steps to run (Windows)
- **Recommended (Python backend + React)**
  1. Create `.env` in `python-backend` (optional for real AI):
     - `OPENAI_API_KEY=your_key_here`
  2. Start both services: double-click `start-python.bat` (or run it in a terminal)
  3. Open the app: `http://localhost:5173`

- **Alternative (Node backend + React)**
  1. Create `.env` in `server` (optional for real AI):
     - `OPENAI_API_KEY=your_key_here`
     - `PORT=4000`
  2. Update `client/src/App.jsx` to call `http://localhost:4000/api/generate`
  3. Start both services: double-click `start.bat`

### Time taken and tradeoffs/assumptions
- **Time taken**: ~1–2 hours for prompt design, backend validation, and integration
- **Tradeoffs**:
  - Chose strict JSON output for simpler parsing; added fallback parsing for robustness
  - Included both Python and Node backends to offer flexibility, at the cost of duplication
  - `simulate` mode trades perfect realism for zero-cost, offline testing
- **Assumptions**:
  - Windows 10+, Node 18+, Python 3.10+
  - React client currently targets the Python backend at `http://localhost:8000`
  - Stable local network; CORS is allowed for `http://localhost:5173`

### Where are the prompts?
- See `PROMPT_USED.txt` in the project root (extracted from `python-backend/main.py` and mirrored from `server/index.js`).
