# 🚀 Advanced Crypto Dashboard

A comprehensive cryptocurrency market data dashboard built with Flask and the CoinMarketCap API, following best practices for code organization and maintainability.

## 📁 Project Structure

```
API Testing/
├── app.py                      # Flask application (routes only)
├── config.py                   # Configuration settings
├── services/
│   └── crypto_service.py       # API logic and business logic
├── templates/
│   └── dashboard.html          # Web interface
├── env_example.txt             # Environment variables template
└── README.md                   # This file
```

## 🏗️ Architecture

### Best Practices Implemented:

1. **Separation of Concerns**
   - `app.py`: Web routes and request handling
   - `crypto_service.py`: API logic and data processing
   - `config.py`: Configuration management
   - `dashboard.html`: Frontend interface

2. **Service Layer Pattern**
   - Centralized API operations in `CryptoService` class
   - Reusable methods for different API endpoints
   - Error handling and data extraction

3. **Configuration Management**
   - Centralized settings in `Config` class
   - Environment variable support
   - API keys and limits management

## 🔒 Security Setup

### ⚠️ IMPORTANT: API Key Configuration

**Before running the application, you MUST set up your API key:**

1. **Get a CoinMarketCap API key:**
   - Visit: https://coinmarketcap.com/api/
   - Sign up for a free account
   - Generate an API key

2. **Set up environment variables:**
   
   **Option A: Create a .env file (recommended)**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env and add your API key
   CMC_API_KEY=your_actual_api_key_here
   ```
   
   **Option B: Set environment variable directly**
   ```bash
   # Windows PowerShell
   $env:CMC_API_KEY="your_actual_api_key_here"
   
   # Windows Command Prompt
   set CMC_API_KEY=your_actual_api_key_here
   
   # Linux/Mac
   export CMC_API_KEY="your_actual_api_key_here"
   ```

3. **Install python-dotenv (optional but recommended):**
   ```bash
   pip install python-dotenv
   ```

### 🔐 Security Notes

- **Never commit your API key** to version control
- **The .env file is ignored** by git (see .gitignore)
- **Use environment variables** in production
- **Rotate your API key** if it gets exposed

## 🚀 Features

### 📊 Market Data Tab
- View cryptocurrency listings with configurable parameters
- Sort by market cap, price, volume, or 24h change
- Adjust number of results and starting position
- Multiple currency support (USD, EUR, GBP, JPY)

### 🔍 Search Tab
- Search cryptocurrencies by name or symbol
- View detailed information about search results
- See active/inactive status and historical data availability

### 📈 Trending Tab
- View top gainers and losers in the last 24 hours
- Real-time price change tracking
- Side-by-side comparison
- Month-over-month growth tracking

### 🌍 Global Metrics Tab
- Total market capitalization
- 24-hour trading volume
- Bitcoin and Ethereum dominance percentages
- Active cryptocurrencies and exchanges count

### 💱 Quotes Tab
- Get specific cryptocurrency quotes by symbol
- Support for multiple symbols (comma-separated)
- Multiple currency conversion

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/api/crypto` | GET | Get cryptocurrency listings |
| `/api/crypto/quotes` | GET | Get specific cryptocurrency quotes |
| `/api/crypto/info/<symbol>` | GET | Get detailed crypto information |
| `/api/crypto/market-pairs/<symbol>` | GET | Get market pairs for a crypto |
| `/api/global-metrics` | GET | Get global market metrics |
| `/api/search` | GET | Search cryptocurrencies |
| `/api/trending` | GET | Get trending cryptocurrencies |
| `/api/currencies` | GET | Get supported currencies |
| `/api/status` | GET | Check API status |

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Flask
- Requests library
- CoinMarketCap API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/natesaada/crypto-dashboard.git
   cd crypto-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install flask requests python-dotenv
   ```

3. **Set up your API key** (see Security Setup section above)

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

## 🔧 Configuration

Edit `config.py` to customize:
- Supported currencies
- Rate limiting
- Default values

**Note:** API key should be set via environment variables, not in config.py

## 📊 API Usage Examples

### Get Top 10 Cryptocurrencies
```bash
curl "http://127.0.0.1:5000/api/crypto?limit=10&convert=USD"
```

### Search for Bitcoin
```bash
curl "http://127.0.0.1:5000/api/search?q=Bitcoin"
```

### Get Global Metrics
```bash
curl "http://127.0.0.1:5000/api/global-metrics?convert=USD"
```

### Get Specific Quotes
```bash
curl "http://127.0.0.1:5000/api/crypto/quotes?symbols=BTC,ETH,ADA&convert=USD"
```

## 🔄 Auto-Refresh

The dashboard automatically refreshes market data every 30 seconds when on the Market Data tab.

## 🎨 Features

- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Data**: Live cryptocurrency market data
- **Multiple Views**: Tabbed interface for different data types
- **Error Handling**: Graceful error handling and user feedback
- **Configurable**: Easy to customize and extend

## 🔒 Security Notes

- API key is stored in environment variables (secure)
- Input validation and sanitization implemented
- Rate limiting configured to prevent API abuse
- Sensitive files are excluded from version control

## 🚀 Future Enhancements

- Historical data charts
- Portfolio tracking
- Price alerts
- More detailed analytics
- Export functionality
- User authentication

## 📝 License

This project is for educational purposes. Please respect the CoinMarketCap API terms of service.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
