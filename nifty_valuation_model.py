
"""
THE MOUNTAIN PATH - WORLD OF FINANCE
Dynamic Relative Valuation Model for Indian Nifty Stocks
Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking

Relative Valuation Framework:
- Earnings Multiple (P/E)
- Book Value Multiple (P/B)
- Sales Multiple (P/S)
- Enterprise Value Multiples (EV/EBITDA, EV/Revenue)
- Dividend Yield
- PEG Ratio
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import comparable multiples module
try:
    from comparable_multiples import get_sector_multiples, calculate_implied_valuation, get_valuation_summary
except ImportError:
    st.warning("⚠️ Comparable multiples module not found. Some features may be unavailable.")

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="Nifty Stock Analysis - Relative Valuation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Mountain Path Branding
st.markdown("""
<style>
    :root {
        --dark-blue: #003366;
        --light-blue: #ADD8E6;
        --gold: #FFD700;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    /* SIDEBAR STYLING - Professional Dark Navy */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a4d7a 0%, #0d2d4d 100%) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 20px;
    }
    
    /* Sidebar Text */
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p {
        color: #ffffff !important;
    }
    
    /* Sidebar Dividers */
    [data-testid="stSidebar"] hr {
        border-color: #4a7ba7 !important;
        margin: 20px 0 !important;
    }
    
    /* Sidebar Title Styling */
    .sidebar-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 2px solid #4a7ba7;
    }
    
    .sidebar-subtitle {
        color: #b3d9ff;
        font-size: 12px;
        margin-bottom: 15px;
        font-style: italic;
    }
    
    .sidebar-section {
        margin-bottom: 25px;
    }
    
    .sidebar-option {
        color: #ffffff;
        font-size: 14px;
        margin: 8px 0;
    }
    
    .sidebar-author {
        background-color: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 6px;
        margin-top: 20px;
        color: #ffffff;
        text-align: center;
        border-left: 3px solid #FFD700;
    }
    
    .sidebar-author-name {
        font-weight: bold;
        color: #FFD700;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .sidebar-author-text {
        color: #b3d9ff;
        font-size: 12px;
        line-height: 1.6;
    }
    
    .sidebar-button {
        background-color: #1e5a96 !important;
        color: #FFD700 !important;
        border: 2px solid #FFD700 !important;
        padding: 10px 15px !important;
        border-radius: 6px !important;
        text-align: center !important;
        font-weight: bold !important;
        margin-top: 15px !important;
        width: 100% !important;
    }
    
    .sidebar-button:hover {
        background-color: #2d73b3 !important;
    }
    
    .stTitle {
        color: #003366;
        font-weight: bold;
        border-bottom: 3px solid #003366;
        padding-bottom: 10px;
    }
    
    .header-box {
        background: linear-gradient(135deg, #003366 0%, #004d7a 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background-color: white;
        padding: 20px;
        border-left: 4px solid #003366;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-title {
        color: #003366;
        font-weight: bold;
        font-size: 14px;
    }
    
    .metric-value {
        color: #003366;
        font-size: 24px;
        font-weight: bold;
        margin-top: 5px;
    }
    
    .positive {
        color: #28a745;
    }
    
    .negative {
        color: #dc3545;
    }
    
    .neutral {
        color: #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# NIFTY 50 STOCKS DATABASE WITH SECTOR CLASSIFICATION
# ============================================================================
NIFTY_50_DATA = {
    'RELIANCE.NS': {'Company': 'Reliance Industries', 'Sector': 'Energy & Utilities'},
    'TCS.NS': {'Company': 'Tata Consultancy Services', 'Sector': 'IT & Software'},
    'HDFCBANK.NS': {'Company': 'HDFC Bank', 'Sector': 'Financial Services'},
    'INFY.NS': {'Company': 'Infosys', 'Sector': 'IT & Software'},
    'ICICIBANK.NS': {'Company': 'ICICI Bank', 'Sector': 'Financial Services'},
    'HINDUNILVR.NS': {'Company': 'Hindustan Unilever', 'Sector': 'Consumer & FMCG'},
    'AXISBANK.NS': {'Company': 'Axis Bank', 'Sector': 'Financial Services'},
    'LT.NS': {'Company': 'Larsen & Toubro', 'Sector': 'Infrastructure & Construction'},
    'WIPRO.NS': {'Company': 'Wipro', 'Sector': 'IT & Software'},
    'BAJAJFINSV.NS': {'Company': 'Bajaj Finserv', 'Sector': 'Financial Services'},
    'MARUTI.NS': {'Company': 'Maruti Suzuki', 'Sector': 'Automobiles'},
    'HCLTECH.NS': {'Company': 'HCL Technologies', 'Sector': 'IT & Software'},
    'SUNPHARMA.NS': {'Company': 'Sun Pharmaceutical', 'Sector': 'Pharmaceuticals'},
    'JSWSTEEL.NS': {'Company': 'JSW Steel', 'Sector': 'Metals & Mining'},
    'TATASTEEL.NS': {'Company': 'Tata Steel', 'Sector': 'Metals & Mining'},
    'POWERGRID.NS': {'Company': 'Power Grid Corp', 'Sector': 'Energy & Utilities'},
    'IOCL.NS': {'Company': 'Indian Oil Corp', 'Sector': 'Energy & Utilities'},
    'BHARTIARTL.NS': {'Company': 'Bharti Airtel', 'Sector': 'Telecom'},
    'ULTRACEMCO.NS': {'Company': 'UltraCem Co', 'Sector': 'Construction & Materials'},
    'TITAN.NS': {'Company': 'Titan Company', 'Sector': 'Consumer & FMCG'},
    'NTPC.NS': {'Company': 'NTPC', 'Sector': 'Energy & Utilities'},
    'ADANIPORTS.NS': {'Company': 'Adani Ports', 'Sector': 'Infrastructure & Construction'},
    'BAJAJHLDNG.NS': {'Company': 'Bajaj Holdings', 'Sector': 'Holding Companies'},
    'SBILIFE.NS': {'Company': 'SBI Life', 'Sector': 'Financial Services'},
    'HEROMOTOCO.NS': {'Company': 'Hero MotoCorp', 'Sector': 'Automobiles'},
    'INDUSIND.NS': {'Company': 'IndusInd Bank', 'Sector': 'Financial Services'},
    'TECHM.NS': {'Company': 'Tech Mahindra', 'Sector': 'IT & Software'},
    'SBIN.NS': {'Company': 'State Bank of India', 'Sector': 'Financial Services'},
    'NESTLEIND.NS': {'Company': 'Nestle India', 'Sector': 'Consumer & FMCG'},
    'ASIANPAINT.NS': {'Company': 'Asian Paints', 'Sector': 'Consumer & FMCG'},
    'LTTS.NS': {'Company': 'LT Technology Services', 'Sector': 'IT & Software'},
    'TIINDIA.NS': {'Company': 'Titanium International', 'Sector': 'Consumer & FMCG'},
    'COALINDIA.NS': {'Company': 'Coal India', 'Sector': 'Metals & Mining'},
    'MVMT.NS': {'Company': 'Marico', 'Sector': 'Consumer & FMCG'},
    'HDFCLIFE.NS': {'Company': 'HDFC Life', 'Sector': 'Financial Services'},
    'BAJAJELECTRI.NS': {'Company': 'Bajaj Electricals', 'Sector': 'Consumer & FMCG'},
    'GAIL.NS': {'Company': 'GAIL', 'Sector': 'Energy & Utilities'},
    'ONGC.NS': {'Company': 'ONGC', 'Sector': 'Energy & Utilities'},
    'BOSCHIND.NS': {'Company': 'Bosch India', 'Sector': 'Automobiles'},
    'DIVISLAB.NS': {'Company': 'Divi Lab', 'Sector': 'Pharmaceuticals'},
    'CIPLA.NS': {'Company': 'Cipla', 'Sector': 'Pharmaceuticals'},
    'DRREDDY.NS': {'Company': 'Dr Reddy Labs', 'Sector': 'Pharmaceuticals'},
    'BIOCON.NS': {'Company': 'Biocon', 'Sector': 'Pharmaceuticals'},
    'BAJAJ-AUTO.NS': {'Company': 'Bajaj Auto', 'Sector': 'Automobiles'},
    'M&MFIN.NS': {'Company': 'M&M Finance', 'Sector': 'Financial Services'},
    'MAHSCOOTER.NS': {'Company': 'Mahindra & Mahindra', 'Sector': 'Automobiles'},
    'LUPIN.NS': {'Company': 'Lupin', 'Sector': 'Pharmaceuticals'},
    'APOLLOHOSP.NS': {'Company': 'Apollo Hospitals', 'Sector': 'Healthcare'},
}

# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, period='1y'):
    """Fetch historical price data for a stock"""
    try:
        data = yf.download(ticker, period=period, progress=False)
        return data
    except:
        return None

@st.cache_data(ttl=3600)
def fetch_stock_info(ticker):
    """Fetch current stock information"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info
    except:
        return None

def calculate_valuation_metrics(ticker, info):
    """Calculate relative valuation metrics"""
    metrics = {}
    
    try:
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        
        # P/E Ratio
        pe_ratio = info.get('trailingPE', None)
        metrics['P/E Ratio'] = pe_ratio
        
        # P/B Ratio
        pb_ratio = info.get('priceToBook', None)
        metrics['P/B Ratio'] = pb_ratio
        
        # Price to Sales
        ps_ratio = info.get('priceToSalesTrailing12Months', None)
        metrics['P/S Ratio'] = ps_ratio
        
        # EV/EBITDA
        ev_ebitda = info.get('enterpriseToEbitda', None)
        metrics['EV/EBITDA'] = ev_ebitda
        
        # Dividend Yield
        dividend_yield = info.get('dividendYield', None)
        if dividend_yield:
            metrics['Dividend Yield %'] = dividend_yield * 100
        else:
            metrics['Dividend Yield %'] = None
        
        # Market Cap
        market_cap = info.get('marketCap', None)
        metrics['Market Cap (Cr)'] = market_cap / 10000000 if market_cap else None
        
        # 52-week high and low
        metrics['52W High'] = info.get('fiftyTwoWeekHigh', None)
        metrics['52W Low'] = info.get('fiftyTwoWeekLow', None)
        
        # Current Price
        metrics['Current Price'] = current_price
        
        # Earnings Growth (%)
        earnings_growth = info.get('earningsGrowth', None)
        if earnings_growth:
            metrics['Earnings Growth %'] = earnings_growth * 100
        else:
            metrics['Earnings Growth %'] = None
        
        return metrics
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return {}

def calculate_sector_analysis(sector, stocks_data):
    """Calculate sector-wise aggregated metrics"""
    sector_stocks = [stock for stock, data in NIFTY_50_DATA.items() 
                     if data['Sector'] == sector]
    
    sector_metrics = []
    for stock in sector_stocks:
        if stock in stocks_data:
            row = stocks_data[stock].copy()
            row['Ticker'] = stock
            row['Company'] = NIFTY_50_DATA[stock]['Company']
            sector_metrics.append(row)
    
    return pd.DataFrame(sector_metrics)

def analyze_valuation_signal(pe, pb, ps, ev_ebitda, peg=None):
    """Generate detailed valuation signal with metric-by-metric breakdown"""
    
    analysis = {
        'metrics': {},
        'overall_sentiment': [],
        'overvalued_count': 0,
        'undervalued_count': 0,
        'fair_count': 0
    }
    
    # P/E Analysis
    if pe:
        if pe < 12:
            analysis['metrics']['P/E'] = {
                'value': pe,
                'signal': '🟢 Undervalued',
                'status': 'Undervalued',
                'reasoning': 'Trading at low earnings multiple',
                'severity': 'Strong Buy',
                'color': 'green'
            }
            analysis['undervalued_count'] += 1
        elif pe < 15:
            analysis['metrics']['P/E'] = {
                'value': pe,
                'signal': '🟡 Undervalued',
                'status': 'Undervalued',
                'reasoning': 'Below historical average',
                'severity': 'Buy',
                'color': 'lightgreen'
            }
            analysis['undervalued_count'] += 1
        elif pe < 20:
            analysis['metrics']['P/E'] = {
                'value': pe,
                'signal': '🟡 Fair Valued',
                'status': 'Fair',
                'reasoning': 'Trading at reasonable multiple',
                'severity': 'Hold',
                'color': 'yellow'
            }
            analysis['fair_count'] += 1
        elif pe < 30:
            analysis['metrics']['P/E'] = {
                'value': pe,
                'signal': '🟠 Overvalued',
                'status': 'Overvalued',
                'reasoning': 'Premium to historical average',
                'severity': 'Sell',
                'color': 'orange'
            }
            analysis['overvalued_count'] += 1
        else:
            analysis['metrics']['P/E'] = {
                'value': pe,
                'signal': '🔴 Heavily Overvalued',
                'status': 'Overvalued',
                'reasoning': 'Trading at very high multiple',
                'severity': 'Strong Sell',
                'color': 'red'
            }
            analysis['overvalued_count'] += 2
    
    # P/B Analysis
    if pb:
        if pb < 0.8:
            analysis['metrics']['P/B'] = {
                'value': pb,
                'signal': '🟢 Undervalued',
                'status': 'Undervalued',
                'reasoning': 'Trading below book value',
                'severity': 'Strong Buy',
                'color': 'green'
            }
            analysis['undervalued_count'] += 1
        elif pb < 1.2:
            analysis['metrics']['P/B'] = {
                'value': pb,
                'signal': '🟡 Fair Valued',
                'status': 'Fair',
                'reasoning': 'Near book value',
                'severity': 'Hold',
                'color': 'yellow'
            }
            analysis['fair_count'] += 1
        elif pb < 2.0:
            analysis['metrics']['P/B'] = {
                'value': pb,
                'signal': '🟡 Moderately Valued',
                'status': 'Fair',
                'reasoning': 'Premium to book value',
                'severity': 'Hold',
                'color': 'yellow'
            }
            analysis['fair_count'] += 1
        elif pb < 3.0:
            analysis['metrics']['P/B'] = {
                'value': pb,
                'signal': '🟠 Overvalued',
                'status': 'Overvalued',
                'reasoning': 'Significant premium to book',
                'severity': 'Sell',
                'color': 'orange'
            }
            analysis['overvalued_count'] += 1
        else:
            analysis['metrics']['P/B'] = {
                'value': pb,
                'signal': '🔴 Heavily Overvalued',
                'status': 'Overvalued',
                'reasoning': 'Extreme premium to book value',
                'severity': 'Strong Sell',
                'color': 'red'
            }
            analysis['overvalued_count'] += 2
    
    # P/S Analysis
    if ps:
        if ps < 0.5:
            analysis['metrics']['P/S'] = {
                'value': ps,
                'signal': '🟢 Undervalued',
                'status': 'Undervalued',
                'reasoning': 'Very low sales multiple',
                'severity': 'Strong Buy',
                'color': 'green'
            }
            analysis['undervalued_count'] += 1
        elif ps < 1.0:
            analysis['metrics']['P/S'] = {
                'value': ps,
                'signal': '🟡 Fair Valued',
                'status': 'Fair',
                'reasoning': 'Reasonable sales multiple',
                'severity': 'Hold',
                'color': 'yellow'
            }
            analysis['fair_count'] += 1
        elif ps < 2.0:
            analysis['metrics']['P/S'] = {
                'value': ps,
                'signal': '🟡 Moderately Valued',
                'status': 'Fair',
                'reasoning': 'Moderate premium',
                'severity': 'Hold',
                'color': 'yellow'
            }
            analysis['fair_count'] += 1
        elif ps < 3.0:
            analysis['metrics']['P/S'] = {
                'value': ps,
                'signal': '🟠 Overvalued',
                'status': 'Overvalued',
                'reasoning': 'Elevated sales multiple',
                'severity': 'Sell',
                'color': 'orange'
            }
            analysis['overvalued_count'] += 1
        else:
            analysis['metrics']['P/S'] = {
                'value': ps,
                'signal': '🔴 Heavily Overvalued',
                'status': 'Overvalued',
                'reasoning': 'Excessive sales multiple',
                'severity': 'Strong Sell',
                'color': 'red'
            }
            analysis['overvalued_count'] += 2
    
    # EV/EBITDA Analysis
    if ev_ebitda:
        if ev_ebitda < 8:
            analysis['metrics']['EV/EBITDA'] = {
                'value': ev_ebitda,
                'signal': '🟢 Undervalued',
                'status': 'Undervalued',
                'reasoning': 'Low EBITDA multiple',
                'severity': 'Strong Buy',
                'color': 'green'
            }
            analysis['undervalued_count'] += 1
        elif ev_ebitda < 12:
            analysis['metrics']['EV/EBITDA'] = {
                'value': ev_ebitda,
                'signal': '🟡 Fair Valued',
                'status': 'Fair',
                'reasoning': 'Historical average multiple',
                'severity': 'Hold',
                'color': 'yellow'
            }
            analysis['fair_count'] += 1
        elif ev_ebitda < 15:
            analysis['metrics']['EV/EBITDA'] = {
                'value': ev_ebitda,
                'signal': '🟡 Moderately Valued',
                'status': 'Fair',
                'reasoning': 'Above average multiple',
                'severity': 'Hold',
                'color': 'yellow'
            }
            analysis['fair_count'] += 1
        elif ev_ebitda < 20:
            analysis['metrics']['EV/EBITDA'] = {
                'value': ev_ebitda,
                'signal': '🟠 Overvalued',
                'status': 'Overvalued',
                'reasoning': 'Premium EBITDA multiple',
                'severity': 'Sell',
                'color': 'orange'
            }
            analysis['overvalued_count'] += 1
        else:
            analysis['metrics']['EV/EBITDA'] = {
                'value': ev_ebitda,
                'signal': '🔴 Heavily Overvalued',
                'status': 'Overvalued',
                'reasoning': 'Very high EBITDA multiple',
                'severity': 'Strong Sell',
                'color': 'red'
            }
            analysis['overvalued_count'] += 2
    
    # Overall sentiment
    if analysis['undervalued_count'] > analysis['overvalued_count']:
        analysis['overall'] = '🟢 UNDERVALUED - BUY'
        analysis['recommendation'] = 'Strong Buy Signal'
    elif analysis['undervalued_count'] == analysis['overvalued_count']:
        analysis['overall'] = '🟡 FAIRLY VALUED - HOLD'
        analysis['recommendation'] = 'Hold Signal'
    else:
        analysis['overall'] = '🔴 OVERVALUED - SELL'
        analysis['recommendation'] = 'Sell Signal'
    
    return analysis

# ============================================================================
# STREAMLIT INTERFACE
# ============================================================================

# Header
st.markdown("""
<div class="header-box">
    <h1>📊 THE MOUNTAIN PATH • WORLD OF FINANCE</h1>
    <h3>Nifty Stock Relative Valuation Analysis Platform</h3>
    <p><i>Dynamic Sector-wise Valuation Model with Risk Metrics</i></p>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking | 10+ Years Academic Excellence</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================
with st.sidebar:
    # Professional Header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 28px; margin-bottom: 5px;">📊</div>
        <h1 style="color: white; font-size: 18px; margin: 0; font-weight: bold;">RELATIVE VALUATION</h1>
        <p style="color: #b3d9ff; font-size: 11px; margin: 8px 0;">Advanced Comparable Multiples Framework</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Select Mode Section
    st.markdown('<div class="sidebar-title">Select Mode:</div>', unsafe_allow_html=True)
    
    analysis_mode = st.radio(
        "Analysis Mode",
        ["Single Stock Analysis", "Sector Comparison", "Multi-Stock Comparison", 
         "Relative Valuation Matrix"],
        label_visibility="collapsed",
        help="Choose how you want to analyze stocks"
    )
    
    # Time Period Selection
    st.markdown('<div class="sidebar-title">Time Period:</div>', unsafe_allow_html=True)
    period = st.selectbox(
        "Select Time Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        label_visibility="collapsed",
        help="Historical data period for charts"
    )
    
    sectors = list(set([data['Sector'] for data in NIFTY_50_DATA.values()]))
    sectors.sort()
    
    st.markdown("---")
    
    # About This Tool Section
    st.markdown('<div class="sidebar-title">About This Tool</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: #ffffff; font-size: 13px; line-height: 1.8; margin-bottom: 15px;">
    This platform uses the <b>Comparable Multiples Framework</b>:
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: #ffffff; font-size: 12px; margin-bottom: 3px;">
    <span style="color: #FF6B6B; font-weight: bold;">📊</span> <b>Valuation</b> - P/E, P/B, P/S Multiples
    </div>
    <div style="color: #ffffff; font-size: 12px; margin-bottom: 3px;">
    <span style="color: #4ECDC4; font-weight: bold;">⚙️</span> <b>EV/EBITDA</b> - Enterprise Value Analysis
    </div>
    <div style="color: #ffffff; font-size: 12px; margin-bottom: 3px;">
    <span style="color: #FFE66D; font-weight: bold;">🎯</span> <b>Sector Peers</b> - Comparable Companies
    </div>
    <div style="color: #ffffff; font-size: 12px; margin-bottom: 3px;">
    <span style="color: #95E1D3; font-weight: bold;">📈</span> <b>Implied Prices</b> - Fair Value Estimates
    </div>
    <div style="color: #ffffff; font-size: 12px; margin-bottom: 15px;">
    <span style="color: #A8E6CF; font-weight: bold;">🔍</span> <b>Investment Signals</b> - Buy/Hold/Sell
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Author Info
    st.markdown("""
    <div class="sidebar-author">
        <div class="sidebar-author-name">Prof. V. Ravichandran</div>
        <div class="sidebar-author-text">
        📚 28+ Years Corporate Finance & Banking Experience<br>
        🎓 10+ Years Academic Excellence<br>
        🏆 The Mountain Path - World of Finance
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # LinkedIn Button
    st.markdown("""
    <div style="margin-top: 15px;">
        <a href="https://www.linkedin.com/in/trichyravis/" target="_blank" 
           style="display: block; background-color: #1e5a96; color: #FFD700; 
                  border: 2px solid #FFD700; padding: 10px 15px; border-radius: 6px; 
                  text-align: center; font-weight: bold; text-decoration: none; 
                  font-size: 12px;">
        🔗 LinkedIn Profile
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features
    st.markdown('<div class="sidebar-title">Key Features</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: #b3d9ff; font-size: 12px; line-height: 1.8;">
    ✅ Real-time valuation multiples<br>
    ✅ Sector peer comparison<br>
    ✅ Implied price calculation<br>
    ✅ Investment recommendations<br>
    ✅ Risk assessment<br>
    ✅ Multi-stock analysis
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ANALYSIS MODE: SINGLE STOCK ANALYSIS
# ============================================================================
if analysis_mode == "Single Stock Analysis":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_ticker = st.selectbox(
            "Select Stock:",
            list(NIFTY_50_DATA.keys()),
            format_func=lambda x: f"{NIFTY_50_DATA[x]['Company']} ({x})"
        )
    
    with col2:
        st.markdown("###")
        if st.button("📈 Analyze Stock", use_container_width=True):
            pass
    
    # Fetch data
    info = fetch_stock_info(selected_ticker)
    
    if info:
        company_name = NIFTY_50_DATA[selected_ticker]['Company']
        sector = NIFTY_50_DATA[selected_ticker]['Sector']
        
        # Header info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-title">Company Name</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{company_name}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-title">Sector</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{sector}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-title">Current Price</div>', unsafe_allow_html=True)
            price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            st.markdown(f'<div class="metric-value">₹ {price:,.2f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-title">Market Cap (Cr)</div>', unsafe_allow_html=True)
            mc = info.get('marketCap', 0) / 10000000
            st.markdown(f'<div class="metric-value">₹ {mc:,.0f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Relative Valuation Metrics
        metrics = calculate_valuation_metrics(selected_ticker, info)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 VALUATION MULTIPLES")
            
            val_data = {
                'Metric': ['P/E Ratio', 'P/B Ratio', 'P/S Ratio', 'EV/EBITDA'],
                'Value': [
                    f"{metrics.get('P/E Ratio', 'N/A'):.2f}" if metrics.get('P/E Ratio') else 'N/A',
                    f"{metrics.get('P/B Ratio', 'N/A'):.2f}" if metrics.get('P/B Ratio') else 'N/A',
                    f"{metrics.get('P/S Ratio', 'N/A'):.2f}" if metrics.get('P/S Ratio') else 'N/A',
                    f"{metrics.get('EV/EBITDA', 'N/A'):.2f}" if metrics.get('EV/EBITDA') else 'N/A',
                ]
            }
            st.table(pd.DataFrame(val_data))
        
        with col2:
            st.markdown("### 📈 PERFORMANCE METRICS")
            
            perf_data = {
                'Metric': ['Dividend Yield %', 'Earnings Growth %', '52W High', '52W Low'],
                'Value': [
                    f"{metrics.get('Dividend Yield %', 'N/A'):.2f}%" if metrics.get('Dividend Yield %') else 'N/A',
                    f"{metrics.get('Earnings Growth %', 'N/A'):.2f}%" if metrics.get('Earnings Growth %') else 'N/A',
                    f"₹ {metrics.get('52W High', 'N/A'):.2f}" if metrics.get('52W High') else 'N/A',
                    f"₹ {metrics.get('52W Low', 'N/A'):.2f}" if metrics.get('52W Low') else 'N/A',
                ]
            }
            st.table(pd.DataFrame(perf_data))
        
        with col3:
            st.markdown("### 🎯 VALUATION SIGNAL")
            
            # Get detailed valuation analysis
            signal_analysis = analyze_valuation_signal(
                metrics.get('P/E Ratio'),
                metrics.get('P/B Ratio'),
                metrics.get('P/S Ratio'),
                metrics.get('EV/EBITDA')
            )
            
            # Display overall sentiment
            st.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; border-left: 5px solid #003366;">
                <div style="font-size: 18px; font-weight: bold; color: #003366; margin-bottom: 10px;">
                {signal_analysis['overall']}
                </div>
                <div style="font-size: 13px; color: #555;">
                {signal_analysis['recommendation']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Price Chart
        st.markdown("### 📉 PRICE CHART & TECHNICAL ANALYSIS")
        
        hist_data = fetch_stock_data(selected_ticker, period)
        
        if hist_data is not None and len(hist_data) > 0:
            try:
                # SUPER SIMPLE approach - just get the data
                import yfinance as yf
                
                # Re-fetch to ensure clean data
                raw_data = yf.download(selected_ticker, period=period, progress=False)
                
                if raw_data is None or len(raw_data) == 0:
                    st.warning("⚠️ No data available")
                else:
                    # Extract close prices - handle both MultiIndex and regular columns
                    if isinstance(raw_data.columns, pd.MultiIndex):
                        close_prices = raw_data[('Close', selected_ticker)]
                    else:
                        close_prices = raw_data['Close']
                    
                    # Create simple dataframe
                    df = pd.DataFrame({
                        'Date': close_prices.index,
                        'Close': close_prices.values
                    })
                    
                    # Convert to numeric and remove NaN
                    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
                    df = df.dropna()
                    df = df.sort_values('Date')
                    
                    if len(df) < 2:
                        st.error("Not enough data points")
                    else:
                        # Calculate MAs
                        df['MA20'] = df['Close'].rolling(20).mean()
                        df['MA50'] = df['Close'].rolling(50).mean()
                        
                        # Create chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close Price', line=dict(color='#003366', width=3)))
                        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name='20-Day MA', line=dict(color='#4472C4', width=2, dash='dash')))
                        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name='50-Day MA', line=dict(color='#FF7C1F', width=2, dash='dot')))
                        
                        fig.update_layout(
                            title=f'{company_name} - Stock Price Analysis',
                            xaxis_title='Date',
                            yaxis_title='Price (₹)',
                            template='plotly_white',
                            height=450,
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Stats
                        st.markdown("### 📊 Price Statistics")
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric("Current", f"₹{df['Close'].iloc[-1]:,.0f}")
                        with col2:
                            st.metric("High", f"₹{df['Close'].max():,.0f}")
                        with col3:
                            st.metric("Low", f"₹{df['Close'].min():,.0f}")
                        with col4:
                            st.metric("Average", f"₹{df['Close'].mean():,.0f}")
                        with col5:
                            vol = df['Close'].pct_change().std() * 100
                            st.metric("Volatility", f"{vol:.2f}%")
                        
                        # ================================================================
                        # COMPARABLE MULTIPLES VALUATION
                        # ================================================================
                        st.markdown("---")
                        st.markdown("### 💰 RELATIVE VALUATION USING COMPARABLE MULTIPLES")
                        
                        st.markdown("""
                        **How it works:** This section uses valuation multiples from comparable companies in the same sector 
                        to calculate an implied valuation for the selected company.
                        """)
                        
                        # Get sector for the selected stock
                        sector = NIFTY_50_DATA[selected_ticker]['Sector']
                        
                        try:
                            sector_multiples = get_sector_multiples(sector)
                            
                            if sector_multiples:
                                # Prepare financials dictionary
                                # Get market cap in crores
                                market_cap_cr = info.get('marketCap', 0) / 10000000 if info.get('marketCap') else 0
                                
                                # Back-calculate financial metrics from multiples
                                # P/E = Market Cap / Net Income → Net Income = Market Cap / P/E
                                pe_ratio = metrics.get('P/E Ratio', 1) if metrics.get('P/E Ratio', 0) > 0 else 1
                                net_income = market_cap_cr / pe_ratio if pe_ratio > 0 else 0
                                
                                # P/B = Market Cap / Book Value → Book Value = Market Cap / P/B
                                pb_ratio = metrics.get('P/B Ratio', 1) if metrics.get('P/B Ratio', 0) > 0 else 1
                                book_value = market_cap_cr / pb_ratio if pb_ratio > 0 else 0
                                
                                # P/S = Market Cap / Revenue → Revenue = Market Cap / P/S
                                # VALIDATE: P/S should be between 0.1x and 20x for most companies
                                ps_ratio_raw = metrics.get('P/S Ratio')
                                # Check for None and handle it
                                if ps_ratio_raw is None or ps_ratio_raw == 0:
                                    ps_ratio = 3.0  # Default conservative estimate
                                elif ps_ratio_raw > 20:  # Sanitize unrealistic values
                                    ps_ratio = 3.0  # Use reasonable default
                                else:
                                    ps_ratio = ps_ratio_raw
                                revenue = market_cap_cr / ps_ratio if ps_ratio > 0 else 0
                                
                                # EV/EBITDA = EV / EBITDA → EBITDA = EV / EV/EBITDA
                                # EV = Market Cap + Net Debt
                                net_debt = (info.get('totalDebt', 0) - info.get('totalCash', 0)) / 10000000 if info.get('totalDebt') else 0
                                ev = market_cap_cr + net_debt
                                ev_ebitda_raw = metrics.get('EV/EBITDA')
                                # Check for None and handle it
                                if ev_ebitda_raw is None or ev_ebitda_raw == 0:
                                    ev_ebitda_ratio = pe_ratio * 0.85  # Derive from P/E
                                elif ev_ebitda_raw > 50:  # Sanitize unrealistic values
                                    ev_ebitda_ratio = pe_ratio * 0.85  # Use P/E as proxy
                                else:
                                    ev_ebitda_ratio = ev_ebitda_raw
                                ebitda = ev / ev_ebitda_ratio if ev_ebitda_ratio > 0 else 0
                                
                                # Shares outstanding from yfinance (in millions)
                                shares_outstanding = info.get('sharesOutstanding', 0) / 1000000 if info.get('sharesOutstanding') else 1
                                
                                company_financials = {
                                    'market_cap': market_cap_cr,
                                    'net_income': net_income,
                                    'book_value': book_value,
                                    'revenue': revenue,
                                    'ebitda': ebitda,
                                    'shares_outstanding': shares_outstanding,
                                    'share_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                                    'net_debt': net_debt
                                }
                                
                                # Get valuation summary
                                valuation_df = get_valuation_summary(company_financials, sector)
                                
                                if not valuation_df.empty:
                                    st.markdown(f"**Sector:** {sector}")
                                    st.markdown(f"**Comparable Companies:** {', '.join(sector_multiples['companies'][:5])}")
                                    
                                    st.markdown("---")
                                    
                                    # Display comparison table
                                    st.markdown("#### Comparable Multiples Valuation")
                                    st.dataframe(valuation_df, use_container_width=True, hide_index=True)
                                    
                                    st.markdown("---")
                                    
                                    # Detailed breakdown by multiple
                                    st.markdown("#### Valuation Analysis by Multiple Type")
                                    
                                    tab1, tab2, tab3, tab4 = st.tabs(['P/E Ratio', 'P/B Ratio', 'P/S Ratio', 'EV/EBITDA'])
                                    
                                    with tab1:
                                        st.markdown("##### **Price/Earnings Multiple Analysis**")
                                        
                                        if company_financials['net_income'] and company_financials['net_income'] > 0:
                                            pe_results = calculate_implied_valuation(
                                                company_financials, 
                                                sector_multiples['multiples'], 
                                                'P/E'
                                            )
                                            
                                            if pe_results:
                                                col_pe1, col_pe2, col_pe3, col_pe4 = st.columns(4)
                                                
                                                for idx, (method, result) in enumerate(pe_results.items()):
                                                    with [col_pe1, col_pe2, col_pe3, col_pe4][idx]:
                                                        color = '#90EE90' if result['upside_downside'] > 0 else '#FFB6C6'
                                                        st.markdown(f"""
                                                        <div style="background-color: {color}; padding: 12px; border-radius: 6px; text-align: center;">
                                                            <b>{method.upper()}</b><br>
                                                            Multiple: {result['multiple']:.2f}x<br>
                                                            <span style="font-size: 18px; font-weight: bold;">₹{result['implied_price']:.0f}</span><br>
                                                            <span style="font-size: 12px;">{result['upside_downside']:+.1f}%</span>
                                                        </div>
                                                        """, unsafe_allow_html=True)
                                                
                                                st.markdown("---")
                                                
                                                col_pe_left, col_pe_right = st.columns(2)
                                                
                                                with col_pe_left:
                                                    st.markdown("**Sector P/E Range**")
                                                    pe_range = sector_multiples['multiples']['P/E']
                                                    st.write(f"High: {pe_range['high']:.2f}x")
                                                    st.write(f"Average: {pe_range['avg']:.2f}x")
                                                    st.write(f"Median: {pe_range['median']:.2f}x")
                                                    st.write(f"Low: {pe_range['low']:.2f}x")
                                                
                                                with col_pe_right:
                                                    st.markdown("**Current Stock**")
                                                    st.write(f"Current P/E: {metrics.get('P/E Ratio', 'N/A'):.2f}x" if metrics.get('P/E Ratio') else "Current P/E: N/A")
                                                    st.write(f"Current Price: ₹{company_financials['share_price']:.0f}")
                                                    median_val = pe_results['median']['implied_price']
                                                    st.write(f"Median Implied: ₹{median_val:.0f}")
                                                    st.write(f"Upside/Downside: {pe_results['median']['upside_downside']:+.1f}%")
                                        else:
                                            st.info("P/E multiple not available due to negative or missing earnings")
                                    
                                    with tab2:
                                        st.markdown("##### **Price-to-Book Multiple Analysis**")
                                        
                                        if company_financials['book_value'] and company_financials['book_value'] > 0:
                                            pb_results = calculate_implied_valuation(
                                                company_financials, 
                                                sector_multiples['multiples'], 
                                                'P/B'
                                            )
                                            
                                            if pb_results:
                                                col_pb1, col_pb2, col_pb3, col_pb4 = st.columns(4)
                                                
                                                for idx, (method, result) in enumerate(pb_results.items()):
                                                    with [col_pb1, col_pb2, col_pb3, col_pb4][idx]:
                                                        color = '#90EE90' if result['upside_downside'] > 0 else '#FFB6C6'
                                                        st.markdown(f"""
                                                        <div style="background-color: {color}; padding: 12px; border-radius: 6px; text-align: center;">
                                                            <b>{method.upper()}</b><br>
                                                            Multiple: {result['multiple']:.2f}x<br>
                                                            <span style="font-size: 18px; font-weight: bold;">₹{result['implied_price']:.0f}</span><br>
                                                            <span style="font-size: 12px;">{result['upside_downside']:+.1f}%</span>
                                                        </div>
                                                        """, unsafe_allow_html=True)
                                                
                                                st.markdown("---")
                                                
                                                col_pb_left, col_pb_right = st.columns(2)
                                                
                                                with col_pb_left:
                                                    st.markdown("**Sector P/B Range**")
                                                    pb_range = sector_multiples['multiples']['P/B']
                                                    st.write(f"High: {pb_range['high']:.2f}x")
                                                    st.write(f"Average: {pb_range['avg']:.2f}x")
                                                    st.write(f"Median: {pb_range['median']:.2f}x")
                                                    st.write(f"Low: {pb_range['low']:.2f}x")
                                                
                                                with col_pb_right:
                                                    st.markdown("**Current Stock**")
                                                    st.write(f"Current P/B: {metrics.get('P/B Ratio', 'N/A'):.2f}x" if metrics.get('P/B Ratio') else "Current P/B: N/A")
                                                    st.write(f"Current Price: ₹{company_financials['share_price']:.0f}")
                                                    median_val = pb_results['median']['implied_price']
                                                    st.write(f"Median Implied: ₹{median_val:.0f}")
                                                    st.write(f"Upside/Downside: {pb_results['median']['upside_downside']:+.1f}%")
                                        else:
                                            st.info("P/B multiple not available due to missing book value")
                                    
                                        with tab3:
                                            st.markdown("##### **Price-to-Sales Multiple Analysis**")
                                        
                                            # Show data quality warning if P/S was sanitized
                                            ps_from_metrics = metrics.get('P/S Ratio')
                                            if ps_from_metrics is not None and ps_from_metrics > 20:
                                                st.warning(f"⚠️ Data Note: P/S ratio from source ({ps_from_metrics:.2f}x) appears unusually high. Using conservative estimate (3.0x) for calculation.")
                                            elif ps_from_metrics is None:
                                                st.info("ℹ️ P/S data not available from source. Using sector estimate for calculation.")
                                        
                                            if company_financials['revenue'] and company_financials['revenue'] > 0:
                                                ps_results = calculate_implied_valuation(
                                                    company_financials, 
                                                    sector_multiples['multiples'], 
                                                    'P/S'
                                                )
                                            
                                                if ps_results:
                                                    col_ps1, col_ps2, col_ps3, col_ps4 = st.columns(4)
                                                
                                                    for idx, (method, result) in enumerate(ps_results.items()):
                                                        with [col_ps1, col_ps2, col_ps3, col_ps4][idx]:
                                                            color = '#90EE90' if result['upside_downside'] > 0 else '#FFB6C6'
                                                            st.markdown(f"""
                                                            <div style="background-color: {color}; padding: 12px; border-radius: 6px; text-align: center;">
                                                                <b>{method.upper()}</b><br>
                                                                Multiple: {result['multiple']:.2f}x<br>
                                                                <span style="font-size: 18px; font-weight: bold;">₹{result['implied_price']:.0f}</span><br>
                                                                <span style="font-size: 12px;">{result['upside_downside']:+.1f}%</span>
                                                            </div>
                                                            """, unsafe_allow_html=True)
                                                
                                                    st.markdown("---")
                                                
                                                    col_ps_left, col_ps_right = st.columns(2)
                                                
                                                    with col_ps_left:
                                                        st.markdown("**Sector P/S Range**")
                                                        ps_range = sector_multiples['multiples']['P/S']
                                                        st.write(f"High: {ps_range['high']:.2f}x")
                                                        st.write(f"Average: {ps_range['avg']:.2f}x")
                                                        st.write(f"Median: {ps_range['median']:.2f}x")
                                                        st.write(f"Low: {ps_range['low']:.2f}x")
                                                
                                                    with col_ps_right:
                                                        st.markdown("**Current Stock**")
                                                        st.write(f"Current P/S: {metrics.get('P/S Ratio', 'N/A'):.2f}x" if metrics.get('P/S Ratio') else "Current P/S: N/A")
                                                        st.write(f"Current Price: ₹{company_financials['share_price']:.0f}")
                                                        median_val = ps_results['median']['implied_price']
                                                        st.write(f"Median Implied: ₹{median_val:.0f}")
                                                        st.write(f"Upside/Downside: {ps_results['median']['upside_downside']:+.1f}%")
                                            else:
                                                st.info("P/S multiple not available due to missing revenue")
                                    
                                        with tab4:
                                            st.markdown("##### **EV/EBITDA Multiple Analysis**")
                                        
                                            # Show data quality warning if EV/EBITDA was derived
                                            ev_ebitda_from_metrics = metrics.get('EV/EBITDA')
                                            if ev_ebitda_from_metrics is not None and ev_ebitda_from_metrics > 50:
                                                pe_val = metrics.get('P/E Ratio', 20)
                                                st.warning(f"⚠️ Data Note: EV/EBITDA ratio from source ({ev_ebitda_from_metrics:.2f}x) appears unusually high. Using derived estimate ({pe_val * 0.85:.2f}x) for calculation.")
                                            elif ev_ebitda_from_metrics is None:
                                                st.info("ℹ️ EV/EBITDA data not available from source. Deriving from P/E ratio for calculation.")
                                        
                                            if company_financials['ebitda'] and company_financials['ebitda'] > 0:
                                                ev_results = calculate_implied_valuation(
                                                    company_financials, 
                                                    sector_multiples['multiples'], 
                                                    'EV/EBITDA'
                                                )
                                            
                                                if ev_results:
                                                    col_ev1, col_ev2, col_ev3, col_ev4 = st.columns(4)
                                                
                                                    for idx, (method, result) in enumerate(ev_results.items()):
                                                        with [col_ev1, col_ev2, col_ev3, col_ev4][idx]:
                                                            color = '#90EE90' if result['upside_downside'] > 0 else '#FFB6C6'
                                                            st.markdown(f"""
                                                            <div style="background-color: {color}; padding: 12px; border-radius: 6px; text-align: center;">
                                                                <b>{method.upper()}</b><br>
                                                                Multiple: {result['multiple']:.2f}x<br>
                                                                <span style="font-size: 18px; font-weight: bold;">₹{result['implied_price']:.0f}</span><br>
                                                                <span style="font-size: 12px;">{result['upside_downside']:+.1f}%</span>
                                                            </div>
                                                            """, unsafe_allow_html=True)
                                                
                                                    st.markdown("---")
                                                
                                                    col_ev_left, col_ev_right = st.columns(2)
                                                
                                                    with col_ev_left:
                                                        st.markdown("**Sector EV/EBITDA Range**")
                                                        ev_range = sector_multiples['multiples']['EV/EBITDA']
                                                        st.write(f"High: {ev_range['high']:.2f}x")
                                                        st.write(f"Average: {ev_range['avg']:.2f}x")
                                                        st.write(f"Median: {ev_range['median']:.2f}x")
                                                        st.write(f"Low: {ev_range['low']:.2f}x")
                                                
                                                    with col_ev_right:
                                                        st.markdown("**Current Stock**")
                                                        st.write(f"Current EV/EBITDA: {metrics.get('EV/EBITDA', 'N/A'):.2f}x" if metrics.get('EV/EBITDA') else "Current EV/EBITDA: N/A")
                                                        st.write(f"Current Price: ₹{company_financials['share_price']:.0f}")
                                                        median_val = ev_results['median']['implied_price']
                                                        st.write(f"Median Implied: ₹{median_val:.0f}")
                                                        st.write(f"Upside/Downside: {ev_results['median']['upside_downside']:+.1f}%")
                                            else:
                                                st.info("EV/EBITDA multiple not available due to missing EBITDA")
                                    
                                    st.markdown("---")
                                    st.markdown("""
                                    **📊 Key Takeaway:**
                                    - **Green boxes** = Stock appears undervalued vs sector comparables
                                    - **Red boxes** = Stock appears overvalued vs sector comparables
                                    - Median multiple used as most representative
                                    - Compare current price with implied prices across methods
                                    """)
                                
                                else:
                                    st.info("Valuation data not available for this stock")
                            else:
                                st.warning(f"Comparable multiples not available for {sector} sector")
                        
                        except Exception as e:
                            st.warning(f"Could not load comparable multiples: {str(e)}")
                        
                        # ================================================================
                        # VALUATION SIGNAL - MOVED BELOW COMPARABLE MULTIPLES
                        # ================================================================
                        st.markdown("---")
                        st.markdown("### 🎯 VALUATION SIGNAL")
                        
                        # Get detailed valuation analysis
                        signal_analysis = analyze_valuation_signal(
                            metrics.get('P/E Ratio'),
                            metrics.get('P/B Ratio'),
                            metrics.get('P/S Ratio'),
                            metrics.get('EV/EBITDA')
                        )
                        
                        # Display overall sentiment
                        st.markdown(f"""
                        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; border-left: 5px solid #003366;">
                            <div style="font-size: 18px; font-weight: bold; color: #003366; margin-bottom: 10px;">
                            {signal_analysis['overall']}
                            </div>
                            <div style="font-size: 13px; color: #555;">
                            {signal_analysis['recommendation']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Expandable detailed analysis
                        with st.expander("📊 DETAILED VALUATION BREAKDOWN", expanded=False):
                            # ================================================================
                            # ENHANCED DETAILED VALUATION BREAKDOWN
                            # ================================================================
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%); 
                                        padding: 20px; border-radius: 10px; border-left: 5px solid #003366;
                                        margin: 20px 0;">
                                <div style="font-size: 16px; font-weight: bold; color: #003366; margin-bottom: 10px;">
                                📊 DETAILED VALUATION BREAKDOWN
                                </div>
                                <div style="font-size: 12px; color: #666;">
                                Comprehensive metric-by-metric analysis with investment signals and severity assessment
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # -------- QUICK SUMMARY TABLE --------
                            st.markdown('<div style="font-weight: bold; color: #003366; margin: 20px 0 10px 0; font-size: 14px;">📋 QUICK SUMMARY</div>', unsafe_allow_html=True)
                            
                            # Create metric details table
                            metric_details = []
                            for metric_name, metric_data in signal_analysis['metrics'].items():
                                signal_emoji = '🟢' if metric_data['status'] == 'Undervalued' else ('🟡' if metric_data['status'] == 'Fair' else '🔴')
                                metric_details.append({
                                    'Metric': metric_name,
                                    'Value': f"{metric_data['value']:.2f}x",
                                    'Signal': f"{signal_emoji} {metric_data['signal']}",
                                    'Status': metric_data['status'],
                                    'Reasoning': metric_data['reasoning']
                                })
                            
                            if metric_details:
                                df_signals = pd.DataFrame(metric_details)
                                st.dataframe(df_signals, use_container_width=True, hide_index=True)
                            
                            # -------- METRIC-BY-METRIC DETAILED ANALYSIS --------
                            st.markdown('<div style="font-weight: bold; color: #003366; margin: 30px 0 15px 0; font-size: 14px;">🔍 METRIC-BY-METRIC ANALYSIS</div>', unsafe_allow_html=True)
                            
                            for idx, (metric_name, metric_data) in enumerate(signal_analysis['metrics'].items(), 1):
                                # Color scheme
                                colors_map = {
                                    'green': ('#2ecc71', '#d4edda', '#155724'),
                                    'lightgreen': ('#7cb342', '#e8f5e9', '#2e7d32'),
                                    'yellow': ('#f1c40f', '#fff3cd', '#856404'),
                                    'orange': ('#ff9800', '#fff3e0', '#e65100'),
                                    'red': ('#e74c3c', '#f8d7da', '#721c24')
                                }
                                
                                color_tuple = colors_map.get(metric_data['color'], ('#95a5a6', '#f0f0f0', '#555'))
                                main_color, bg_color, text_color = color_tuple
                                
                                # Signal emoji
                                signal_emoji = '🟢' if metric_data['status'] == 'Undervalued' else ('🟡' if metric_data['status'] == 'Fair' else '🔴')
                                
                                st.markdown(f"""
                                <div style="background-color: {bg_color}; border-left: 5px solid {main_color}; 
                                            padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                                    
                                    <!-- Header Row -->
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                        <div style="font-weight: bold; font-size: 16px; color: {text_color};">
                                        {idx}. {metric_name}
                                        </div>
                                        <div style="background-color: {main_color}; color: white; padding: 6px 12px; 
                                                   border-radius: 20px; font-weight: bold; font-size: 14px;">
                                        {metric_data['value']:.2f}x
                                        </div>
                                    </div>
                                    
                                    <!-- Content Grid -->
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                        
                                        <!-- Left Column: Status & Severity -->
                                        <div>
                                            <div style="margin-bottom: 10px;">
                                                <span style="font-weight: bold; color: {text_color};">Status:</span>
                                                <span style="color: {text_color}; margin-left: 5px;">{signal_emoji} {metric_data['status']}</span>
                                            </div>
                                            <div>
                                                <span style="font-weight: bold; color: {text_color};">Severity:</span>
                                                <span style="background-color: {main_color}; color: white; padding: 3px 8px; 
                                                           border-radius: 4px; font-size: 12px; margin-left: 5px;">
                                                {metric_data['severity']}
                                                </span>
                                            </div>
                                        </div>
                                        
                                        <!-- Right Column: Reasoning -->
                                        <div>
                                            <div style="font-weight: bold; color: {text_color}; margin-bottom: 5px;">💡 Reasoning:</div>
                                            <div style="color: {text_color}; font-size: 13px; line-height: 1.6;">
                                            {metric_data['reasoning']}
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Valuation Level Bar -->
                                    <div style="margin-top: 12px;">
                                        <div style="font-weight: bold; color: {text_color}; font-size: 12px; margin-bottom: 5px;">
                                        Valuation Level:
                                        </div>
                                        <div style="width: 100%; height: 8px; background-color: #e0e0e0; border-radius: 4px; overflow: hidden;">
                                            <div style="width: {min(max((metric_data['value'] / 30) * 100, 5), 100)}%; height: 100%; 
                                                       background: linear-gradient(90deg, #2ecc71 0%, #f1c40f 50%, #e74c3c 100%);">
                                            </div>
                                        </div>
                                        <div style="font-size: 10px; color: #666; margin-top: 4px; display: flex; justify-content: space-between;">
                                            <span>Low</span>
                                            <span>Fair</span>
                                            <span>High</span>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            
                            # -------- VALUATION SCORE CARDS --------
                            st.markdown('<div style="font-weight: bold; color: #003366; margin: 20px 0 15px 0; font-size: 14px;">📊 VALUATION SCORE BREAKDOWN</div>', unsafe_allow_html=True)
                            
                            score_col1, score_col2, score_col3, score_col4 = st.columns(4)
                            
                            undervalued_count = signal_analysis['undervalued_count']
                            fair_count = signal_analysis['fair_count']
                            overvalued_count = signal_analysis['overvalued_count']
                            total_metrics = undervalued_count + fair_count + overvalued_count
                            
                            with score_col1:
                                st.markdown(f"""
                                <div style="background-color: #d4edda; border-left: 4px solid #28a745; padding: 15px; border-radius: 6px; text-align: center;">
                                    <div style="font-size: 28px; font-weight: bold; color: #28a745;">🟢</div>
                                    <div style="font-weight: bold; color: #155724; margin: 8px 0;">Undervalued</div>
                                    <div style="font-size: 24px; font-weight: bold; color: #28a745;">{undervalued_count}</div>
                                    <div style="font-size: 11px; color: #155724; margin-top: 5px;">
                                    {(undervalued_count/total_metrics)*100:.0f}% of metrics
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with score_col2:
                                st.markdown(f"""
                                <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 6px; text-align: center;">
                                    <div style="font-size: 28px; font-weight: bold;">🟡</div>
                                    <div style="font-weight: bold; color: #856404; margin: 8px 0;">Fair Valued</div>
                                    <div style="font-size: 24px; font-weight: bold; color: #ffc107;">{fair_count}</div>
                                    <div style="font-size: 11px; color: #856404; margin-top: 5px;">
                                    {(fair_count/total_metrics)*100:.0f}% of metrics
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with score_col3:
                                st.markdown(f"""
                                <div style="background-color: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; border-radius: 6px; text-align: center;">
                                    <div style="font-size: 28px; font-weight: bold;">🔴</div>
                                    <div style="font-weight: bold; color: #721c24; margin: 8px 0;">Overvalued</div>
                                    <div style="font-size: 24px; font-weight: bold; color: #dc3545;">{overvalued_count}</div>
                                    <div style="font-size: 11px; color: #721c24; margin-top: 5px;">
                                    {(overvalued_count/total_metrics)*100:.0f}% of metrics
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with score_col4:
                                st.markdown(f"""
                                <div style="background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; border-radius: 6px; text-align: center;">
                                    <div style="font-size: 28px; font-weight: bold;">📊</div>
                                    <div style="font-weight: bold; color: #0d47a1; margin: 8px 0;">Total Metrics</div>
                                    <div style="font-size: 24px; font-weight: bold; color: #2196f3;">{total_metrics}</div>
                                    <div style="font-size: 11px; color: #0d47a1; margin-top: 5px;">
                                    Analyzed
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            
                            # -------- INVESTMENT RECOMMENDATION --------
                            st.markdown('<div style="font-weight: bold; color: #003366; margin: 20px 0 15px 0; font-size: 14px;">💡 INVESTMENT RECOMMENDATION</div>', unsafe_allow_html=True)
                            
                            if "UNDERVALUED" in signal_analysis['overall']:
                                recommendation_text = """
                                **🟢 BUY SIGNAL**
                                
                                The stock appears undervalued across multiple metrics. Potential for upside returns.
                                
                                *Suitable for:*
                                - Value investors
                                - Contrarian investors
                                - Long-term holders
                                - Risk-tolerant investors
                                """
                                rec_color = "#d4edda"
                                rec_border = "#28a745"
                                icon_color = "#28a745"
                            
                            elif "FAIRLY" in signal_analysis['overall']:
                                recommendation_text = """
                                **🟡 HOLD SIGNAL**
                                
                                The stock is trading at reasonable valuations. Balanced risk-reward profile.
                                
                                *Suitable for:*
                                - Income investors
                                - Conservative investors
                                - Current holders
                                - Moderate growth seekers
                                """
                                rec_color = "#fff3cd"
                                rec_border = "#ffc107"
                                icon_color = "#ffc107"
                            
                            else:
                                recommendation_text = """
                                **🔴 SELL SIGNAL**
                                
                                The stock appears overvalued on multiple metrics. Limited upside, significant downside risk.
                                
                                *Suitable for:*
                                - Risk-averse investors
                                - Profit-takers
                                - Short-term traders
                                - Those seeking better valuations
                                """
                                rec_color = "#f8d7da"
                                rec_border = "#dc3545"
                                icon_color = "#dc3545"
                            
                            st.markdown(f"""
                            <div style="background-color: {rec_color}; border-left: 5px solid {rec_border}; padding: 20px; border-radius: 8px;">
                            {recommendation_text}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            
                            # Disclaimer
                            st.markdown("""
                            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 6px; border-left: 4px solid #666;">
                                <div style="font-weight: bold; color: #333; margin-bottom: 8px;">⚠️ IMPORTANT DISCLAIMER</div>
                                <div style="font-size: 12px; color: #555; line-height: 1.7;">
                                This analysis is based on historical thresholds and valuation ratios and is purely educational. 
                                It should not be considered financial advice. Always conduct your own due diligence, analyze company fundamentals, 
                                market conditions, and consult with qualified financial advisors before making investment decisions. 
                                Past performance is not indicative of future results. Stocks involve risk, including potential loss of principal.
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("No data")

# ============================================================================
# ANALYSIS MODE: SECTOR COMPARISON
# ============================================================================
elif analysis_mode == "Sector Comparison":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_sector = st.selectbox(
            "Select Sector:",
            sectors,
            help="Choose sector for detailed analysis"
        )
    
    with col2:
        st.markdown("###")
        if st.button("🔍 Analyze Sector", use_container_width=True):
            pass
    
    st.markdown("---")
    
    # Get all stocks in sector
    sector_stocks = {stock: data for stock, data in NIFTY_50_DATA.items() 
                     if data['Sector'] == selected_sector}
    
    st.markdown(f"### {selected_sector} - Sector Analysis")
    st.write(f"**Total Companies:** {len(sector_stocks)}")
    
    # Fetch data for all stocks
    sector_data = []
    
    with st.spinner(f"Fetching data for {selected_sector} stocks..."):
        for ticker in sector_stocks.keys():
            info = fetch_stock_info(ticker)
            if info:
                metrics = calculate_valuation_metrics(ticker, info)
                metrics['Ticker'] = ticker
                metrics['Company'] = sector_stocks[ticker]['Company']
                sector_data.append(metrics)
    
    if sector_data:
        df_sector = pd.DataFrame(sector_data)
        
        # Display metrics table
        st.markdown("### Relative Valuation Metrics")
        
        display_cols = ['Company', 'Current Price', 'P/E Ratio', 'P/B Ratio', 
                       'P/S Ratio', 'EV/EBITDA', 'Dividend Yield %']
        
        df_display = df_sector[display_cols].copy()
        
        # Format for display
        for col in ['Current Price', 'P/E Ratio', 'P/B Ratio', 'P/S Ratio', 'EV/EBITDA', 'Dividend Yield %']:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(
                    lambda x: f"{x:.2f}" if pd.notna(x) else "N/A"
                )
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Sector comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pe = px.bar(
                df_sector.dropna(subset=['P/E Ratio']),
                x='Company',
                y='P/E Ratio',
                title='P/E Ratio Comparison',
                color='P/E Ratio',
                color_continuous_scale='RdYlGn_r',
                height=400
            )
            fig_pe.update_layout(xaxis_tickangle=-45, hovermode='x')
            st.plotly_chart(fig_pe, use_container_width=True)
        
        with col2:
            fig_pb = px.bar(
                df_sector.dropna(subset=['P/B Ratio']),
                x='Company',
                y='P/B Ratio',
                title='P/B Ratio Comparison',
                color='P/B Ratio',
                color_continuous_scale='RdYlGn_r',
                height=400
            )
            fig_pb.update_layout(xaxis_tickangle=-45, hovermode='x')
            st.plotly_chart(fig_pb, use_container_width=True)
        
        # Summary statistics
        st.markdown("### Sector Summary Statistics")
        
        summary_stats = {
            'Metric': ['Average P/E', 'Average P/B', 'Average P/S', 'Avg Dividend Yield %'],
            'Value': [
                f"{df_sector['P/E Ratio'].mean():.2f}" if len(df_sector['P/E Ratio'].dropna()) > 0 else 'N/A',
                f"{df_sector['P/B Ratio'].mean():.2f}" if len(df_sector['P/B Ratio'].dropna()) > 0 else 'N/A',
                f"{df_sector['P/S Ratio'].mean():.2f}" if len(df_sector['P/S Ratio'].dropna()) > 0 else 'N/A',
                f"{df_sector['Dividend Yield %'].mean():.2f}%" if len(df_sector['Dividend Yield %'].dropna()) > 0 else 'N/A',
            ]
        }
        
        st.dataframe(pd.DataFrame(summary_stats), use_container_width=True, hide_index=True)

# ============================================================================
# ANALYSIS MODE: MULTI-STOCK COMPARISON
# ============================================================================
elif analysis_mode == "Multi-Stock Comparison":
    st.markdown("### 📊 Compare Multiple Stocks")
    
    selected_tickers = st.multiselect(
        "Select stocks to compare:",
        list(NIFTY_50_DATA.keys()),
        format_func=lambda x: f"{NIFTY_50_DATA[x]['Company']} ({x})",
        max_selections=6
    )
    
    if selected_tickers:
        st.markdown("---")
        
        comparison_data = []
        
        with st.spinner("Fetching comparison data..."):
            for ticker in selected_tickers:
                info = fetch_stock_info(ticker)
                if info:
                    metrics = calculate_valuation_metrics(ticker, info)
                    metrics['Ticker'] = ticker
                    metrics['Company'] = NIFTY_50_DATA[ticker]['Company']
                    metrics['Sector'] = NIFTY_50_DATA[ticker]['Sector']
                    comparison_data.append(metrics)
        
        if comparison_data:
            df_compare = pd.DataFrame(comparison_data)
            
            # Comparison table
            st.markdown("### Comparative Valuation Metrics")
            
            display_cols = ['Company', 'Sector', 'Current Price', 'P/E Ratio', 
                           'P/B Ratio', 'P/S Ratio', 'EV/EBITDA', 'Market Cap (Cr)']
            
            df_display = df_compare[display_cols].copy()
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Radar chart for valuation comparison
            st.markdown("### Multi-Dimensional Valuation Comparison")
            
            # Normalize metrics for radar chart
            df_normalized = df_compare[['Company', 'P/E Ratio', 'P/B Ratio', 'P/S Ratio']].copy()
            df_normalized = df_normalized.dropna()
            
            if len(df_normalized) > 0:
                fig_radar = go.Figure()
                
                for idx, row in df_normalized.iterrows():
                    fig_radar.add_trace(go.Scatterpolar(
                        r=[row['P/E Ratio'], row['P/B Ratio'], row['P/S Ratio']],
                        theta=['P/E Ratio', 'P/B Ratio', 'P/S Ratio'],
                        fill='toself',
                        name=row['Company']
                    ))
                
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 30])),
                    title='Relative Valuation Multiples Comparison',
                    height=500
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)

# ============================================================================
# ANALYSIS MODE: RELATIVE VALUATION MATRIX
# ============================================================================
else:  # Relative Valuation Matrix
    st.markdown("### 🎯 Relative Valuation Matrix - All Nifty 50 Stocks")
    
    selected_sectors_matrix = st.multiselect(
        "Select sectors for matrix:",
        sectors,
        default=sectors[:3],
        help="Choose sectors to include in the analysis matrix"
    )
    
    if selected_sectors_matrix:
        st.markdown("---")
        
        matrix_data = []
        
        # Filter stocks by selected sectors
        filtered_tickers = [ticker for ticker, data in NIFTY_50_DATA.items() 
                           if data['Sector'] in selected_sectors_matrix]
        
        with st.spinner("Building Relative Valuation Matrix..."):
            for ticker in filtered_tickers[:20]:  # Limit to 20 for performance
                info = fetch_stock_info(ticker)
                if info:
                    metrics = calculate_valuation_metrics(ticker, info)
                    metrics['Ticker'] = ticker
                    metrics['Company'] = NIFTY_50_DATA[ticker]['Company']
                    metrics['Sector'] = NIFTY_50_DATA[ticker]['Sector']
                    matrix_data.append(metrics)
        
        if matrix_data:
            df_matrix = pd.DataFrame(matrix_data)
            
            # Create heatmap
            st.markdown("### Valuation Heatmap (P/E Ratio)")
            
            heatmap_data = df_matrix[['Company', 'Sector', 'P/E Ratio', 'P/B Ratio', 'EV/EBITDA']].dropna()
            
            if len(heatmap_data) > 0:
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=[heatmap_data['P/E Ratio'], heatmap_data['P/B Ratio'], heatmap_data['EV/EBITDA']],
                    y=['P/E Ratio', 'P/B Ratio', 'EV/EBITDA'],
                    x=heatmap_data['Company'],
                    colorscale='RdYlGn_r',
                    colorbar=dict(title='Valuation Level')
                ))
                
                fig_heatmap.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Sector-wise summary
            st.markdown("### Sector-wise Valuation Summary")
            
            sector_summary = df_matrix.groupby('Sector').agg({
                'P/E Ratio': 'mean',
                'P/B Ratio': 'mean',
                'EV/EBITDA': 'mean',
                'Dividend Yield %': 'mean',
                'Company': 'count'
            }).round(2)
            
            sector_summary.columns = ['Avg P/E', 'Avg P/B', 'Avg EV/EBITDA', 'Avg Div Yield %', 'Stock Count']
            
            st.dataframe(sector_summary, use_container_width=True)
            
            # Box plot for distribution analysis
            st.markdown("### Distribution of P/E Ratios by Sector")
            
            fig_box = px.box(
                df_matrix.dropna(subset=['P/E Ratio']),
                x='Sector',
                y='P/E Ratio',
                title='P/E Ratio Distribution by Sector',
                height=400
            )
            
            fig_box.update_layout(xaxis_tickangle=-45, hovermode='x')
            st.plotly_chart(fig_box, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #003366; font-size: 12px;">
    <p><b>THE MOUNTAIN PATH - WORLD OF FINANCE</b></p>
    <p>Prof. V. Ravichandran | Advanced Finance Education & Research</p>
    <p>Disclaimer: This tool is for educational purposes. Past performance is not indicative of future results. 
    Always conduct your own due diligence before investment decisions.</p>
</div>
""", unsafe_allow_html=True)
