"""
Configuration file for the Stock Scanner Agent
"""
import os
from datetime import time

# Market Configuration
SMALL_CAP_MIN = 300_000_000  # $300M minimum market cap
SMALL_CAP_MAX = 2_000_000_000  # $2B maximum market cap

# Short Squeeze Detection Criteria
MIN_SHORT_INTEREST = 10.0  # Minimum short interest percentage
MIN_DAYS_TO_COVER = 3.0    # Minimum days to cover ratio
MIN_COST_TO_BORROW = 20.0  # Minimum cost to borrow percentage

# Price Movement Criteria
MIN_DAILY_GAIN = 5.0       # Minimum daily gain percentage for consideration
MIN_VOLUME_RATIO = 2.0     # Minimum volume vs average volume ratio

# Update Intervals
DATA_UPDATE_INTERVAL = 300  # 5 minutes in seconds
NEWS_UPDATE_INTERVAL = 900  # 15 minutes in seconds

# Market Hours (EST)
MARKET_OPEN = time(9, 30)
MARKET_CLOSE = time(16, 0)

# Demo Mode
USE_DEMO_DATA = False       # Set to True to use demo data instead of live data

# Data Sources Configuration
DATA_SOURCES = {
    'yahoo_finance': {
        'enabled': True,
        'priority': 1,
        'rate_limit': 2000  # requests per hour
    },
    'finviz': {
        'enabled': True,
        'priority': 2,
        'rate_limit': 100
    },
    'reddit_wsb': {
        'enabled': True,
        'priority': 3,
        'rate_limit': 60
    },
    'financial_news': {
        'enabled': True,
        'priority': 4,
        'rate_limit': 1000
    }
}

# API Keys (optional - set in environment variables)
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY', '')

# Web Interface
WEB_HOST = '0.0.0.0'
WEB_PORT = 8050
DEBUG_MODE = True

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'stock_scanner.log'

# Database (if using SQLite for caching)
DATABASE_PATH = 'stock_scanner.db'

# Top Lists Configuration
TOP_GAINERS_COUNT = 25
TOP_SQUEEZE_CANDIDATES = 10

# Sentiment Analysis
SENTIMENT_KEYWORDS = {
    'positive': ['bullish', 'moon', 'squeeze', 'breakout', 'rally', 'buy', 'calls', 'pump'],
    'negative': ['bearish', 'crash', 'dump', 'puts', 'short', 'sell', 'drop']
}

# News Sources
NEWS_SOURCES = [
    'yahoo.com',
    'marketwatch.com',
    'seekingalpha.com',
    'benzinga.com',
    'zacks.com',
    'fool.com'
]

# Reddit Subreddits
REDDIT_SUBREDDITS = [
    'wallstreetbets',
    'stocks',
    'SecurityAnalysis',
    'investing',
    'pennystocks'
]