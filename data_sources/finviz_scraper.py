"""
FinViz scraper for short interest and advanced screening data
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import Dict, List, Optional
import time
import re
import config

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class FinvizScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://finviz.com"
        
    def get_screener_data(self, filters: Dict = None) -> List[Dict]:
        """Get data from FinViz screener with custom filters"""
        try:
            # Default filters for small cap stocks with high short interest
            default_filters = {
                'v': '111',  # Overview view
                'f': 'cap_smallover,sh_short_o10',  # Small cap, short ratio > 10%
                'o': '-volume'  # Sort by volume descending
            }
            
            if filters:
                default_filters.update(filters)
            
            # Build URL
            url = f"{self.base_url}/screener.ashx"
            params = '&'.join([f"{k}={v}" for k, v in default_filters.items()])
            full_url = f"{url}?{params}"
            
            response = self.session.get(full_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            stocks = []
            
            # Find the screener table
            table = soup.find('table', {'class': 'table-light'})
            if not table:
                logger.warning("Could not find FinViz screener table")
                return []
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 11:
                    try:
                        ticker = cells[1].text.strip()
                        company = cells[2].text.strip()
                        sector = cells[3].text.strip()
                        industry = cells[4].text.strip()
                        market_cap = self._parse_market_cap(cells[6].text.strip())
                        price = float(cells[8].text.strip())
                        change = self._parse_percentage(cells[9].text.strip())
                        volume = self._parse_volume(cells[10].text.strip())
                        
                        # Get additional metrics if available
                        short_float = 0
                        if len(cells) > 11:
                            short_float = self._parse_percentage(cells[11].text.strip())
                        
                        stock_data = {
                            'symbol': ticker,
                            'company_name': company,
                            'sector': sector,
                            'industry': industry,
                            'market_cap': market_cap,
                            'current_price': price,
                            'daily_change': change,
                            'volume': volume,
                            'short_percent_float': short_float,
                            'source': 'finviz',
                            'timestamp': int(time.time())
                        }
                        
                        # Filter by market cap
                        if config.SMALL_CAP_MIN <= market_cap <= config.SMALL_CAP_MAX:
                            stocks.append(stock_data)
                            
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error parsing FinViz row: {e}")
                        continue
            
            return stocks
            
        except Exception as e:
            logger.error(f"Error scraping FinViz screener: {e}")
            return []
    
    def get_short_squeeze_candidates(self) -> List[Dict]:
        """Get stocks with high short interest (potential squeeze candidates)"""
        try:
            # Filter for high short interest stocks
            filters = {
                'v': '111',
                'f': 'cap_smallover,sh_short_o20,sh_avgvol_o200',  # Small cap, short >20%, avg volume >200K
                'o': '-shortfloat'  # Sort by short float descending
            }
            
            return self.get_screener_data(filters)
            
        except Exception as e:
            logger.error(f"Error getting short squeeze candidates: {e}")
            return []
    
    def get_high_volume_movers(self) -> List[Dict]:
        """Get small caps with high volume and price movement"""
        try:
            filters = {
                'v': '111',
                'f': 'cap_smallover,ta_change_u5,ta_volume_o200',  # Small cap, change >5%, volume >200K
                'o': '-change'  # Sort by change descending
            }
            
            return self.get_screener_data(filters)
            
        except Exception as e:
            logger.error(f"Error getting high volume movers: {e}")
            return []
    
    def get_stock_details(self, symbol: str) -> Optional[Dict]:
        """Get detailed information for a specific stock"""
        try:
            url = f"{self.base_url}/quote.ashx?t={symbol}"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse the details table
            details = {}
            
            # Find all table cells with stock data
            tables = soup.find_all('table', {'class': 'snapshot-table2'})
            
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    for i in range(0, len(cells), 2):
                        if i + 1 < len(cells):
                            key = cells[i].text.strip()
                            value = cells[i + 1].text.strip()
                            details[key] = value
            
            # Extract key metrics
            stock_data = {
                'symbol': symbol,
                'market_cap': self._parse_market_cap(details.get('Market Cap', '0')),
                'short_percent_float': self._parse_percentage(details.get('Short Float', '0')),
                'short_ratio': self._parse_float(details.get('Short Ratio', '0')),
                'insider_own': self._parse_percentage(details.get('Insider Own', '0')),
                'insider_trans': self._parse_percentage(details.get('Insider Trans', '0')),
                'inst_own': self._parse_percentage(details.get('Inst Own', '0')),
                'inst_trans': self._parse_percentage(details.get('Inst Trans', '0')),
                'rsi': self._parse_float(details.get('RSI (14)', '0')),
                'beta': self._parse_float(details.get('Beta', '0')),
                'avg_volume': self._parse_volume(details.get('Avg Volume', '0')),
                'rel_volume': self._parse_float(details.get('Rel Volume', '0')),
                'pe_ratio': self._parse_float(details.get('P/E', '0')),
                'eps_growth': self._parse_percentage(details.get('EPS growth this year', '0')),
                'source': 'finviz_detail',
                'timestamp': int(time.time())
            }
            
            return stock_data
            
        except Exception as e:
            logger.error(f"Error getting FinViz details for {symbol}: {e}")
            return None
    
    def _parse_market_cap(self, text: str) -> int:
        """Parse market cap string to integer"""
        try:
            text = text.replace('$', '').replace(',', '').upper()
            if 'B' in text:
                return int(float(text.replace('B', '')) * 1_000_000_000)
            elif 'M' in text:
                return int(float(text.replace('M', '')) * 1_000_000)
            else:
                return int(float(text))
        except:
            return 0
    
    def _parse_percentage(self, text: str) -> float:
        """Parse percentage string to float"""
        try:
            return float(text.replace('%', '').replace('+', ''))
        except:
            return 0.0
    
    def _parse_float(self, text: str) -> float:
        """Parse float string"""
        try:
            return float(text.replace(',', ''))
        except:
            return 0.0
    
    def _parse_volume(self, text: str) -> int:
        """Parse volume string to integer"""
        try:
            text = text.replace(',', '').upper()
            if 'M' in text:
                return int(float(text.replace('M', '')) * 1_000_000)
            elif 'K' in text:
                return int(float(text.replace('K', '')) * 1_000)
            else:
                return int(float(text))
        except:
            return 0