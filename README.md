# Swiggy Chatbot - Full Stack Restaurant Management Assistant

A full-stack chatbot application that helps restaurant owners manage their inventory, track sales, and analyze profits through an AI-powered conversational interface.

## 🚀 Features

- **Professional Chat Interface**: React-based chatbot with Tailwind CSS styling
- **Restaurant Management**: Check inventory, sales data, profits, and more
- **AI-Powered Responses**: Uses Gemini API for intelligent responses
- **Real-time Communication**: FastAPI backend with seamless frontend integration
- **Local Database**: In-memory Python dictionary for fast data retrieval

## 📁 Project Structure

```
SwiggyBot/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main application file
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment variables template
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── Chatbot.tsx # Main chatbot component
│   │   ├── App.tsx         # App component
│   │   └── index.css       # Tailwind CSS
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind configuration
└── README.md              # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** installed
- **Gemini API Key** (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the backend server:**
   ```bash
   uvicorn main:app --reload
   ```

   The backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will be available at: `http://localhost:3000`

## 🎯 Usage Examples

Once both servers are running, you can ask questions like:

- **Inventory Queries:**
  - "How many burgers are left?"
  - "Show me all inventory"
  - "Which items are running low?"

- **Sales & Profit:**
  - "What's today's profit?"
  - "Show me all sales data"
  - "What are my best selling items?"

- **General Questions:**
  - "Give me a business overview"
  - "What should I restock?"

## 🏗️ Architecture

### Integration Flow
```
Frontend (React) → Backend (FastAPI) → Database (Python Dict) → LLM (Gemini API) → Response
```

1. User enters query in React frontend
2. Frontend sends POST request to `/chat` endpoint
3. Backend searches local database for relevant data
4. Backend sends query + data context to Gemini API
5. LLM generates intelligent response
6. Backend returns structured response to frontend
7. Frontend displays response in chat interface

### Database Schema

```python
db = {
    "inventory": [
        {
            "item_name": "Burger",
            "quantity_left": 24,
            "unit_price": 120
        }
        # ... more items
    ],
    "sales": [
        {
            "date": "2025-09-09",
            "item_name": "Burger", 
            "quantity_sold": 15,
            "total_profit": 1800
        }
        # ... more sales records
    ]
}
```

## 🔧 API Endpoints

### POST /chat
- **Description**: Process user query and return AI response
- **Request Body**: `{"message": "How many burgers are left?"}`
- **Response**: `{"response": "You currently have 24 burgers left in stock.", "data_used": {...}}`

### GET /health
- **Description**: Health check endpoint
- **Response**: API status and configuration info

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Smooth conversation flow with typing indicators
- **Quick Actions**: Pre-built query buttons for common questions
- **Professional UI**: Orange theme matching Swiggy branding
- **Error Handling**: Graceful error messages and retry capabilities

## 🔒 Environment Configuration

Create a `.env` file in the backend directory:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Alternative LLM APIs
# ZAI_API_KEY=your_zai_api_key
# ZAI_BASE_URL=https://api.zai.com/v1
```

## 🚨 Troubleshooting

### Backend Issues
- **Port already in use**: Change port in `uvicorn main:app --reload --port 8001`
- **API key error**: Ensure GEMINI_API_KEY is set correctly
- **CORS errors**: Backend is configured for localhost:3000 and localhost:5173

### Frontend Issues
- **Build errors**: Run `npm install` to ensure all dependencies are installed
- **API connection failed**: Verify backend is running on port 8000

## 📦 Dependencies

### Backend
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation
- `google-generativeai`: Gemini API client
- `python-dotenv`: Environment variables

### Frontend
- `react`: UI library
- `typescript`: Type safety
- `tailwindcss`: Styling framework

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Made with ❤️ for restaurant owners who want to manage their business smarter!**
