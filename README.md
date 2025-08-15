# 🚀 Small Cap Stock Scanner Agent

A comprehensive stock scanner that identifies small-cap stocks with short squeeze potential and strong movement opportunities by scraping multiple free data sources. Built with Python, featuring real-time monitoring, advanced analytics, and a modern web dashboard.

## ✨ Features

- **🎯 Real-time Stock Monitoring**: Tracks small-cap stocks during market hours
- **💥 Short Squeeze Detection**: Advanced algorithm identifies stocks with high squeeze potential
- **📈 Top Gainers Tracking**: Shows top 25 daily gainers with detailed metrics
- **📰 News Sentiment Analysis**: Analyzes financial news for movement catalysts
- **🖥️ Modern Web Dashboard**: Beautiful, responsive interface with real-time charts
- **🔄 Automated Updates**: Refreshes data every 5 minutes during market hours
- **📊 Advanced Analytics**: Sector analysis, performance charts, and trend visualization
- **🎮 Demo Mode**: Test with realistic sample data without live market dependency

## 🔍 Short Squeeze Detection Algorithm

Our proprietary algorithm analyzes multiple factors to score squeeze potential (0-100):

- **Short Interest %** (25% weight) - Higher short interest = higher squeeze potential
- **Days to Cover** (20% weight) - Time required to cover all short positions
- **Cost to Borrow** (15% weight) - Estimated borrowing cost for short sellers
- **Volume Spike** (15% weight) - Current volume vs average volume
- **Price Momentum** (10% weight) - Recent price movement strength
- **Float Size** (10% weight) - Smaller float = easier to squeeze
- **Insider Ownership** (5% weight) - Higher insider ownership reduces available float

### Risk Levels:
- **🔥 Very High (70+)**: Extreme squeeze potential - watch closely
- **⚡ High (50-69)**: Strong squeeze setup - monitor activity
- **📊 Medium (30-49)**: Moderate potential - worth investigating
- **💭 Low (<30)**: Limited squeeze potential

## 📡 Data Sources

- **Yahoo Finance** - Stock prices, volumes, basic financial data (free, no API key needed)
- **FinViz** - Advanced screener data, short interest, financial metrics (free)
- **Financial News** - Sentiment analysis from major financial news sources
- **Social Media** - Reddit WallStreetBets sentiment (optional, requires API keys)

## 📊 Key Metrics Tracked

- **Market Cap**: Filtered for small caps ($300M - $2B)
- **Short Interest %**: Percentage of float sold short
- **Days to Cover**: Average daily volume / shares short
- **Daily Change %**: Current session price movement
- **Volume Ratio**: Current volume vs 20-day average
- **News Sentiment**: Aggregated sentiment score from news analysis
- **Technical Indicators**: RSI, Beta, 52-week ranges

## 🚀 Quick Start

### Method 1: Using the convenient launcher script
```bash
# Start web interface
./run.sh

# Start with demo data
./run.sh demo

# Run a quick scan
./run.sh scan

# Install dependencies
./run.sh install
```

### Method 2: Direct Python execution
```bash
# Install dependencies
pip install -r requirements.txt

# Start web interface
python main.py

# Start with demo data (recommended for testing)
python main.py --demo

# Run single scan and exit
python main.py --scan-only

# Run demo scan
python main.py --scan-only --demo
```

## 🖥️ Web Interface

Once running, open your browser to `http://localhost:8050` to access:

### 📈 Top Gainers Tab
- Real-time list of top 25 small-cap gainers
- Sortable table with price, change %, volume, market cap
- Color-coded performance indicators

### 💥 Short Squeeze Tab  
- Top 10 stocks with highest squeeze potential
- Detailed squeeze scores and risk levels
- Actionable recommendations with emoji indicators

### 🎯 Overall Rankings Tab
- Comprehensive ranking combining all factors
- Composite scores weighing squeeze potential, momentum, volume, and sentiment
- Best overall opportunities for further research

### 📊 Analytics Tab
- Sector distribution pie charts
- Performance visualization
- Volume and momentum analysis

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Market cap range for small caps
SMALL_CAP_MIN = 300_000_000   # $300M
SMALL_CAP_MAX = 2_000_000_000 # $2B

# Screening criteria
MIN_SHORT_INTEREST = 10.0     # Minimum short interest %
MIN_DAILY_GAIN = 5.0          # Minimum daily gain %
MIN_VOLUME_RATIO = 2.0        # Minimum volume ratio

# Update intervals
DATA_UPDATE_INTERVAL = 300    # 5 minutes
```

## 🔧 Advanced Usage

### Command Line Options
```bash
python main.py --help                    # Show all options
python main.py --port 8080               # Custom port
python main.py --host 0.0.0.0            # Custom host
python main.py --debug                   # Enable debug mode
python main.py --log-level DEBUG         # Set log level
```

### Environment Variables (Optional)
```bash
# Copy example env file
cp .env.example .env

# Edit with your API keys (all optional)
NEWSAPI_KEY=your_key_here
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret
ALPHA_VANTAGE_KEY=your_av_key
```

## 📁 Project Structure

```
stock_scanner/
├── main.py                 # Main entry point
├── config.py              # Configuration settings
├── stock_scanner.py       # Core scanning engine
├── web_interface.py       # Dash web application
├── demo_data.py           # Demo data for testing
├── requirements.txt       # Python dependencies
├── run.sh                # Convenient launcher script
├── data_sources/          # Data scraping modules
│   ├── yahoo_finance.py   # Yahoo Finance scraper
│   └── finviz_scraper.py  # FinViz scraper
└── analysis/              # Analysis algorithms
    ├── short_squeeze_detector.py  # Squeeze detection
    └── sentiment_analyzer.py      # News sentiment analysis
```

## 🧪 Testing & Demo Mode

The application includes a comprehensive demo mode with realistic sample data:

```bash
# Test with demo data (no internet required)
python main.py --demo

# Quick demo scan
python main.py --scan-only --demo
```

Demo mode includes:
- 10 realistic small-cap stocks with varied profiles
- Different sectors (biotech, tech, telecom, etc.)
- Range of short interest levels (12% - 40%)
- Varied price movements and volume spikes
- Simulated news sentiment data

## 🐛 Troubleshooting

### Common Issues:

1. **"No data found"** - Market might be closed, try demo mode: `python main.py --demo`
2. **Import errors** - Install dependencies: `pip install -r requirements.txt`
3. **Permission denied** - Make run script executable: `chmod +x run.sh`
4. **Port already in use** - Try different port: `python main.py --port 8051`

### Debug Mode:
```bash
python main.py --debug --log-level DEBUG
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**IMPORTANT**: This tool is for educational and informational purposes only. It is **NOT** financial advice. 

- Stock trading involves significant risk and can result in financial loss
- Past performance does not guarantee future results
- Always conduct your own research and due diligence
- Consider consulting with a qualified financial advisor
- The authors are not responsible for any trading losses

**Use at your own risk. Trade responsibly.**

## 🙏 Acknowledgments

- Yahoo Finance for free financial data
- FinViz for advanced stock screening capabilities
- The Python community for excellent libraries
- Contributors and testers who helped improve this tool

---

### 🌟 Star this repository if you find it useful!

Made with ❤️ for the trading community
