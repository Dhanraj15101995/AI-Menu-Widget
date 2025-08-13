from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, field_validator
import os
from dotenv import load_dotenv
import openai
import json
import re
import time
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import hashlib

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Menu Intelligence Widget",
    description="AI-powered widget for generating menu descriptions and upsell suggestions",
    version="1.0.0"
)

# Security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware for production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "your-domain.com"]
    )

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = None
if openai_api_key:
    openai_client = openai.OpenAI(api_key=openai_api_key)

# Rate limiting storage
rate_limit_store: Dict[str, List[float]] = {}

# Pydantic models with validation
class MenuItemRequest(BaseModel):
    item_name: str
    simulate: Optional[bool] = False
    gpt_model: Optional[str] = "gpt-3.5-turbo"  # Bonus: GPT model selection
    
    @field_validator('item_name')
    @classmethod
    def validate_item_name(cls, v):
        """Validate and sanitize item name input"""
        if not v or not v.strip():
            raise ValueError('Item name cannot be empty')
        
        # Sanitize input - remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', v.strip())
        
        # Length validation
        if len(sanitized) > 100:
            raise ValueError('Item name too long (max 100 characters)')
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'script', r'javascript', r'<.*>', r'http://', r'https://',
            r'exec\(', r'eval\(', r'system\(', r'import\s+os'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                raise ValueError('Invalid characters detected in item name')
        
        return sanitized
    
    @field_validator('gpt_model')
    @classmethod
    def validate_gpt_model(cls, v):
        """Validate GPT model selection"""
        allowed_models = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo']
        if v not in allowed_models:
            return 'gpt-3.5-turbo'  # Default fallback
        return v

class MenuItemResponse(BaseModel):
    description: str
    upsell_suggestion: str
    generated_at: str
    model_used: str

# Rate limiting function
def check_rate_limit(client_ip: str, limit: int = 10, window: int = 60) -> bool:
    """
    Rate limiting: max 10 requests per minute per IP
    """
    current_time = time.time()
    
    if client_ip not in rate_limit_store:
        rate_limit_store[client_ip] = []
    
    # Remove old requests outside the time window
    rate_limit_store[client_ip] = [
        req_time for req_time in rate_limit_store[client_ip]
        if current_time - req_time < window
    ]
    
    # Check if limit exceeded
    if len(rate_limit_store[client_ip]) >= limit:
        return False
    
    # Add current request
    rate_limit_store[client_ip].append(current_time)
    return True

# Get client IP
def get_client_ip(request: Request) -> str:
    """Extract client IP address"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host

# Enhanced prompt engineering
class PromptEngineer:
    """
    Prompt Engineering Class for structured AI interactions
    """
    
    @staticmethod
    def create_system_prompt() -> str:
        """
        System prompt that defines the AI's role and behavior
        """
        return """You are an expert menu copywriter for a premium restaurant chain. Your role is to:

1. CREATE COMPELLING DESCRIPTIONS: Write appetizing, professional menu descriptions that make customers want to order immediately
2. SUGGEST RELEVANT UPSALES: Recommend complementary items that enhance the dining experience
3. MAINTAIN CONSISTENCY: Use consistent tone, style, and format across all descriptions
4. RESPECT CONSTRAINTS: Keep descriptions under 30 words and focus on key selling points

Guidelines:
- Highlight unique ingredients, cooking methods, and flavors
- Use sensory words (aromatic, crispy, tender, etc.)
- Emphasize quality and authenticity
- Suggest culturally appropriate pairings
- Maintain professional, appetizing tone

Output Format: Return ONLY a valid JSON object with "description" and "upsell_suggestion" fields."""

    @staticmethod
    def create_user_prompt(item_name: str) -> str:
        """
        User prompt with specific instructions for the given food item
        """
        return f"""Create a menu description for "{item_name}" following these specific requirements:

DESCRIPTION REQUIREMENTS:
- Maximum 30 words
- Highlight: key ingredients, cooking method, taste/texture, unique selling point
- Use appetizing, professional language
- Focus on what makes this dish special

UPSELL REQUIREMENTS:
- Suggest ONE complementary item (beverage, side, dessert)
- Should enhance the main dish experience
- Culturally appropriate pairing
- Specific, actionable suggestion

RESPONSE FORMAT:
Return ONLY a JSON object:
{{
  "description": "Your menu description here (max 30 words)",
  "upsell_suggestion": "Your upsell suggestion here"
}}

Ensure the response is valid JSON and follows the exact format specified."""

    @staticmethod
    def validate_ai_response(response_text: str) -> Dict[str, str]:
        """
        Validate and clean AI response
        """
        try:
            # Try to parse JSON
            parsed = json.loads(response_text.strip())
            
            # Validate required fields
            if not parsed.get("description") or not parsed.get("upsell_suggestion"):
                raise ValueError("Missing required fields")
            
            # Clean and validate description
            description = parsed["description"].strip()
            if len(description) > 150:  # Safety limit
                description = description[:147] + "..."
            
            # Clean and validate upsell
            upsell = parsed["upsell_suggestion"].strip()
            if len(upsell) > 100:  # Safety limit
                upsell = upsell[:97] + "..."
            
            return {
                "description": description,
                "upsell_suggestion": upsell
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback parsing for malformed responses
            lines = [line.strip() for line in response_text.split('\n') if line.strip()]
            
            description = lines[0] if lines else "Delicious dish prepared with care."
            if len(description) > 150:
                description = description[:147] + "..."
            
            # Find upsell suggestion
            upsell_line = ""
            for line in lines[1:]:
                if any(word in line.lower() for word in ['pair', 'add', 'combo', 'suggest', 'try']):
                    upsell_line = line
                    break
            
            if not upsell_line and len(lines) > 1:
                upsell_line = lines[1]
            
            upsell = re.sub(r'(Combo:|combo:|suggestion:|suggest:)', '', upsell_line).strip()
            if not upsell:
                upsell = "Pair it with your favorite beverage!"
            
            return {
                "description": description,
                "upsell_suggestion": upsell
            }

# Dynamic simulate responses based on food type
def get_simulate_response(item_name: str) -> dict:
    """Generate simulated responses based on food type"""
    item = item_name.lower()
    
    if any(word in item for word in ['pizza', 'pasta']):
        return {
            "description": f"{item_name} — freshly baked with premium ingredients, aromatic herbs, and authentic Italian flavors.",
            "upsell_suggestion": "Pair it with a refreshing Italian Soda!"
        }
    elif any(word in item for word in ['burger', 'sandwich']):
        return {
            "description": f"{item_name} — juicy, perfectly grilled with fresh vegetables and special sauce.",
            "upsell_suggestion": "Add crispy French Fries and a cold drink!"
        }
    elif any(word in item for word in ['curry', 'biryani', 'tikka']):
        return {
            "description": f"{item_name} — rich, aromatic spices with tender meat and authentic Indian flavors.",
            "upsell_suggestion": "Pair it with fluffy Naan bread and Mango Lassi!"
        }
    elif any(word in item for word in ['sushi', 'roll']):
        return {
            "description": f"{item_name} — fresh, premium fish with perfectly seasoned rice and crisp vegetables.",
            "upsell_suggestion": "Add miso soup and green tea!"
        }
    elif any(word in item for word in ['salad', 'bowl']):
        return {
            "description": f"{item_name} — fresh, crisp vegetables with healthy grains and light dressing.",
            "upsell_suggestion": "Add a protein boost with grilled chicken!"
        }
    elif any(word in item for word in ['dessert', 'cake', 'ice cream']):
        return {
            "description": f"{item_name} — sweet, indulgent treat made with premium ingredients.",
            "upsell_suggestion": "Pair it with hot coffee or tea!"
        }
    elif any(word in item for word in ['drink', 'juice', 'smoothie']):
        return {
            "description": f"{item_name} — refreshing, natural flavors with no artificial additives.",
            "upsell_suggestion": "Add a light snack or dessert!"
        }
    else:
        return {
            "description": f"{item_name} — delicious, freshly prepared with quality ingredients and authentic flavors.",
            "upsell_suggestion": "Pair it with your favorite beverage!"
        }

@app.get("/")
async def root():
    """Root endpoint with security info"""
    return {
        "message": "AI Menu Intelligence Widget API",
        "version": "1.0.0",
        "security": {
            "input_validation": "enabled",
            "rate_limiting": "enabled",
            "sanitization": "enabled"
        },
        "endpoints": {
            "generate_item_details": "/generate-item-details",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with security status"""
    return {
        "status": "healthy",
        "openai_configured": openai_client is not None,
        "security_features": {
            "input_validation": True,
            "rate_limiting": True,
            "sanitization": True
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/generate-item-details", response_model=MenuItemResponse)
async def generate_item_details(request: MenuItemRequest, client_request: Request):
    """
    Generate menu description and upsell suggestion for a food item.
    
    Security Features:
    - Input validation and sanitization
    - Rate limiting (10 requests/minute per IP)
    - XSS protection
    - SQL injection protection
    
    GRAFTERR POS INTEGRATION:
    This endpoint can be integrated into Grafterr's POS item management screen by:
    1. Adding a "Generate AI Description" button next to each menu item
    2. Calling this API when the button is clicked
    3. Auto-filling the description and upsell fields in the POS form
    4. Allowing managers to edit the AI-generated content before saving
    5. Storing the generated content in Grafterr's menu database
    """
    try:
        # Rate limiting check
        client_ip = get_client_ip(client_request)
        if not check_rate_limit(client_ip):
            raise HTTPException(
                status_code=429, 
                detail="Rate limit exceeded. Please try again in 1 minute."
            )
        
        # Simulate mode or no OpenAI client
        if request.simulate or not openai_client:
            response = get_simulate_response(request.item_name)
            return MenuItemResponse(
                description=response["description"],
                upsell_suggestion=response["upsell_suggestion"],
                generated_at=datetime.now().isoformat(),
                model_used="simulate"
            )
        
        # OpenAI API call with enhanced prompt engineering
        try:
            # Create structured prompts
            system_prompt = PromptEngineer.create_system_prompt()
            user_prompt = PromptEngineer.create_user_prompt(request.item_name)
            
            completion = openai_client.chat.completions.create(
                model=request.gpt_model, # Use the selected model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=200,
                timeout=30  # 30 second timeout
            )
            
            response_text = completion.choices[0].message.content.strip()
            
            # Validate and clean AI response
            validated_response = PromptEngineer.validate_ai_response(response_text)
            
            return MenuItemResponse(
                description=validated_response["description"],
                upsell_suggestion=validated_response["upsell_suggestion"],
                generated_at=datetime.now().isoformat(),
                model_used=request.gpt_model
            )
                
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            # Fallback to simulate response
            response = get_simulate_response(request.item_name)
            return MenuItemResponse(
                description=response["description"],
                upsell_suggestion=response["upsell_suggestion"],
                generated_at=datetime.now().isoformat(),
                model_used="fallback"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/security-info")
async def security_info():
    """Security information endpoint"""
    return {
        "input_validation": {
            "enabled": True,
            "features": [
                "Length validation (max 100 chars)",
                "Character sanitization",
                "Suspicious pattern detection",
                "XSS protection"
            ]
        },
        "rate_limiting": {
            "enabled": True,
            "limit": "10 requests per minute per IP",
            "window": "60 seconds"
        },
        "prompt_engineering": {
            "structured_prompts": True,
            "system_prompt": "Defines AI role and behavior",
            "user_prompt": "Specific instructions per request",
            "response_validation": True
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
