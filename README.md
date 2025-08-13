# AI Menu Intelligence Widget

A full-stack AI-powered widget that helps restaurant managers auto-generate item descriptions for digital menus using AI, and suggests upsell combos.

## 🎯 Assessment Requirements Met

✅ **Frontend (React)**
- Accepts food item name via simple form
- Uses AI tool to generate menu descriptions  
- Suggests upsell combo items

✅ **Backend Options**
- **Node.js/Express** - JavaScript backend
- **Python/FastAPI** - Python backend (Assessment preferred)
- API endpoint `/generate-item-details` or `/api/generate`
- Receives food item name
- Uses LLM (OpenAI or simulated) to return:
  - Description (max 30 words)
  - Upsell suggestion
- Responds with JSON content

## 🚀 Features

- **AI-Powered Generation** - Real OpenAI integration
- **Simulate Mode** - Works without API key for testing
- **Dynamic Responses** - Smart food type detection
- **Modern UI** - Beautiful, responsive interface
- **Multiple Backends** - Choose Node.js or Python
- **Auto Documentation** - Interactive API docs
- **Error Handling** - Robust error management

## 📁 Project Structure

```
ai-menu-widget/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   └── package.json
├── server/                 # Node.js backend
│   ├── index.js           # Express server
│   ├── package.json
│   └── .env
├── python-backend/         # Python backend
│   ├── main.py            # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   ├── setup.py          # Setup script
│   └── .env
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- **For Node.js Backend**: Node.js (v16 or higher)
- **For Python Backend**: Python 3.8 or higher
- **Frontend**: Node.js (v16 or higher)
- **Optional**: OpenAI API key for AI features

### Option 1: Node.js Backend Setup

1. **Install client dependencies:**
   ```bash
   cd client
   npm install
   ```

2. **Install server dependencies:**
   ```bash
   cd server
   npm install
   ```

3. **Configure environment:**
   ```bash
   # Edit server/.env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   PORT=4000
   ```

4. **Start the application:**
   ```bash
   # Terminal 1 - Backend
   cd server
   npm start
   
   # Terminal 2 - Frontend
   cd client
   npm run dev
   ```

### Option 2: Python Backend Setup (Recommended for Assessment)

1. **Install client dependencies:**
   ```bash
   cd client
   npm install
   ```

2. **Setup Python backend:**
   ```bash
   cd python-backend
   pip install fastapi uvicorn python-dotenv openai pydantic
   ```

3. **Configure environment:**
   ```bash
   # Edit python-backend/.env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   PORT=8000
   ```

4. **Start the application:**
   ```bash
   # Terminal 1 - Python Backend
   cd python-backend
   python main.py
   
   # Terminal 2 - Frontend
   cd client
   npm run dev
   ```

## 🌐 Access Points

### Node.js Backend
- **API**: http://localhost:4000
- **Health Check**: http://localhost:4000/api/health
- **Frontend**: http://localhost:5173

### Python Backend
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Frontend**: http://localhost:5173

## 📚 API Endpoints

### Node.js Backend (`/api/generate`)
```json
POST /api/generate
{
  "itemName": "Paneer Tikka Pizza",
  "simulate": false
}
```

### Python Backend (`/generate-item-details`)
```json
POST /generate-item-details
{
  "item_name": "Paneer Tikka Pizza",
  "simulate": false
}
```

### Response Format
```json
{
  "description": "Freshly baked pizza topped with marinated paneer tikka, aromatic spices, and authentic Indian flavors.",
  "upsell_suggestion": "Pair it with a refreshing Mango Lassi!"
}
```

## 🧪 Testing

### Using the Frontend
1. Open http://localhost:5173
2. Enter a food item name
3. Check "Simulate (no API)" for testing
4. Click "Generate Menu Description"

### Using API Documentation (Python Backend)
1. Open http://localhost:8000/docs
2. Click on `/generate-item-details`
3. Click "Try it out"
4. Enter test data and execute

### Using curl
```bash
# Node.js Backend
curl -X POST http://localhost:4000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"itemName":"Chicken Biryani","simulate":true}'

# Python Backend
curl -X POST http://localhost:8000/generate-item-details \
  -H "Content-Type: application/json" \
  -d '{"item_name":"Chicken Biryani","simulate":true}'
```

## 🎨 Frontend Features

- **Modern UI** - Glass morphism design with gradients
- **Responsive Design** - Works on all devices
- **Example Buttons** - Quick food item suggestions
- **Loading Animations** - Smooth user experience
- **Error Handling** - Clear error messages
- **Success Animations** - Visual feedback

## 🔧 Configuration

### Environment Variables

**Node.js Backend (.env):**
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
PORT=4000
```

**Python Backend (.env):**
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
PORT=8000
```

### Simulate Mode

When `simulate=true` or no OpenAI API key is provided, the system uses pre-defined responses:

- **Pizza/Pasta** → Italian flavors + Italian Soda
- **Burger/Sandwich** → Juicy grilled + French Fries
- **Curry/Biryani/Tikka** → Indian spices + Naan & Lassi
- **Sushi/Roll** → Fresh fish + Miso soup & Green tea
- **Salad/Bowl** → Fresh vegetables + Protein boost
- **Dessert/Cake** → Sweet treats + Coffee/Tea
- **Drinks/Juice** → Natural flavors + Light snack

## 🚀 Quick Start

### Using the Batch File (Windows)
```bash
# Double-click start.bat
# This will start both Node.js backend and frontend
```

### Manual Start
```bash
# Option 1: Node.js Backend
cd server && npm start
cd client && npm run dev

# Option 2: Python Backend (Recommended)
cd python-backend && python main.py
cd client && npm run dev
```

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors:**
   ```bash
   # Node.js
   npm install
   
   # Python
   pip install -r requirements.txt
   ```

2. **Port already in use:**
   ```bash
   # Windows
   taskkill /f /im node.exe
   taskkill /f /im python.exe
   
   # Or change PORT in .env file
   ```

3. **OpenAI API errors:**
   - Check your API key in .env file
   - Use simulate mode for testing: `"simulate": true`

4. **CORS errors:**
   - Ensure frontend URL is in allowed origins
   - Check that both frontend and backend are running

### Health Checks

- **Node.js**: http://localhost:4000/api/health
- **Python**: http://localhost:8000/health

## 📝 Assessment Submission

### Files to Submit

**Frontend:**
- `client/src/App.jsx` - Main React component
- `client/src/components/MenuForm.jsx` - Form component
- `client/src/components/Suggestions.jsx` - Results component

**Backend (Choose One):**
- **Python**: `python-backend/main.py` - FastAPI application
- **Node.js**: `server/index.js` - Express server

**Configuration:**
- `requirements.txt` (Python) or `package.json` (Node.js)
- `.env` files (with API key configuration)

### Key Features Demonstrated

✅ **React Frontend** - Simple form accepting food item names
✅ **AI Integration** - OpenAI API for menu generation
✅ **Upsell Suggestions** - Combo recommendations
✅ **Python Backend** - FastAPI with `/generate-item-details` endpoint
✅ **JSON Response** - Structured API responses
✅ **Error Handling** - Robust error management
✅ **Simulate Mode** - Works without API key

## 📄 License

ISC

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
