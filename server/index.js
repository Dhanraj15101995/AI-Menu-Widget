import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import OpenAI from 'openai';

dotenv.config();

const PORT = process.env.PORT || 4000;
const app = express();
app.use(cors());
app.use(express.json());

// init client only if key present
const openAIKey = process.env.OPENAI_API_KEY;
const client = openAIKey ? new OpenAI({ apiKey: openAIKey }) : null;

// Dynamic simulate responses based on food type
const getSimulateResponse = (itemName) => {
  const item = itemName.toLowerCase();
  
  // Different descriptions based on food type
  let description = '';
  let combo = '';
  
  if (item.includes('pizza') || item.includes('pasta')) {
    description = `${itemName} — freshly baked with premium ingredients, aromatic herbs, and authentic Italian flavors.`;
    combo = `Pair it with a refreshing Italian Soda!`;
  } else if (item.includes('burger') || item.includes('sandwich')) {
    description = `${itemName} — juicy, perfectly grilled with fresh vegetables and special sauce.`;
    combo = `Add crispy French Fries and a cold drink!`;
  } else if (item.includes('curry') || item.includes('biryani') || item.includes('tikka')) {
    description = `${itemName} — rich, aromatic spices with tender meat and authentic Indian flavors.`;
    combo = `Pair it with fluffy Naan bread and Mango Lassi!`;
  } else if (item.includes('sushi') || item.includes('roll')) {
    description = `${itemName} — fresh, premium fish with perfectly seasoned rice and crisp vegetables.`;
    combo = `Add miso soup and green tea!`;
  } else if (item.includes('salad') || item.includes('bowl')) {
    description = `${itemName} — fresh, crisp vegetables with healthy grains and light dressing.`;
    combo = `Add a protein boost with grilled chicken!`;
  } else if (item.includes('dessert') || item.includes('cake') || item.includes('ice cream')) {
    description = `${itemName} — sweet, indulgent treat made with premium ingredients.`;
    combo = `Pair it with hot coffee or tea!`;
  } else if (item.includes('drink') || item.includes('juice') || item.includes('smoothie')) {
    description = `${itemName} — refreshing, natural flavors with no artificial additives.`;
    combo = `Add a light snack or dessert!`;
  } else {
    // Default response
    description = `${itemName} — delicious, freshly prepared with quality ingredients and authentic flavors.`;
    combo = `Pair it with your favorite beverage!`;
  }
  
  return { description, combos: [combo] };
};

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    openai: client ? 'configured' : 'not configured',
    timestamp: new Date().toISOString()
  });
});

app.post('/api/generate', async (req, res) => {
  try {
    const { itemName, simulate } = req.body;
    
    // Validate input
    if (!itemName || typeof itemName !== 'string') {
      return res.status(400).json({ 
        error: 'itemName is required and must be a string' 
      });
    }

    if (itemName.trim().length === 0) {
      return res.status(400).json({ 
        error: 'itemName cannot be empty' 
      });
    }

    // simulate mode (useful when offline or no API key)
    if (simulate || !client) {
      return res.json(getSimulateResponse(itemName));
    }

    // Enhanced AI prompt for better results
    const system = `You are an expert menu copywriter for a premium restaurant. You create compelling, appetizing descriptions that make customers want to order immediately. You also suggest relevant upsell items that complement the main dish.`;
    
    const userPrompt = `Create an attractive menu description for "${itemName}" (max 30 words) that highlights:
1. Key ingredients and cooking method
2. Taste and texture
3. What makes it special

Then suggest ONE relevant upsell combo that would pair well with this dish.

Return ONLY a JSON object with:
{
  "description": "your menu description here",
  "combo": "your upsell suggestion here"
}`;

    const completion = await client.chat.completions.create({
      model: process.env.OPENAI_MODEL || 'gpt-3.5-turbo',
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: userPrompt }
      ],
      temperature: 0.7,
      max_tokens: 200
    });

    const text = completion.choices?.[0]?.message?.content ?? '';

    if (!text) {
      throw new Error('No response from OpenAI');
    }

    // Try to parse JSON; fallback to naive extraction
    try {
      const parsed = JSON.parse(text);
      const description = parsed.description || '';
      const combo = parsed.combo || parsed.combos || '';
      
      if (!description) {
        throw new Error('No description in response');
      }
      
      return res.json({ description, combos: [combo] });
    } catch (parseErr) {
      // fallback parsing
      const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
      const description = lines[0] || text.slice(0, 120);
      const comboLine = lines.find(l => /pair|add|combo|suggest/i.test(l)) || lines[1] || '';
      const combo = comboLine.replace(/(Combo:|combo:|suggestion:|suggest:)/i,'').trim();
      
      if (!description) {
        throw new Error('Could not extract description from response');
      }
      
      return res.json({ description, combos: [combo] });
    }
  } catch (err) {
    console.error('API Error:', err);
    
    // Handle specific OpenAI errors
    if (err.code === 'insufficient_quota') {
      return res.status(429).json({ 
        error: 'OpenAI quota exceeded. Please try again later.' 
      });
    }
    
    if (err.code === 'invalid_api_key') {
      return res.status(401).json({ 
        error: 'Invalid OpenAI API key. Please check your configuration.' 
      });
    }
    
    return res.status(500).json({ 
      error: 'Request failed', 
      details: err.message 
    });
  }
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`OpenAI configured: ${client ? 'Yes' : 'No'}`);
});
