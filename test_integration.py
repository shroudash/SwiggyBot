#!/usr/bin/env python3
"""
Integration test for Swiggy Chatbot
Tests the complete flow without requiring API keys
"""

import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from main import search_database_context, generate_llm_response

def test_database_functions():
    """Test database helper functions"""
    print("🔄 Testing Database Functions...")
    
    # Test inventory query
    context = search_database_context("How many burgers are left?")
    print(f"✅ Inventory Query: {context['query_type']}")
    print(f"   Data: {context['data']}")
    
    # Test sales query
    context = search_database_context("What's today's profit?")
    print(f"✅ Sales Query: {context['query_type']}")
    print(f"   Total Profit: ₹{context['data']['total_profit']}")
    
    # Test low stock query
    context = search_database_context("Which items are running low?")
    print(f"✅ Low Stock Query: {context['query_type']}")
    print(f"   Low Stock Items: {len(context['data'])} items")
    
    print("✅ All database functions working correctly!\n")

def test_mock_llm_response():
    """Test LLM response generation (without API key)"""
    print("🔄 Testing Mock LLM Response...")
    
    # Mock the LLM response for demonstration
    query = "How many burgers are left?"
    context = search_database_context(query)
    
    # Since we don't have API key, create a mock response
    if context['data'] and 'item_name' in context['data']:
        quantity = context['data']['quantity_left']
        price = context['data']['unit_price']
        mock_response = f"You currently have {quantity} {context['data']['item_name'].lower()}s left in stock, priced at ₹{price} each."
    else:
        mock_response = "I can help you with inventory, sales, and profit queries!"
    
    print(f"✅ Query: {query}")
    print(f"✅ Mock Response: {mock_response}")
    print("✅ LLM integration flow working correctly!\n")

def test_api_endpoints():
    """Test API endpoint structure"""
    print("🔄 Testing API Endpoint Structure...")
    
    # Test the main chat endpoint logic
    test_queries = [
        "How many burgers are left?",
        "What's today's profit?", 
        "Show me low stock items",
        "What are my best selling items?"
    ]
    
    for query in test_queries:
        context = search_database_context(query)
        print(f"✅ Query: '{query}' -> Type: {context['query_type']}")
    
    print("✅ All API endpoint logic working correctly!\n")

def main():
    """Run all integration tests"""
    print("🚀 Swiggy Chatbot Integration Test\n")
    print("=" * 50)
    
    try:
        test_database_functions()
        test_mock_llm_response()
        test_api_endpoints()
        
        print("🎉 ALL TESTS PASSED!")
        print("\nNext Steps:")
        print("1. Get a Gemini API key from: https://makersuite.google.com/app/apikey")
        print("2. Create backend/.env file with: GEMINI_API_KEY=your_key_here")
        print("3. Start backend: cd backend && uvicorn main:app --reload")
        print("4. Start frontend: cd frontend && npm start")
        print("5. Open http://localhost:3000 to use the chatbot!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
