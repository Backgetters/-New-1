#!/usr/bin/env python3
"""
Small Cap Stock Scanner Agent
Main entry point for the application

Usage:
    python main.py                  # Start web interface
    python main.py --scan-only      # Run single scan and exit
    python main.py --demo           # Use demo data
    python main.py --help           # Show help
"""
import argparse
import sys
import os
import logging
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import our modules
from stock_scanner import StockScanner
import config

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'data_sources',
        'analysis',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def run_single_scan(use_demo=False):
    """Run a single scan and print results"""
    print("🚀 Starting Small Cap Stock Scanner...")
    if use_demo:
        print("📊 DEMO MODE - Using sample data for demonstration")
    print("=" * 60)
    
    scanner = StockScanner()
    
    if use_demo:
        # Import and use demo data
        from demo_data import get_demo_stocks
        demo_stocks = get_demo_stocks()
        results = scanner.analyze_and_rank_stocks(demo_stocks)
    else:
        results = scanner.scan_stocks()
    
    # Display results
    print(f"\n📊 SCAN RESULTS")
    print(f"Total stocks analyzed: {results.get('total_stocks_analyzed', 0)}")
    print(f"Small caps found: {results.get('small_caps_found', 0)}")
    print(f"Market open: {'Yes' if results.get('market_open') else 'No'}")
    
    # Top Gainers
    top_gainers = results.get('top_gainers', [])
    if top_gainers:
        print(f"\n🎯 TOP {len(top_gainers)} GAINERS:")
        print("-" * 80)
        print(f"{'Symbol':<8} {'Company':<25} {'Price':<10} {'Change%':<10} {'Volume':<12} {'Market Cap':<15}")
        print("-" * 80)
        
        for stock in top_gainers:
            symbol = stock.get('symbol', 'N/A')[:7]
            company = stock.get('company_name', 'N/A')[:24]
            price = f"${stock.get('current_price', 0):.2f}"
            change = f"{stock.get('daily_change', 0):.1f}%"
            volume = f"{stock.get('volume', 0):,}"[:11]
            market_cap = f"${stock.get('market_cap', 0)/1e6:.0f}M"
            
            print(f"{symbol:<8} {company:<25} {price:<10} {change:<10} {volume:<12} {market_cap:<15}")
    
    # Short Squeeze Candidates
    squeeze_candidates = results.get('squeeze_candidates', [])
    if squeeze_candidates:
        print(f"\n💥 TOP {len(squeeze_candidates)} SHORT SQUEEZE CANDIDATES:")
        print("-" * 100)
        print(f"{'Symbol':<8} {'Score':<8} {'Risk':<12} {'Short%':<8} {'Days':<6} {'Price':<10} {'Change%':<10} {'Recommendation':<25}")
        print("-" * 100)
        
        for stock in squeeze_candidates:
            symbol = stock.get('symbol', 'N/A')[:7]
            score = f"{stock.get('squeeze_score', 0):.1f}"
            risk = stock.get('risk_level', 'N/A')[:11]
            short_pct = f"{stock.get('short_interest', 0):.1f}%"
            days = f"{stock.get('days_to_cover', 0):.1f}"
            price = f"${stock.get('current_price', 0):.2f}"
            change = f"{stock.get('daily_change', 0):.1f}%"
            recommendation = stock.get('recommendation', 'N/A')[:24]
            
            print(f"{symbol:<8} {score:<8} {risk:<12} {short_pct:<8} {days:<6} {price:<10} {change:<10} {recommendation:<25}")
    
    # Save results
    filename = scanner.save_results_to_file()
    if filename:
        print(f"\n💾 Results saved to: {filename}")
    
    print(f"\n✅ Scan completed successfully!")

def run_web_interface(use_demo=False):
    """Start the web interface"""
    print("🚀 Starting Small Cap Stock Scanner Web Interface...")
    if use_demo:
        print("📊 DEMO MODE - Using sample data for demonstration")
        config.USE_DEMO_DATA = True
    print(f"📱 Open your browser to: http://localhost:{config.WEB_PORT}")
    print("🔄 Background scanning will start automatically")
    print("💡 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        # Import and run the web interface
        from web_interface import app
        app.run_server(
            host=config.WEB_HOST,
            port=config.WEB_PORT,
            debug=config.DEBUG_MODE
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Small Cap Stock Scanner Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start web interface (default)
  python main.py --scan-only        # Run single scan and exit
  python main.py --demo             # Use demo data for testing
  python main.py --port 8080        # Start web interface on custom port
  
Features:
  - Real-time monitoring of small-cap stocks
  - Short squeeze detection algorithm
  - Sentiment analysis from news sources
  - Modern web dashboard with charts
  - Automated background scanning
  
Data Sources:
  - Yahoo Finance (free, no API key needed)
  - FinViz (free stock screener)
  - Financial news aggregation
  - Social media sentiment (optional)
        """
    )
    
    parser.add_argument(
        '--scan-only',
        action='store_true',
        help='Run a single scan and exit (no web interface)'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Use demo data for testing and demonstration'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=config.WEB_PORT,
        help=f'Port for web interface (default: {config.WEB_PORT})'
    )
    
    parser.add_argument(
        '--host',
        default=config.WEB_HOST,
        help=f'Host for web interface (default: {config.WEB_HOST})'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default=config.LOG_LEVEL,
        help=f'Set log level (default: {config.LOG_LEVEL})'
    )
    
    args = parser.parse_args()
    
    # Update config with command line arguments
    config.WEB_PORT = args.port
    config.WEB_HOST = args.host
    config.LOG_LEVEL = args.log_level
    
    if args.debug:
        config.DEBUG_MODE = True
        config.LOG_LEVEL = 'DEBUG'
    
    # Setup
    setup_logging()
    create_directories()
    
    # Display banner
    print("=" * 60)
    print("🚀 SMALL CAP STOCK SCANNER AGENT")
    print("🎯 Finding Short Squeeze Opportunities")
    if args.demo:
        print("📊 DEMO MODE ENABLED")
    print("=" * 60)
    print(f"📊 Scanning small caps: ${config.SMALL_CAP_MIN/1e6:.0f}M - ${config.SMALL_CAP_MAX/1e6:.0f}M market cap")
    print(f"💥 Min short interest: {config.MIN_SHORT_INTEREST}%")
    print(f"📈 Min daily gain: {config.MIN_DAILY_GAIN}%")
    print(f"⏰ Update interval: {config.DATA_UPDATE_INTERVAL//60} minutes")
    print("=" * 60)
    
    # Run based on mode
    if args.scan_only:
        run_single_scan(use_demo=args.demo)
    else:
        run_web_interface(use_demo=args.demo)

if __name__ == "__main__":
    main()