from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import logging
from datetime import datetime
import google.generativeai as genai
from typing import Dict, Any, List
from dotenv import load_dotenv
from prompt_manager import get_formatted_prompt, get_prompt_info

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Swiggy Chatbot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("Warning: GEMINI_API_KEY not found. Please set the environment variable.")
    model = None

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    data_used: Dict[str, Any] = None

# In-memory database
db = {
    "inventory": [
        {"item_name": "Burger", "quantity_left": 24, "unit_price": 120},
        {"item_name": "Pizza", "quantity_left": 10, "unit_price": 250},
        {"item_name": "Fries", "quantity_left": 40, "unit_price": 60},
        {"item_name": "Sandwich", "quantity_left": 15, "unit_price": 90},
        {"item_name": "Pasta", "quantity_left": 8, "unit_price": 180},
        {"item_name": "Salad", "quantity_left": 20, "unit_price": 100}
    ],
    "sales": [
        {"date": "2025-09-09", "item_name": "Burger", "quantity_sold": 15, "total_profit": 1800},
        {"date": "2025-09-09", "item_name": "Pizza", "quantity_sold": 3, "total_profit": 750},
        {"date": "2025-09-09", "item_name": "Fries", "quantity_sold": 22, "total_profit": 1320},
        {"date": "2025-09-08", "item_name": "Burger", "quantity_sold": 20, "total_profit": 2400},
        {"date": "2025-09-08", "item_name": "Pizza", "quantity_sold": 5, "total_profit": 1250},
        {"date": "2025-09-07", "item_name": "Sandwich", "quantity_sold": 12, "total_profit": 1080},
    ]
}

# Database helper functions
def get_inventory_by_item(item_name: str) -> Dict[str, Any]:
    """Get inventory details for a specific item"""
    for item in db["inventory"]:
        if item["item_name"].lower() == item_name.lower():
            return item
    return None

def get_all_inventory() -> List[Dict[str, Any]]:
    """Get all inventory items"""
    return db["inventory"]

def get_low_stock_items(threshold: int = 10) -> List[Dict[str, Any]]:
    """Get items with stock below threshold"""
    return [item for item in db["inventory"] if item["quantity_left"] < threshold]

def get_sales_by_date(date: str) -> List[Dict[str, Any]]:
    """Get sales for a specific date"""
    return [sale for sale in db["sales"] if sale["date"] == date]

def get_total_profit_by_date(date: str) -> float:
    """Get total profit for a specific date"""
    daily_sales = get_sales_by_date(date)
    return sum(sale["total_profit"] for sale in daily_sales)

def get_total_profit_all_time() -> float:
    """Get total profit across all dates"""
    return sum(sale["total_profit"] for sale in db["sales"])

def get_top_selling_items() -> List[Dict[str, Any]]:
    """Get items sorted by quantity sold"""
    item_sales = {}
    for sale in db["sales"]:
        item_name = sale["item_name"]
        if item_name not in item_sales:
            item_sales[item_name] = {"item_name": item_name, "total_sold": 0, "total_profit": 0}
        item_sales[item_name]["total_sold"] += sale["quantity_sold"]
        item_sales[item_name]["total_profit"] += sale["total_profit"]
    
    return sorted(item_sales.values(), key=lambda x: x["total_sold"], reverse=True)

def search_database_context(query: str) -> Dict[str, Any]:
    """Search database and return relevant context based on query"""
    query_lower = query.lower()
    context = {"query_type": "general", "data": {}}
    
    # Detect query type and fetch relevant data
    if any(word in query_lower for word in ["inventory", "stock", "left", "remaining", "available"]):
        context["query_type"] = "inventory"
        if any(item["item_name"].lower() in query_lower for item in db["inventory"]):
            # Specific item query
            for item in db["inventory"]:
                if item["item_name"].lower() in query_lower:
                    context["data"] = get_inventory_by_item(item["item_name"])
                    break
        else:
            # General inventory query
            context["data"] = get_all_inventory()
    
    elif any(word in query_lower for word in ["profit", "sales", "revenue", "earnings"]):
        context["query_type"] = "sales"
        if "today" in query_lower or "2025-09-09" in query_lower:
            context["data"] = {
                "date": "2025-09-09",
                "sales": get_sales_by_date("2025-09-09"),
                "total_profit": get_total_profit_by_date("2025-09-09")
            }
        else:
            context["data"] = {
                "all_sales": db["sales"],
                "total_profit": get_total_profit_all_time()
            }
    
    elif any(word in query_lower for word in ["low", "running", "out", "shortage"]):
        context["query_type"] = "low_stock"
        context["data"] = get_low_stock_items()
    
    elif any(word in query_lower for word in ["top", "best", "popular", "selling"]):
        context["query_type"] = "top_selling"
        context["data"] = get_top_selling_items()
    
    else:
        # General query - provide overview
        context["query_type"] = "overview"
        context["data"] = {
            "inventory": get_all_inventory(),
            "recent_sales": get_sales_by_date("2025-09-09"),
            "total_profit": get_total_profit_all_time()
        }
    
    return context

def generate_llm_response(query: str, context: Dict[str, Any]) -> str:
    """Generate response using Gemini API or demo mode"""
    if not model:
        # Demo mode: Generate realistic responses based on context
        query_type = context.get("query_type", "general")
        data = context.get("data", {})
        
        if query_type == "inventory":
            if isinstance(data, dict) and data.get("item_name"):
                quantity = data['quantity_left']
                price = data['unit_price']
                item = data['item_name']
                return f"You currently have {quantity} {item.lower()}s left in stock, priced at ₹{price} each. {'⚠️ Running low!' if quantity < 10 else '✅ Stock looks good!'}"
            elif isinstance(data, list):
                items = [f"{item['item_name']}: {item['quantity_left']} units" for item in data]
                return f"📦 **Inventory Overview:**\n" + "\n".join(items)
            return "I couldn't find specific inventory details for that query."
        
        elif query_type == "sales":
            if "date" in data:
                date = data["date"]
                total_profit = data.get("total_profit", 0)
                sales_count = len(data.get("sales", []))
                return f"📊 **Sales Report for {date}:**\n💰 Total Profit: ₹{total_profit:,}\n📈 Number of transactions: {sales_count}"
            else:
                total_profit = data.get("total_profit", 0)
                return f"💰 **All-time total profit:** ₹{total_profit:,}\n🎯 Great job managing your restaurant!"
        
        elif query_type == "low_stock":
            if isinstance(data, list) and data:
                low_items = [f"• {item['item_name']}: Only {item['quantity_left']} left" for item in data]
                return f"⚠️ **Low Stock Alert:**\n" + "\n".join(low_items) + "\n\n💡 Consider restocking these items soon!"
            return "✅ All items are well-stocked! No items are running low."
        
        elif query_type == "top_selling":
            if isinstance(data, list) and data:
                top_items = [f"{i+1}. {item['item_name']}: {item['total_sold']} sold (₹{item['total_profit']} profit)" for i, item in enumerate(data[:5])]
                return f"🏆 **Top Selling Items:**\n" + "\n".join(top_items)
            return "📊 No sales data available yet to determine top-selling items."
        
        elif query_type == "overview":
            inventory_count = len(data.get("inventory", []))
            recent_sales = len(data.get("recent_sales", []))
            total_profit = data.get("total_profit", 0)
            return f"🏪 **Restaurant Overview:**\n📦 Inventory Items: {inventory_count}\n📊 Today's Sales: {recent_sales} transactions\n💰 All-time Profit: ₹{total_profit:,}\n\n🤖 *Demo Mode Active - Get your Gemini API key for smarter responses!*"
        
        return "🤖 I'm running in demo mode! Ask me about inventory, sales, profits, or low stock items.\n\n💡 *Get a Gemini API key for more intelligent responses!*"
    
    try:
        # Get comprehensive prompt from file-based system
        query_type = context.get("query_type", "default")
        prompt = get_formatted_prompt(query_type, query, context)
        
        logger.info(f"[GEMINI] Using '{query_type}' prompt template")
        logger.info("[GEMINI] Calling model gemini-1.5-flash ...")
        response = model.generate_content(prompt)
        text = getattr(response, 'text', '') or ''
        logger.info(f"[GEMINI] Received response (chars={len(text)}).")
        return text
        
    except Exception as e:
        return f"I apologize, but I encountered an error processing your request: {str(e)}"

# API Routes
@app.get("/")
async def root():
    return {"message": "Swiggy Chatbot API is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Search database for relevant context
        context = search_database_context(request.message)
        
        # Generate response using LLM
        response_text = generate_llm_response(request.message, context)
        
        return ChatResponse(
            response=response_text,
            data_used=context
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "gemini_api_configured": GEMINI_API_KEY is not None,
        "database_items": len(db["inventory"]),
        "sales_records": len(db["sales"])
    }

@app.get("/prompt-info")
async def prompt_info():
    """Get information about loaded prompt templates (for demo purposes)"""
    return get_prompt_info()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
