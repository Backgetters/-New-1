"""
Sentiment Analysis Module
Analyzes news articles and social media for stock sentiment
"""
import requests
from textblob import TextBlob
import re
import logging
from typing import Dict, List, Optional
import time
from datetime import datetime, timedelta
import config

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def analyze_stock_sentiment(self, symbol: str) -> Dict:
        """Analyze overall sentiment for a stock"""
        try:
            # Get news sentiment
            news_sentiment = self.analyze_news_sentiment(symbol)
            
            # Get Reddit sentiment (if available)
            reddit_sentiment = self.analyze_reddit_sentiment(symbol)
            
            # Combine sentiments
            overall_sentiment = self._combine_sentiments([news_sentiment, reddit_sentiment])
            
            return {
                'symbol': symbol,
                'overall_sentiment': overall_sentiment,
                'news_sentiment': news_sentiment,
                'reddit_sentiment': reddit_sentiment,
                'sentiment_score': self._calculate_sentiment_score(overall_sentiment),
                'timestamp': int(time.time())
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {symbol}: {e}")
            return {'symbol': symbol, 'sentiment_score': 0}
    
    def analyze_news_sentiment(self, symbol: str) -> Dict:
        """Analyze sentiment from financial news"""
        try:
            # Try multiple news sources
            articles = []
            
            # Yahoo Finance news
            yahoo_articles = self._get_yahoo_news(symbol)
            articles.extend(yahoo_articles)
            
            # Google News (if available)
            google_articles = self._get_google_news(symbol)
            articles.extend(google_articles)
            
            if not articles:
                return {'sentiment': 'neutral', 'confidence': 0, 'articles_count': 0}
            
            # Analyze sentiment of all articles
            sentiments = []
            positive_keywords = 0
            negative_keywords = 0
            
            for article in articles:
                text = f"{article.get('title', '')} {article.get('summary', '')}"
                
                # TextBlob sentiment analysis
                blob = TextBlob(text)
                sentiment_score = blob.sentiment.polarity
                sentiments.append(sentiment_score)
                
                # Keyword analysis
                text_lower = text.lower()
                for keyword in config.SENTIMENT_KEYWORDS['positive']:
                    positive_keywords += text_lower.count(keyword)
                
                for keyword in config.SENTIMENT_KEYWORDS['negative']:
                    negative_keywords += text_lower.count(keyword)
            
            # Calculate overall sentiment
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            
            # Determine sentiment category
            if avg_sentiment > 0.1 or positive_keywords > negative_keywords * 2:
                sentiment = 'positive'
            elif avg_sentiment < -0.1 or negative_keywords > positive_keywords * 2:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Calculate confidence based on number of articles and keyword matches
            confidence = min((len(articles) * 10 + abs(positive_keywords - negative_keywords) * 5), 100)
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'articles_count': len(articles),
                'sentiment_score': avg_sentiment,
                'positive_keywords': positive_keywords,
                'negative_keywords': negative_keywords,
                'recent_articles': articles[:3]  # Include top 3 articles
            }
            
        except Exception as e:
            logger.error(f"Error analyzing news sentiment for {symbol}: {e}")
            return {'sentiment': 'neutral', 'confidence': 0, 'articles_count': 0}
    
    def analyze_reddit_sentiment(self, symbol: str) -> Dict:
        """Analyze sentiment from Reddit discussions"""
        try:
            # Note: This would require Reddit API credentials
            # For now, we'll return a placeholder implementation
            
            # In a full implementation, this would:
            # 1. Search Reddit for mentions of the stock symbol
            # 2. Analyze post titles and comments
            # 3. Count positive/negative sentiment indicators
            # 4. Return aggregated sentiment
            
            return {
                'sentiment': 'neutral',
                'confidence': 0,
                'mentions_count': 0,
                'sentiment_score': 0
            }
            
        except Exception as e:
            logger.error(f"Error analyzing Reddit sentiment for {symbol}: {e}")
            return {'sentiment': 'neutral', 'confidence': 0, 'mentions_count': 0}
    
    def _get_yahoo_news(self, symbol: str) -> List[Dict]:
        """Get news articles from Yahoo Finance"""
        try:
            url = f"https://finance.yahoo.com/quote/{symbol}/news"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            # Parse HTML to extract news (simplified implementation)
            # In production, you'd use a proper HTML parser
            articles = []
            
            # This is a simplified extraction - in reality you'd parse the HTML properly
            content = response.text
            
            # Look for news-related patterns (this is very basic)
            if 'earnings' in content.lower():
                articles.append({
                    'title': f"{symbol} Earnings Report",
                    'summary': "Company reported quarterly earnings",
                    'source': 'yahoo',
                    'timestamp': int(time.time())
                })
            
            if 'upgrade' in content.lower() or 'buy' in content.lower():
                articles.append({
                    'title': f"{symbol} Analyst Upgrade",
                    'summary': "Analysts upgraded the stock",
                    'source': 'yahoo',
                    'timestamp': int(time.time())
                })
            
            return articles
            
        except Exception as e:
            logger.error(f"Error getting Yahoo news for {symbol}: {e}")
            return []
    
    def _get_google_news(self, symbol: str) -> List[Dict]:
        """Get news articles from Google News"""
        try:
            # Google News search for stock symbol
            query = f"{symbol} stock news"
            url = f"https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            # Parse results (simplified)
            articles = []
            
            # In a real implementation, you'd properly parse the Google News HTML
            # This is just a placeholder
            content = response.text.lower()
            
            if symbol.lower() in content:
                articles.append({
                    'title': f"{symbol} in the News",
                    'summary': "Recent news coverage",
                    'source': 'google',
                    'timestamp': int(time.time())
                })
            
            return articles
            
        except Exception as e:
            logger.error(f"Error getting Google news for {symbol}: {e}")
            return []
    
    def _combine_sentiments(self, sentiments: List[Dict]) -> str:
        """Combine multiple sentiment analyses"""
        try:
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for sentiment_data in sentiments:
                sentiment = sentiment_data.get('sentiment', 'neutral')
                confidence = sentiment_data.get('confidence', 0)
                
                # Weight by confidence
                weight = max(confidence / 100, 0.1)
                
                if sentiment == 'positive':
                    positive_count += weight
                elif sentiment == 'negative':
                    negative_count += weight
                else:
                    neutral_count += weight
            
            # Determine overall sentiment
            if positive_count > negative_count and positive_count > neutral_count:
                return 'positive'
            elif negative_count > positive_count and negative_count > neutral_count:
                return 'negative'
            else:
                return 'neutral'
                
        except Exception as e:
            logger.error(f"Error combining sentiments: {e}")
            return 'neutral'
    
    def _calculate_sentiment_score(self, sentiment: str) -> float:
        """Convert sentiment to numerical score (-1 to 1)"""
        sentiment_scores = {
            'positive': 0.7,
            'negative': -0.7,
            'neutral': 0.0
        }
        return sentiment_scores.get(sentiment, 0.0)
    
    def get_trending_stocks_sentiment(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get sentiment analysis for multiple stocks"""
        try:
            sentiments = {}
            
            for symbol in symbols:
                try:
                    sentiment = self.analyze_stock_sentiment(symbol)
                    sentiments[symbol] = sentiment
                    time.sleep(0.5)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error getting sentiment for {symbol}: {e}")
                    sentiments[symbol] = {'sentiment_score': 0}
            
            return sentiments
            
        except Exception as e:
            logger.error(f"Error getting trending stocks sentiment: {e}")
            return {}