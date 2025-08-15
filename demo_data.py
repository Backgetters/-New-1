"""
Demo data for testing and demonstration
"""
import time
import random

def get_demo_stocks():
    """Generate demo stock data for testing"""
    
    demo_stocks = [
        {
            'symbol': 'GALT',
            'company_name': 'Galectin Therapeutics Inc',
            'current_price': 4.25,
            'daily_change': 12.5,
            'volume': 2500000,
            'avg_volume': 800000,
            'volume_ratio': 3.1,
            'market_cap': 320000000,
            'sector': 'Healthcare',
            'industry': 'Biotechnology',
            'short_ratio': 8.5,
            'short_percent_float': 18.4,
            'beta': 1.8,
            'fifty_two_week_high': 8.50,
            'fifty_two_week_low': 1.20,
            'pe_ratio': 0,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'BYND',
            'company_name': 'Beyond Meat Inc',
            'current_price': 6.80,
            'daily_change': 8.3,
            'volume': 4200000,
            'avg_volume': 1500000,
            'volume_ratio': 2.8,
            'market_cap': 450000000,
            'sector': 'Consumer Defensive',
            'industry': 'Food Processing',
            'short_ratio': 12.3,
            'short_percent_float': 40.5,
            'beta': 2.1,
            'fifty_two_week_high': 15.20,
            'fifty_two_week_low': 4.50,
            'pe_ratio': -5.2,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'OCGN',
            'company_name': 'Ocugen Inc',
            'current_price': 1.85,
            'daily_change': 15.6,
            'volume': 8900000,
            'avg_volume': 2100000,
            'volume_ratio': 4.2,
            'market_cap': 420000000,
            'sector': 'Healthcare',
            'industry': 'Biotechnology',
            'short_ratio': 6.8,
            'short_percent_float': 24.3,
            'beta': 2.5,
            'fifty_two_week_high': 4.80,
            'fifty_two_week_low': 0.90,
            'pe_ratio': 0,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'MVIS',
            'company_name': 'MicroVision Inc',
            'current_price': 3.45,
            'daily_change': 9.2,
            'volume': 1850000,
            'avg_volume': 650000,
            'volume_ratio': 2.8,
            'market_cap': 680000000,
            'sector': 'Technology',
            'industry': 'Electronic Components',
            'short_ratio': 7.2,
            'short_percent_float': 26.0,
            'beta': 1.9,
            'fifty_two_week_high': 8.90,
            'fifty_two_week_low': 1.80,
            'pe_ratio': 0,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'LAZR',
            'company_name': 'Luminar Technologies Inc',
            'current_price': 2.15,
            'daily_change': 14.1,
            'volume': 3200000,
            'avg_volume': 950000,
            'volume_ratio': 3.4,
            'market_cap': 850000000,
            'sector': 'Technology',
            'industry': 'Electronic Components',
            'short_ratio': 9.8,
            'short_percent_float': 32.1,
            'beta': 2.3,
            'fifty_two_week_high': 6.20,
            'fifty_two_week_low': 1.40,
            'pe_ratio': 0,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'CIFR',
            'company_name': 'Cipher Mining Inc',
            'current_price': 3.44,
            'daily_change': 15.05,
            'volume': 22160000,
            'avg_volume': 4200000,
            'volume_ratio': 5.3,
            'market_cap': 1150000000,
            'sector': 'Technology',
            'industry': 'Information Technology Services',
            'short_ratio': 5.4,
            'short_percent_float': 16.8,
            'beta': 2.8,
            'fifty_two_week_high': 8.30,
            'fifty_two_week_low': 1.90,
            'pe_ratio': 0,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'WVE',
            'company_name': 'Wave Life Sciences Ltd',
            'current_price': 8.19,
            'daily_change': 53.37,
            'volume': 15640000,
            'avg_volume': 1200000,
            'volume_ratio': 13.0,
            'market_cap': 977000000,
            'sector': 'Healthcare',
            'industry': 'Biotechnology',
            'short_ratio': 3.8,
            'short_percent_float': 12.5,
            'beta': 1.7,
            'fifty_two_week_high': 12.50,
            'fifty_two_week_low': 2.10,
            'pe_ratio': 0,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'ATUS',
            'company_name': 'Altice USA Inc',
            'current_price': 2.44,
            'daily_change': 15.64,
            'volume': 6450000,
            'avg_volume': 2100000,
            'volume_ratio': 3.1,
            'market_cap': 1050000000,
            'sector': 'Communication Services',
            'industry': 'Telecom Services',
            'short_ratio': 4.2,
            'short_percent_float': 14.2,
            'beta': 1.4,
            'fifty_two_week_high': 4.80,
            'fifty_two_week_low': 1.90,
            'pe_ratio': -2.1,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'PACB',
            'company_name': 'Pacific Biosciences of California Inc',
            'current_price': 1.25,
            'daily_change': 7.8,
            'volume': 2800000,
            'avg_volume': 1100000,
            'volume_ratio': 2.5,
            'market_cap': 380000000,
            'sector': 'Healthcare',
            'industry': 'Medical Devices',
            'short_ratio': 11.2,
            'short_percent_float': 17.0,
            'beta': 2.4,
            'fifty_two_week_high': 3.80,
            'fifty_two_week_low': 0.80,
            'pe_ratio': 0,
            'timestamp': int(time.time()),
            'source': 'demo'
        },
        {
            'symbol': 'AAOI',
            'company_name': 'Applied Optoelectronics Inc',
            'current_price': 15.98,
            'daily_change': 13.66,
            'volume': 5520000,
            'avg_volume': 850000,
            'volume_ratio': 6.5,
            'market_cap': 653000000,
            'sector': 'Technology',
            'industry': 'Electronic Components',
            'short_ratio': 8.9,
            'short_percent_float': 22.3,
            'beta': 2.1,
            'fifty_two_week_high': 28.50,
            'fifty_two_week_low': 8.20,
            'pe_ratio': 0,
            'timestamp': int(time.time()),
            'source': 'demo'
        }
    ]
    
    # Add some randomization to make it more realistic
    for stock in demo_stocks:
        # Add small random variations
        price_variation = random.uniform(-0.05, 0.05)
        stock['current_price'] *= (1 + price_variation)
        stock['current_price'] = round(stock['current_price'], 2)
        
        change_variation = random.uniform(-1, 1)
        stock['daily_change'] += change_variation
        stock['daily_change'] = round(stock['daily_change'], 2)
        
        volume_variation = random.uniform(0.8, 1.2)
        stock['volume'] = int(stock['volume'] * volume_variation)
        
        # Add sentiment data
        sentiments = ['positive', 'negative', 'neutral']
        stock['sentiment'] = {
            'overall_sentiment': random.choice(sentiments),
            'sentiment_score': random.uniform(-0.5, 0.8),
            'news_sentiment': {
                'sentiment': random.choice(sentiments),
                'confidence': random.randint(20, 80),
                'articles_count': random.randint(1, 5)
            }
        }
    
    return demo_stocks

def get_demo_news():
    """Generate demo news data"""
    news_items = [
        {
            'title': 'Biotech sector sees renewed interest from investors',
            'summary': 'Small-cap biotechnology companies are gaining attention as potential takeover targets',
            'sentiment': 'positive',
            'timestamp': int(time.time()) - 3600
        },
        {
            'title': 'Short interest reaches multi-year highs in several small caps',
            'summary': 'Institutional investors increase short positions in volatile small-cap stocks',
            'sentiment': 'negative', 
            'timestamp': int(time.time()) - 7200
        },
        {
            'title': 'Technology stocks show strong momentum amid sector rotation',
            'summary': 'Small-cap tech names benefit from rotation out of large-cap growth stocks',
            'sentiment': 'positive',
            'timestamp': int(time.time()) - 10800
        }
    ]
    
    return news_items