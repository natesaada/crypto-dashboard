from flask import Flask, render_template, jsonify, request
from services.crypto_service import CryptoService
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the crypto service
crypto_service = CryptoService()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/crypto')
def api_crypto():
    """Get cryptocurrency listings with configurable parameters"""
    limit = request.args.get('limit', Config.DEFAULT_LIMIT, type=int)
    start = request.args.get('start', 1, type=int)
    convert = request.args.get('convert', 'USD')
    sort = request.args.get('sort', 'market_cap')
    
    data = crypto_service.get_crypto_listings(limit, start, convert, sort)
    return jsonify(data)

@app.route('/api/crypto/quotes')
def api_crypto_quotes():
    """Get specific cryptocurrency quotes by symbols"""
    symbols = request.args.get('symbols', '').split(',')
    convert = request.args.get('convert', 'USD')
    
    # Filter out empty symbols
    symbols = [s.strip() for s in symbols if s.strip()]
    
    if not symbols:
        return jsonify({'error': 'No symbols provided'}), 400
    
    data = crypto_service.get_crypto_quotes(symbols, convert)
    return jsonify(data)

@app.route('/api/crypto/info/<symbol>')
def api_crypto_info(symbol):
    """Get detailed information about a specific cryptocurrency"""
    data = crypto_service.get_crypto_info(symbol.upper())
    return jsonify(data)

@app.route('/api/crypto/market-pairs/<symbol>')
def api_market_pairs(symbol):
    """Get market pairs for a specific cryptocurrency"""
    data = crypto_service.get_market_pairs(symbol.upper())
    return jsonify(data)

@app.route('/api/global-metrics')
def api_global_metrics():
    """Get global cryptocurrency market metrics"""
    convert = request.args.get('convert', 'USD')
    data = crypto_service.get_global_metrics(convert)
    return jsonify(data)

@app.route('/api/search')
def api_search():
    """Search for cryptocurrencies by name or symbol"""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'name')
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    if search_type == 'symbol':
        # Use the CoinMarketCap map endpoint and filter by symbol
        data = crypto_service.search_cryptocurrencies(query.upper(), by_symbol=True)
    else:
        # Default: search by name
        data = crypto_service.search_cryptocurrencies(query, by_symbol=False)
    return jsonify(data)

@app.route('/api/trending')
def api_trending():
    """Get trending cryptocurrencies (top gainers and losers)"""
    data = crypto_service.get_trending_cryptocurrencies()
    return jsonify(data)

@app.route('/api/currencies')
def api_currencies():
    """Get list of supported currencies"""
    return jsonify({
        'currencies': Config.SUPPORTED_CURRENCIES,
        'default': 'USD'
    })

@app.route('/api/status')
def api_status():
    """Check API status and configuration"""
    return jsonify({
        'status': 'operational',
        'api_base_url': Config.CMC_BASE_URL,
        'supported_currencies': Config.SUPPORTED_CURRENCIES,
        'max_limit': Config.MAX_LIMIT,
        'default_limit': Config.DEFAULT_LIMIT
    })

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5000) 