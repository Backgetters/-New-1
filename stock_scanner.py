"""
Main Stock Scanner Engine
Combines all data sources and analysis modules
"""
import logging
import time
from datetime import datetime, time as dt_time
from typing import Dict, List, Optional
import threading
import json
import os

# Import our modules
from data_sources.yahoo_finance import YahooFinanceScaper
from data_sources.finviz_scraper import FinvizScraper
from analysis.short_squeeze_detector import ShortSqueezeDetector
from analysis.sentiment_analyzer import SentimentAnalyzer
import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StockScanner:
    def __init__(self):
        # Initialize data sources
        self.yahoo_scraper = YahooFinanceScaper()
        self.finviz_scraper = FinvizScraper()
        
        # Initialize analysis modules
        self.squeeze_detector = ShortSqueezeDetector()
        self.sentiment_analyzer = SentimentAnalyzer()
        
        # Data storage
        self.cached_data = {
            'top_gainers': [],
            'squeeze_candidates': [],
            'last_update': 0,
            'update_in_progress': False
        }
        
        # Threading
        self.update_thread = None
        self.should_stop = False
        
        logger.info("Stock Scanner initialized")
    
    def is_market_open(self) -> bool:
        """Check if market is currently open"""
        try:
            now = datetime.now().time()
            # Simple check - assumes Eastern time
            return config.MARKET_OPEN <= now <= config.MARKET_CLOSE
        except Exception as e:
            logger.error(f"Error checking market hours: {e}")
            return True  # Default to open for testing
    
    def scan_stocks(self) -> Dict:
        """Main scanning function that combines all data sources"""
        try:
            logger.info("Starting stock scan...")
            
            # Check if we should use demo data
            if config.USE_DEMO_DATA:
                logger.info("Using demo data...")
                from demo_data import get_demo_stocks
                demo_stocks = get_demo_stocks()
                results = self.analyze_and_rank_stocks(demo_stocks)
                
                # Cache results
                self.cached_data.update(results)
                self.cached_data['last_update'] = int(time.time())
                self.cached_data['update_in_progress'] = False
                
                logger.info(f"Demo scan completed. Found {len(demo_stocks)} stocks")
                return results
            
            # Check if update is already in progress
            if self.cached_data['update_in_progress']:
                logger.info("Update already in progress, returning cached data")
                return self.get_cached_results()
            
            self.cached_data['update_in_progress'] = True
            
            # Collect data from all sources
            all_stocks = {}
            
            # Get data from Yahoo Finance
            logger.info("Fetching data from Yahoo Finance...")
            yahoo_gainers = self.yahoo_scraper.get_small_cap_gainers()
            yahoo_actives = self.yahoo_scraper.get_most_active_small_caps()
            
            # Combine Yahoo data
            for stock in yahoo_gainers + yahoo_actives:
                symbol = stock['symbol']
                if symbol not in all_stocks:
                    all_stocks[symbol] = stock
                else:
                    # Merge data, keeping the most recent
                    all_stocks[symbol].update(stock)
            
            # Get data from FinViz
            logger.info("Fetching data from FinViz...")
            finviz_stocks = self.finviz_scraper.get_screener_data()
            finviz_squeeze = self.finviz_scraper.get_short_squeeze_candidates()
            finviz_movers = self.finviz_scraper.get_high_volume_movers()
            
            # Merge FinViz data
            for stock in finviz_stocks + finviz_squeeze + finviz_movers:
                symbol = stock['symbol']
                if symbol in all_stocks:
                    # Merge data from multiple sources
                    all_stocks[symbol].update(stock)
                else:
                    all_stocks[symbol] = stock
            
            # Enhance data with detailed analysis
            logger.info("Enhancing data with detailed analysis...")
            enhanced_stocks = []
            for symbol, stock_data in all_stocks.items():
                try:
                    # Get additional FinViz details if not already present
                    if stock_data.get('source') != 'finviz_detail':
                        finviz_details = self.finviz_scraper.get_stock_details(symbol)
                        if finviz_details:
                            stock_data.update(finviz_details)
                    
                    # Add sentiment analysis
                    sentiment = self.sentiment_analyzer.analyze_stock_sentiment(symbol)
                    stock_data['sentiment'] = sentiment
                    
                    enhanced_stocks.append(stock_data)
                    
                except Exception as e:
                    logger.warning(f"Error enhancing data for {symbol}: {e}")
                    enhanced_stocks.append(stock_data)
            
            # Analyze and rank stocks
            results = self.analyze_and_rank_stocks(enhanced_stocks)
            
            # Cache results
            self.cached_data.update(results)
            self.cached_data['last_update'] = int(time.time())
            self.cached_data['update_in_progress'] = False
            
            logger.info(f"Stock scan completed. Found {len(enhanced_stocks)} stocks")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in stock scan: {e}")
            self.cached_data['update_in_progress'] = False
            return self.get_cached_results()
    
    def analyze_and_rank_stocks(self, stocks: List[Dict]) -> Dict:
        """Analyze and rank stocks for different categories"""
        try:
            # Filter for small caps
            small_caps = []
            for stock in stocks:
                market_cap = stock.get('market_cap', 0)
                if config.SMALL_CAP_MIN <= market_cap <= config.SMALL_CAP_MAX:
                    small_caps.append(stock)
            
            # Get top gainers
            top_gainers = self.get_top_gainers(small_caps)
            
            # Get short squeeze candidates
            squeeze_candidates = self.squeeze_detector.rank_squeeze_candidates(small_caps)
            
            # Calculate composite scores for overall ranking
            for stock in small_caps:
                stock['composite_score'] = self.calculate_composite_score(stock)
            
            # Sort by composite score for overall recommendations
            overall_recommendations = sorted(
                small_caps, 
                key=lambda x: x.get('composite_score', 0), 
                reverse=True
            )[:15]
            
            return {
                'top_gainers': top_gainers,
                'squeeze_candidates': squeeze_candidates,
                'overall_recommendations': overall_recommendations,
                'total_stocks_analyzed': len(stocks),
                'small_caps_found': len(small_caps),
                'scan_timestamp': int(time.time()),
                'market_open': self.is_market_open()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing and ranking stocks: {e}")
            return {
                'top_gainers': [],
                'squeeze_candidates': [],
                'overall_recommendations': [],
                'total_stocks_analyzed': 0,
                'small_caps_found': 0,
                'scan_timestamp': int(time.time()),
                'market_open': self.is_market_open()
            }
    
    def get_top_gainers(self, stocks: List[Dict]) -> List[Dict]:
        """Get top gainers by daily change percentage"""
        try:
            # Filter for significant gains
            gainers = []
            for stock in stocks:
                daily_change = stock.get('daily_change', 0)
                volume_ratio = stock.get('volume_ratio', 1)
                
                if daily_change >= config.MIN_DAILY_GAIN and volume_ratio >= config.MIN_VOLUME_RATIO:
                    gainers.append(stock)
            
            # Sort by daily change descending
            gainers.sort(key=lambda x: x.get('daily_change', 0), reverse=True)
            
            return gainers[:config.TOP_GAINERS_COUNT]
            
        except Exception as e:
            logger.error(f"Error getting top gainers: {e}")
            return []
    
    def calculate_composite_score(self, stock_data: Dict) -> float:
        """Calculate composite score combining multiple factors"""
        try:
            # Get individual scores
            squeeze_score = stock_data.get('squeeze_score', 0)
            daily_change = stock_data.get('daily_change', 0)
            volume_ratio = stock_data.get('volume_ratio', 1)
            sentiment_score = stock_data.get('sentiment', {}).get('sentiment_score', 0)
            
            # Normalize scores (0-100 scale)
            squeeze_normalized = min(squeeze_score, 100)
            momentum_normalized = min(daily_change * 2, 100)  # 50% gain = 100 points
            volume_normalized = min((volume_ratio - 1) * 20, 100)  # 6x volume = 100 points
            sentiment_normalized = (sentiment_score + 1) * 50  # -1 to 1 becomes 0 to 100
            
            # Weighted composite score
            composite = (
                squeeze_normalized * 0.35 +      # 35% weight on squeeze potential
                momentum_normalized * 0.25 +     # 25% weight on price momentum
                volume_normalized * 0.25 +       # 25% weight on volume
                sentiment_normalized * 0.15      # 15% weight on sentiment
            )
            
            return round(composite, 2)
            
        except Exception as e:
            logger.error(f"Error calculating composite score: {e}")
            return 0.0
    
    def get_cached_results(self) -> Dict:
        """Return cached results if available"""
        try:
            if self.cached_data['last_update'] == 0:
                return {
                    'top_gainers': [],
                    'squeeze_candidates': [],
                    'overall_recommendations': [],
                    'message': 'No data available yet. Please wait for initial scan to complete.',
                    'scan_timestamp': int(time.time()),
                    'market_open': self.is_market_open()
                }
            
            # Check if data is too old (more than 1 hour)
            age = int(time.time()) - self.cached_data['last_update']
            if age > 3600:
                self.cached_data['data_warning'] = 'Data is more than 1 hour old'
            
            return {
                'top_gainers': self.cached_data.get('top_gainers', []),
                'squeeze_candidates': self.cached_data.get('squeeze_candidates', []),
                'overall_recommendations': self.cached_data.get('overall_recommendations', []),
                'last_update': self.cached_data['last_update'],
                'data_age_minutes': age // 60,
                'scan_timestamp': int(time.time()),
                'market_open': self.is_market_open(),
                'data_warning': self.cached_data.get('data_warning')
            }
            
        except Exception as e:
            logger.error(f"Error getting cached results: {e}")
            return {'error': 'Error retrieving cached data'}
    
    def start_automated_scanning(self):
        """Start automated scanning in background thread"""
        try:
            if self.update_thread and self.update_thread.is_alive():
                logger.info("Automated scanning already running")
                return
            
            self.should_stop = False
            self.update_thread = threading.Thread(target=self._automated_scan_loop)
            self.update_thread.daemon = True
            self.update_thread.start()
            
            logger.info("Automated scanning started")
            
        except Exception as e:
            logger.error(f"Error starting automated scanning: {e}")
    
    def stop_automated_scanning(self):
        """Stop automated scanning"""
        try:
            self.should_stop = True
            if self.update_thread:
                self.update_thread.join(timeout=10)
            
            logger.info("Automated scanning stopped")
            
        except Exception as e:
            logger.error(f"Error stopping automated scanning: {e}")
    
    def _automated_scan_loop(self):
        """Background loop for automated scanning"""
        while not self.should_stop:
            try:
                # Only scan during market hours or if data is very old
                if self.is_market_open() or (int(time.time()) - self.cached_data['last_update'] > 3600):
                    logger.info("Running automated scan...")
                    self.scan_stocks()
                
                # Wait for next update interval
                for _ in range(config.DATA_UPDATE_INTERVAL):
                    if self.should_stop:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in automated scan loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def save_results_to_file(self, filename: str = None):
        """Save current results to JSON file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"stock_scan_results_{timestamp}.json"
            
            results = self.get_cached_results()
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Results saved to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving results to file: {e}")
            return None