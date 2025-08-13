# AI Menu Intelligence Widget - Python Backend

A FastAPI-based backend for the AI Menu Intelligence Widget that generates creative menu descriptions and upsell suggestions using AI.

## 🎯 Assessment Requirements Met

✅ **Frontend (React)**
- Accepts food item name via simple form
- Uses AI tool to generate menu descriptions
- Suggests upsell combo items

✅ **Backend (Python/FastAPI)**
- API endpoint `/generate-item-details`
- Receives food item name
- Uses LLM (OpenAI or simulated) to return:
  - Description (max 30 words)
  - Upsell suggestion
- Responds with JSON content

## 🚀 Features

- **FastAPI Backend** - Modern, fast Python web framework
- **OpenAI Integration** - Real AI-powered menu generation
- **Simulate Mode** - Works without API key for testing
- **Dynamic Responses** - Smart food type detection
- **Auto-generated Documentation** - Interactive API docs
- **CORS Support** - Frontend integration ready
- **Error Handling** - Robust error management

## 📁 Project Structure

```
python-backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── setup.py            # Setup script
├── .env                # Environment variables
└── README.md           # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the backend directory:**
   ```bash
   cd python-backend
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Configure OpenAI API (Optional):**
   - Edit `.env` file
   - Replace `your_openai_api_key_here` with your actual OpenAI API key
   - If no API key, the app will work in simulate mode

### Running the Application

1. **Start the Python backend:**
   ```bash
   python main.py
   ```

2. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

3. **Start the React frontend:**
   ```bash
   cd ../client
   npm run dev
   ```

4. **Open the application:**
   - Frontend: http://localhost:5173

## 📚 API Endpoints

### `POST /generate-item-details`

Generate menu description and upsell suggestion for a food item.

**Request Body:**
```json
{
  "item_name": "Paneer Tikka Pizza",
  "simulate": false
}
```

**Response:**
```json
{
  "description": "Freshly baked pizza topped with marinated paneer tikka, aromatic spices, and authentic Indian flavors.",
  "upsell_suggestion": "Pair it with a refreshing Mango Lassi!"
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "openai_configured": true,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### `GET /`

Root endpoint with API information.

## 🧪 Testing

### Using the Interactive Documentation

1. Open http://localhost:8000/docs
2. Click on `/generate-item-details`
3. Click "Try it out"
4. Enter your test data
5. Click "Execute"

### Using curl

```bash
curl -X POST "http://localhost:8000/generate-item-details" \
     -H "Content-Type: application/json" \
     -d '{"item_name": "Chicken Biryani", "simulate": true}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/generate-item-details",
    json={"item_name": "Margherita Pizza", "simulate": True}
)
print(response.json())
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Server Configuration
PORT=8000
```

### Simulate Mode

When `simulate=true` or no OpenAI API key is provided, the system uses pre-defined responses based on food type:

- **Pizza/Pasta** → Italian flavors + Italian Soda
- **Burger/Sandwich** → Juicy grilled + French Fries
- **Curry/Biryani/Tikka** → Indian spices + Naan & Lassi
- **Sushi/Roll** → Fresh fish + Miso soup & Green tea
- **Salad/Bowl** → Fresh vegetables + Protein boost
- **Dessert/Cake** → Sweet treats + Coffee/Tea
- **Drinks/Juice** → Natural flavors + Light snack

## 🎨 Frontend Integration

The React frontend is configured to work with this Python backend:

- **API Endpoint**: `http://localhost:8000/generate-item-details`
- **Request Format**: `{ item_name: string, simulate: boolean }`
- **Response Format**: `{ description: string, upsell_suggestion: string }`

## 🚀 Deployment

### Local Development

```bash
# Terminal 1 - Backend
cd python-backend
python main.py

# Terminal 2 - Frontend
cd client
npm run dev
```

### Production

1. **Backend Deployment:**
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Frontend Deployment:**
   ```bash
   npm run build
   # Serve the dist folder
   ```

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port already in use:**
   - Change PORT in .env file
   - Or kill existing processes: `taskkill /f /im python.exe`

3. **OpenAI API errors:**
   - Check your API key in .env file
   - Use simulate mode for testing: `"simulate": true`

4. **CORS errors:**
   - Ensure frontend URL is in allowed origins
   - Check that both frontend and backend are running

### Health Check

Visit http://localhost:8000/health to verify the backend is running correctly.

## 📝 License

ISC

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
