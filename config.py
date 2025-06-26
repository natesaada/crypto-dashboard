import os

class Config:
    """Configuration settings for the application"""
    
    # CoinMarketCap API Configuration
    CMC_API_KEY = os.environ.get('CMC_API_KEY') or 'e131422b-6290-4d0c-8fad-2041edeb4249'
    CMC_BASE_URL = 'https://pro-api.coinmarketcap.com'
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # API Rate Limiting
    DEFAULT_LIMIT = 10
    MAX_LIMIT = 100
    
    # Supported Currencies
    SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY'] 