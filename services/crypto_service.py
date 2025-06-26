from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from typing import Dict, List, Optional, Any
from config import Config

class CryptoService:
    """Service class for handling cryptocurrency API operations"""
    
    def __init__(self):
        self.base_url = Config.CMC_BASE_URL
        self.api_key = Config.CMC_API_KEY
        self.session = Session()
        self.session.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        })
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return {'error': f'Connection error: {str(e)}'}
        except Exception as e:
            return {'error': f'API error: {str(e)}'}
    
    def get_crypto_listings(self, limit: int = 10, start: int = 1, 
                           convert: str = 'USD', sort: str = 'market_cap', sort_dir: str = 'desc') -> List[Dict]:
        """Get cryptocurrency listings with market data"""
        params = {
            'start': str(start),
            'limit': str(min(limit, Config.MAX_LIMIT)),
            'convert': convert,
            'sort': sort,
            'sort_dir': sort_dir
        }
        
        data = self._make_request('/v1/cryptocurrency/listings/latest', params)
        
        if 'error' in data:
            return [data]
        
        return self._extract_basic_info(data.get('data', []))
    
    def get_crypto_quotes(self, symbols: List[str], convert: str = 'USD') -> List[Dict]:
        """Get specific cryptocurrency quotes by symbol"""
        if not symbols:
            return []
        
        params = {
            'symbol': ','.join(symbols),
            'convert': convert
        }
        
        data = self._make_request('/v1/cryptocurrency/quotes/latest', params)
        
        if 'error' in data:
            return [data]
        
        quotes = []
        for symbol in symbols:
            if symbol in data.get('data', {}):
                coin_data = data['data'][symbol]
                quotes.append(self._extract_quote_info(coin_data))
        
        return quotes
    
    def get_crypto_info(self, symbol: str) -> Dict:
        """Get detailed information about a specific cryptocurrency"""
        params = {'symbol': symbol}
        
        data = self._make_request('/v1/cryptocurrency/info', params)
        
        if 'error' in data:
            return data
        
        coin_data = data.get('data', {}).get(symbol, {})
        return self._extract_detailed_info(coin_data)
    
    def get_market_pairs(self, symbol: str) -> List[Dict]:
        """Get market pairs for a specific cryptocurrency"""
        params = {'symbol': symbol}
        
        data = self._make_request('/v1/cryptocurrency/market-pairs/latest', params)
        
        if 'error' in data:
            return [data]
        
        pairs = data.get('data', {}).get('market_pairs', [])
        return self._extract_market_pairs(pairs)
    
    def get_global_metrics(self, convert: str = 'USD') -> Dict:
        """Get global cryptocurrency market metrics"""
        params = {'convert': convert}
        
        data = self._make_request('/v1/global-metrics/quotes/latest', params)
        
        if 'error' in data:
            return data
        
        return self._extract_global_metrics(data.get('data', {}))
    
    def search_cryptocurrencies(self, query: str, by_symbol: bool = False) -> List[Dict]:
        """Search for cryptocurrencies by name or symbol"""
        params = {'listing_status': 'active,inactive'}
        data = self._make_request('/v1/cryptocurrency/map', params)
        if 'error' in data:
            return [data]
        results = data.get('data', [])
        if by_symbol:
            # Exact match on symbol (case-insensitive)
            filtered = [r for r in results if r.get('symbol', '').upper() == query.upper()]
        else:
            # Substring match on name (case-insensitive)
            filtered = [r for r in results if query.lower() in r.get('name', '').lower()]
        return self._extract_search_results(filtered)
    
    def get_trending_cryptocurrencies(self) -> List[Dict]:
        """Get trending cryptocurrencies (using gainers/losers)"""
        # Get top gainers (descending)
        gainers = self.get_crypto_listings(limit=5, sort='percent_change_24h', sort_dir='desc')
        # Get top losers (ascending)
        losers = self.get_crypto_listings(limit=5, sort='percent_change_24h', sort_dir='asc')
        return {
            'top_gainers': gainers,
            'top_losers': losers
        }
    
    def _extract_basic_info(self, coins: List[Dict]) -> List[Dict]:
        """Extract basic information from coin data"""
        basic_info = []
        for coin in coins:
            basic_info.append({
                'id': coin.get('id'),
                'name': coin.get('name'),
                'symbol': coin.get('symbol'),
                'slug': coin.get('slug'),
                'rank': coin.get('cmc_rank'),
                'price_usd': coin.get('quote', {}).get('USD', {}).get('price'),
                'market_cap': coin.get('quote', {}).get('USD', {}).get('market_cap'),
                'volume_24h': coin.get('quote', {}).get('USD', {}).get('volume_24h'),
                'percent_change_1h': coin.get('quote', {}).get('USD', {}).get('percent_change_1h'),
                'percent_change_24h': coin.get('quote', {}).get('USD', {}).get('percent_change_24h'),
                'percent_change_7d': coin.get('quote', {}).get('USD', {}).get('percent_change_7d'),
                'percent_change_30d': coin.get('quote', {}).get('USD', {}).get('percent_change_30d'),
                'circulating_supply': coin.get('circulating_supply'),
                'total_supply': coin.get('total_supply'),
                'max_supply': coin.get('max_supply'),
                'last_updated': coin.get('last_updated'),
                'tags': coin.get('tags', [])
            })
        return basic_info
    
    def _extract_quote_info(self, coin_data: Dict) -> Dict:
        """Extract quote information from coin data"""
        return {
            'id': coin_data.get('id'),
            'name': coin_data.get('name'),
            'symbol': coin_data.get('symbol'),
            'price_usd': coin_data.get('quote', {}).get('USD', {}).get('price'),
            'market_cap': coin_data.get('quote', {}).get('USD', {}).get('market_cap'),
            'volume_24h': coin_data.get('quote', {}).get('USD', {}).get('volume_24h'),
            'percent_change_24h': coin_data.get('quote', {}).get('USD', {}).get('percent_change_24h'),
            'last_updated': coin_data.get('last_updated')
        }
    
    def _extract_detailed_info(self, coin_data: Dict) -> Dict:
        """Extract detailed information from coin data"""
        return {
            'id': coin_data.get('id'),
            'name': coin_data.get('name'),
            'symbol': coin_data.get('symbol'),
            'category': coin_data.get('category'),
            'description': coin_data.get('description'),
            'logo': coin_data.get('logo'),
            'urls': coin_data.get('urls', {}),
            'tags': coin_data.get('tags', []),
            'platform': coin_data.get('platform'),
            'date_added': coin_data.get('date_added'),
            'notice': coin_data.get('notice')
        }
    
    def _extract_market_pairs(self, pairs: List[Dict]) -> List[Dict]:
        """Extract market pair information"""
        return [{
            'exchange': pair.get('exchange', {}).get('name'),
            'pair': pair.get('market_pair'),
            'price': pair.get('quote', {}).get('USD', {}).get('price'),
            'volume_24h': pair.get('quote', {}).get('USD', {}).get('volume_24h'),
            'percent_exchange_volume': pair.get('percent_exchange_volume'),
            'last_updated': pair.get('last_updated')
        } for pair in pairs]
    
    def _extract_global_metrics(self, data: Dict) -> Dict:
        """Extract global market metrics"""
        return {
            'total_market_cap': data.get('quote', {}).get('USD', {}).get('total_market_cap'),
            'total_volume_24h': data.get('quote', {}).get('USD', {}).get('total_volume_24h'),
            'bitcoin_dominance': data.get('btc_dominance'),
            'ethereum_dominance': data.get('eth_dominance'),
            'active_cryptocurrencies': data.get('active_cryptocurrencies'),
            'active_exchanges': data.get('active_exchanges'),
            'last_updated': data.get('last_updated')
        }
    
    def _extract_search_results(self, results: List[Dict]) -> List[Dict]:
        """Extract search result information"""
        return [{
            'id': result.get('id'),
            'name': result.get('name'),
            'symbol': result.get('symbol'),
            'slug': result.get('slug'),
            'rank': result.get('rank'),
            'is_active': result.get('is_active'),
            'first_historical_data': result.get('first_historical_data'),
            'last_historical_data': result.get('last_historical_data'),
            'platform': result.get('platform')
        } for result in results] 