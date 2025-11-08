# 📊 Stock Analytics Dashboard - Backend API

A high-performance FastAPI backend providing real-time stock data, user authentication, and analytics for the Stock Analytics Dashboard. Built with **Python 3.9+**, **FastAPI**, **Firebase Admin SDK**, and **yfinance**.

## ✨ Features

### 🔐 Authentication & Security
- **Firebase Admin SDK** integration for token verification
- **JWT token validation** with proper error handling
- **CORS configuration** for cross-origin requests
- **Rate limiting** and request caching

### 📈 Stock Data API
- **Real-time stock quotes** with multiple data sources
- **Historical data** with optimized intervals per timeframe
- **Multiple timeframes**: `1D`, `5D`, `1W`, `1M`, `3M`, `1Y`, `YTD`, `MTD`
- **OHLCV data** with volume analysis
- **Fallback data generation** when APIs are unavailable

### 🗄️ Database Integration
- **Firestore integration** for user profiles and preferences
- **User activity logging** for analytics
- **Favorites management** with real-time sync
- **Automatic user profile creation**

### ⚡ Performance Features
- **Request caching** (5-minute default)
- **Async/await** for non-blocking operations
- **Error handling** with graceful fallbacks
- **Logging** for debugging and monitoring

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Firebase project with Admin SDK enabled
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   cd stock-analytics-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your Firebase credentials:
   ```env
   # Firebase Configuration
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_PRIVATE_KEY_ID=your-private-key-id
   FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\nYour-Private-Key-Here\\n-----END PRIVATE KEY-----\\n"
   FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
   FIREBASE_CLIENT_ID=your-client-id
   
   # API Configuration
   CORS_ORIGINS=http://localhost:3000,https://your-domain.com
   API_HOST=0.0.0.0
   API_PORT=8000
   
   # Cache Configuration
   CACHE_EXPIRE_SECONDS=300
   
   # Development Settings
   ENVIRONMENT=development
   DEBUG=true
   ```

### Firebase Admin SDK Setup

1. **Generate Service Account Key**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Navigate to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Download the JSON file

2. **Extract Credentials**
   From the downloaded JSON file, copy these values to your `.env`:
   - `project_id` → `FIREBASE_PROJECT_ID`
   - `private_key_id` → `FIREBASE_PRIVATE_KEY_ID`
   - `private_key` → `FIREBASE_PRIVATE_KEY` (keep \\n escape sequences)
   - `client_email` → `FIREBASE_CLIENT_EMAIL`
   - `client_id` → `FIREBASE_CLIENT_ID`

3. **Firestore Database Setup**
   - Enable Firestore Database in Firebase Console
   - Set up security rules (see frontend README)

### Running the Application

```bash
# Development mode
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## 📚 API Documentation

### Authentication

All protected endpoints require a Firebase ID token in the Authorization header:
```
Authorization: Bearer <firebase-id-token>
```

### Endpoints

#### 🔍 Stock Data

**GET `/api/stocks`**
- Fetch stock data for specified symbols and timeframe
- **Parameters**:
  - `symbols` (string): Comma-separated symbols (e.g., "AAPL,MSFT,GOOGL")
  - `range` (string): Timeframe ("1D", "5D", "1W", "1M", "3M", "1Y", "YTD", "MTD")
- **Response**: OHLCV data with timestamps
- **Authentication**: Required

```bash
curl -H "Authorization: Bearer <token>" \\
  "http://localhost:8000/api/stocks?symbols=AAPL,MSFT&range=1D"
```

#### 👤 User Profile

**GET `/api/profile`**
- Get user profile information
- **Authentication**: Required
- **Response**: User profile with preferences and favorites

**POST `/api/profile`**
- Update user profile
- **Body**: Profile data object
- **Authentication**: Required

#### ⭐ Favorites Management

**POST `/api/favorites`**
- Add symbol to favorites
- **Body**: `{"symbol": "AAPL"}`
- **Authentication**: Required

**DELETE `/api/favorites/{symbol}`**
- Remove symbol from favorites
- **Authentication**: Required

#### 🔍 Health Check

**GET `/health`**
- Health check endpoint
- **Response**: API status and configuration
- **Authentication**: Not required

### Response Examples

**Stock Data Response:**
```json
{
  "AAPL": {
    "timestamps": [1640995200000, 1640998800000],
    "open": [182.61, 183.00],
    "high": [184.20, 184.95],
    "low": [181.50, 182.75],
    "close": [182.86, 184.25],
    "volume": [74919600, 68751200]
  }
}
```

**User Profile Response:**
```json
{
  "uid": "user123",
  "email": "user@example.com",
  "displayName": "John Doe",
  "favorites": ["AAPL", "MSFT", "GOOGL"],
  "preferences": {
    "defaultTimeRange": "1M",
    "defaultSymbols": "AAPL,MSFT,GOOGL"
  },
  "lastLogin": "2024-01-15T10:30:00Z"
}
```

## 🏗️ Project Structure

```
stock-analytics-backend/
├── main.py                 # FastAPI application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── .env                   # Environment variables (create this)
└── README.md              # This file
```

## 🔧 Configuration

### Timeframe Mapping

The API automatically maps frontend timeframes to optimal yfinance parameters:

```python
period_map = {
    '1D': '1d',    # 1-minute intervals
    '5D': '5d',    # 5-minute intervals  
    '1W': '5d',    # 15-minute intervals
    '1M': '1mo',   # 1-hour intervals
    '3M': '3mo',   # Daily intervals
    '1Y': '1y',    # Daily intervals
    'YTD': 'ytd',  # Daily intervals
    'MTD': '1mo'   # Hourly intervals
}
```

### Cache Configuration

```python
# Cache requests for 5 minutes by default
CACHE_EXPIRE_SECONDS = 300

# Customize cache settings
requests_cache.install_cache('stock_cache', expire_after=CACHE_EXPIRE_SECONDS)
```

### CORS Configuration

```python
# Configure allowed origins
CORS_ORIGINS = [
    "http://localhost:3000",      # Development frontend
    "https://your-domain.com"     # Production frontend
]
```

## 🐛 Troubleshooting

### Common Issues

1. **Firebase Authentication Errors**
   ```
   Error: "Invalid or expired token"
   ```
   - Verify Firebase credentials in `.env`
   - Check token format and expiration
   - Ensure Firebase project is properly configured

2. **Stock Data API Errors**
   ```
   Error: "No data available"
   ```
   - Check yfinance API status
   - Verify symbol validity
   - API will fallback to sample data automatically

3. **CORS Errors**
   ```
   Error: "Access-Control-Allow-Origin"
   ```
   - Add frontend URL to `CORS_ORIGINS` in `.env`
   - Restart the server after configuration changes

4. **Module Import Errors**
   ```
   Error: "No module named 'firebase_admin'"
   ```
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

### Debug Mode

Enable detailed logging:
```python
# Set in .env
DEBUG=true

# Or set logging level in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Development Mode

When Firebase is not configured, the API runs in development mode:
- Token validation is bypassed
- Mock user data is returned
- All endpoints remain functional for testing

## 🚀 Deployment

### Environment Variables for Production

```env
ENVIRONMENT=production
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://your-frontend-domain.com
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment

**Google Cloud Run:**
```bash
gcloud run deploy stock-analytics-api \\
  --source . \\
  --platform managed \\
  --region us-central1 \\
  --allow-unauthenticated
```

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 📊 Monitoring & Analytics

### Health Monitoring

```bash
# Check API health
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "firebase_enabled": true,
  "environment": "development"
}
```

### User Activity Tracking

The API automatically logs user activities to Firestore:
- Stock data fetches
- Profile updates
- Favorite changes
- Authentication events

### Performance Monitoring

- Request caching reduces API calls
- Async operations prevent blocking
- Error logging for debugging
- Response time tracking available via FastAPI middleware

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use secure key generation
   - Rotate Firebase keys regularly

2. **Token Validation**
   - Always verify Firebase ID tokens
   - Handle token expiration gracefully
   - Log authentication failures

3. **Rate Limiting**
   - Implement request limits per user
   - Cache responses to reduce load
   - Monitor for abuse patterns

4. **Data Validation**
   - Validate all input parameters
   - Sanitize user data before storage
   - Use Pydantic models for type safety

## 📝 API Testing

### Using curl

```bash
# Get user profile
curl -H "Authorization: Bearer $TOKEN" \\
  http://localhost:8000/api/profile

# Fetch stock data
curl -H "Authorization: Bearer $TOKEN" \\
  "http://localhost:8000/api/stocks?symbols=AAPL&range=1D"

# Add favorite
curl -X POST -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"symbol":"TSLA"}' \\
  http://localhost:8000/api/favorites
```

### Using Python

```python
import requests

headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/api/stocks",
    params={"symbols": "AAPL,MSFT", "range": "1D"},
    headers=headers
)
print(response.json())
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🔗 Related

- [Frontend Documentation](../stock-analytics-frontend/README.md)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [yfinance Documentation](https://pypi.org/project/yfinance/)

---
