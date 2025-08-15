"""
Yahoo Finance data scraper for stock information
"""
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, List, Optional
import time
import config

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class YahooFinanceScaper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_stock_data(self, symbol: str) -> Optional[Dict]:
        """Get comprehensive stock data for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="5d")
            
            if hist.empty or not info:
                return None
                
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            
            # Calculate metrics
            daily_change = ((current_price - prev_close) / prev_close) * 100
            volume = hist['Volume'].iloc[-1]
            avg_volume = hist['Volume'].mean()
            volume_ratio = volume / avg_volume if avg_volume > 0 else 0
            
            # Get market cap
            shares_outstanding = info.get('sharesOutstanding', 0)
            market_cap = shares_outstanding * current_price if shares_outstanding else 0
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', symbol),
                'current_price': round(current_price, 2),
                'daily_change': round(daily_change, 2),
                'volume': int(volume),
                'avg_volume': int(avg_volume),
                'volume_ratio': round(volume_ratio, 2),
                'market_cap': int(market_cap),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'short_ratio': info.get('shortRatio', 0),
                'short_percent_float': info.get('shortPercentOfFloat', 0),
                'beta': info.get('beta', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'timestamp': int(time.time())
            }
            
        except Exception as e:
            logger.error(f"Error getting data for {symbol}: {e}")
            return None
    
    def get_small_cap_gainers(self) -> List[Dict]:
        """Get list of small cap gainers from Yahoo Finance screener"""
        try:
            # Yahoo Finance screener URL for small cap gainers
            url = "https://finance.yahoo.com/screener/predefined/small_cap_gainers"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            gainers = []
            
            # Parse the screener table
            table = soup.find('table', {'data-test': 'screener-table'})
            if not table:
                logger.warning("Could not find screener table on Yahoo Finance")
                return []
                
            rows = table.find('tbody').find_all('tr')
            
            for row in rows[:50]:  # Limit to first 50 results
                cells = row.find_all('td')
                if len(cells) >= 8:
                    try:
                        symbol = cells[0].text.strip()
                        name = cells[1].text.strip()
                        price = float(cells[2].text.replace(',', ''))
                        change = cells[3].text.strip()
                        change_pct = float(change.replace('%', '').replace('+', ''))
                        volume = cells[4].text.strip()
                        
                        # Convert volume to number
                        if 'M' in volume:
                            volume_num = float(volume.replace('M', '')) * 1_000_000
                        elif 'K' in volume:
                            volume_num = float(volume.replace('K', '')) * 1_000
                        else:
                            volume_num = float(volume.replace(',', ''))
                        
                        # Get additional data for this stock
                        stock_data = self.get_stock_data(symbol)
                        if stock_data and config.SMALL_CAP_MIN <= stock_data['market_cap'] <= config.SMALL_CAP_MAX:
                            stock_data.update({
                                'current_price': price,
                                'daily_change': change_pct,
                                'volume': int(volume_num)
                            })
                            gainers.append(stock_data)
                            
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error parsing row: {e}")
                        continue
                        
            return gainers
            
        except Exception as e:
            logger.error(f"Error scraping Yahoo Finance gainers: {e}")
            return []
    
    def get_most_active_small_caps(self) -> List[Dict]:
        """Get most active small cap stocks"""
        try:
            url = "https://finance.yahoo.com/screener/predefined/most_actives"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            actives = []
            table = soup.find('table', {'data-test': 'screener-table'})
            
            if not table:
                return []
                
            rows = table.find('tbody').find_all('tr')
            
            for row in rows[:30]:
                cells = row.find_all('td')
                if len(cells) >= 6:
                    try:
                        symbol = cells[0].text.strip()
                        
                        # Get full stock data
                        stock_data = self.get_stock_data(symbol)
                        if (stock_data and 
                            config.SMALL_CAP_MIN <= stock_data['market_cap'] <= config.SMALL_CAP_MAX and
                            stock_data['volume_ratio'] >= config.MIN_VOLUME_RATIO):
                            actives.append(stock_data)
                            
                    except Exception as e:
                        logger.warning(f"Error processing active stock {symbol}: {e}")
                        continue
                        
            return actives
            
        except Exception as e:
            logger.error(f"Error scraping Yahoo Finance most actives: {e}")
            return []
    
    def search_stocks_by_criteria(self, min_gain: float = 5.0) -> List[Dict]:
        """Search for stocks meeting specific criteria"""
        try:
            # Get both gainers and most actives, then filter and combine
            gainers = self.get_small_cap_gainers()
            actives = self.get_most_active_small_caps()
            
            # Combine and deduplicate
            all_stocks = {}
            
            for stock in gainers + actives:
                if stock['daily_change'] >= min_gain:
                    all_stocks[stock['symbol']] = stock
            
            return list(all_stocks.values())
            
        except Exception as e:
            logger.error(f"Error in search_stocks_by_criteria: {e}")
            return []