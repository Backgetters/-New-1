#!/bin/bash

# Small Cap Stock Scanner Agent
# Convenient launcher script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    exit 1
fi

# Function to install dependencies
install_deps() {
    print_info "Installing Python dependencies..."
    if pip install --break-system-packages -r requirements.txt > /dev/null 2>&1; then
        print_success "Dependencies installed successfully"
    else
        print_warning "Some packages may already be installed"
    fi
}

# Function to show usage
show_usage() {
    echo ""
    echo "🚀 Small Cap Stock Scanner Agent"
    echo "=================================="
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  web         Start web interface (default)"
    echo "  demo        Start web interface with demo data"
    echo "  scan        Run single scan and exit"
    echo "  scan-demo   Run single scan with demo data"
    echo "  install     Install/update dependencies"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0          # Start web interface"
    echo "  $0 demo     # Start with demo data"
    echo "  $0 scan     # Quick scan"
    echo ""
}

# Parse command line arguments
case "${1:-web}" in
    "web")
        print_info "Starting Stock Scanner Web Interface..."
        print_info "Open your browser to: http://localhost:8050"
        python3 main.py
        ;;
    "demo")
        print_info "Starting Stock Scanner in Demo Mode..."
        print_info "Open your browser to: http://localhost:8050"
        python3 main.py --demo
        ;;
    "scan")
        print_info "Running single stock scan..."
        python3 main.py --scan-only
        ;;
    "scan-demo")
        print_info "Running demo stock scan..."
        python3 main.py --scan-only --demo
        ;;
    "install")
        install_deps
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        print_error "Unknown option: $1"
        show_usage
        exit 1
        ;;
esac