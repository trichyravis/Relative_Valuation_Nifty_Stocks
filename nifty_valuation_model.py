
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
    'ULTRACEMCO.NS': {'Company': 'UltraTech Cement', 'Sector': 'Construction & Materials'},
    'TITAN.NS': {'Company': 'Titan Company', 'Sector': 'Consumer & FMCG'},
    'NTPC.NS': {'Company': 'NTPC', 'Sector': 'Energy & Utilities'},
    'ADANIPORTS.NS': {'Company': 'Adani Ports & SEZ', 'Sector': 'Infrastructure'},
    'BAJAJHLDNG.NS': {'Company': 'Bajaj Holdings', 'Sector': 'Holding Companies'},
    'SBILIFE.NS': {'Company': 'SBI Life Insurance', 'Sector': 'Financial Services'},
    'HEROMOTOCO.NS': {'Company': 'Hero MotoCorp', 'Sector': 'Automobiles'},
    'INDUSIND.NS': {'Company': 'IndusInd Bank', 'Sector': 'Financial Services'},
    'TECHM.NS': {'Company': 'Tech Mahindra', 'Sector': 'IT & Software'},
    'SBIN.NS': {'Company': 'State Bank of India', 'Sector': 'Financial Services'},
    'NESTLEIND.NS': {'Company': 'Nestle India', 'Sector': 'Consumer & FMCG'},
    'ASIANPAINT.NS': {'Company': 'Asian Paints', 'Sector': 'Consumer & FMCG'},
    'LTTS.NS': {'Company': 'LT Technology Services', 'Sector': 'IT & Software'},
    'TATACONSUMER.NS': {'Company': 'Tata Consumer Products', 'Sector': 'Consumer & FMCG'},
    'COALINDIA.NS': {'Company': 'Coal India Limited', 'Sector': 'Metals & Mining'},
    'MARICO.NS': {'Company': 'Marico Limited', 'Sector': 'Consumer & FMCG'},
    'HDFCLIFE.NS': {'Company': 'HDFC Life Insurance', 'Sector': 'Financial Services'},
    'JSWENERGY.NS': {'Company': 'JSW Energy', 'Sector': 'Energy & Utilities'},
    'GAIL.NS': {'Company': 'GAIL India', 'Sector': 'Energy & Utilities'},
    'ONGC.NS': {'Company': 'ONGC Limited', 'Sector': 'Energy & Utilities'},
    'BOSCHIND.NS': {'Company': 'Bosch India', 'Sector': 'Automobiles'},
    'DIVISLAB.NS': {'Company': 'Divi Lab', 'Sector': 'Pharmaceuticals'},
    'CIPLA.NS': {'Company': 'Cipla Limited', 'Sector': 'Pharmaceuticals'},
    'DRREDDY.NS': {'Company': 'Dr Reddy Labs', 'Sector': 'Pharmaceuticals'},
    'BIOCON.NS': {'Company': 'Biocon Limited', 'Sector': 'Pharmaceuticals'},
    'BAJAJXAUSMF.NS': {'Company': 'Bajaj Auto', 'Sector': 'Automobiles'},
    'MCDOWELL.NS': {'Company': 'Mahindra & Mahindra Financial', 'Sector': 'Financial Services'},
    'MM.NS': {'Company': 'Mahindra & Mahindra', 'Sector': 'Automobiles'},
    'LUPIN.NS': {'Company': 'Lupin Limited', 'Sector': 'Pharmaceuticals'},
    'APOLLOHOSP.NS': {'Company': 'Apollo Hospitals Enterprise', 'Sector': 'Healthcare'},
    'BPCL.NS': {'Company': 'Bharat Petroleum Corp', 'Sector': 'Energy & Utilities'},
    'HINDALCO.NS': {'Company': 'Hindalco Industries', 'Sector': 'Metals & Mining'},
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

st.markdown("---")

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
    st.markdown('<div style="color: white; font-weight: bold; margin-bottom: 10px;">SELECT MODE:</div>', unsafe_allow_html=True)
    
    analysis_mode = st.radio(
        "Analysis Mode",
        ["Single Stock Analysis", "Sector Comparison", "Multi-Stock Comparison", 
         "Relative Valuation Matrix"],
        label_visibility="collapsed",
        help="Choose how you want to analyze stocks"
    )
    
    # Time Period Selection
    st.markdown('<div style="color: white; font-weight: bold; margin-bottom: 10px; margin-top: 20px;">TIME PERIOD:</div>', unsafe_allow_html=True)
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
    st.markdown('<div style="color: white; font-weight: bold;">ABOUT THIS TOOL</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: #ffffff; font-size: 12px; line-height: 1.8;">
    📊 <b>Valuation</b> - P/E, P/B, P/S Multiples<br>
    ⚙️ <b>EV/EBITDA</b> - Enterprise Value<br>
    🎯 <b>Sector Peers</b> - Comparables<br>
    📈 <b>Implied Prices</b> - Fair Values<br>
    🔍 <b>Signals</b> - Buy/Hold/Sell
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Author Info
    st.markdown("""
    <div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 6px; border-left: 3px solid #FFD700;">
        <div style="font-weight: bold; color: #FFD700; font-size: 14px;">Prof. V. Ravichandran</div>
        <div style="color: #b3d9ff; font-size: 11px; line-height: 1.6; margin-top: 8px;">
        📚 28+ Years Corporate Finance & Banking<br>
        🎓 10+ Years Academic Excellence
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

# ============================================================================
# ANALYSIS MODE: SINGLE STOCK ANALYSIS
# ============================================================================
if analysis_mode == "Single Stock Analysis":
    # Enhanced stock selection header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a4d7a 0%, #2d6fa3 100%); 
                padding: 20px; border-radius: 12px; margin-bottom: 20px;
                border-left: 6px solid #ffd700; box-shadow: 0 4px 15px rgba(0, 51, 102, 0.3);">
        <h2 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: bold;">
            🔍 SELECT YOUR STOCK
        </h2>
        <p style="color: #b0d4ff; margin: 8px 0 0 0; font-size: 13px;">
            Choose from 50 NIFTY companies to analyze valuations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_ticker = st.selectbox(
            "📊 **Select Stock From List:**",
            list(NIFTY_50_DATA.keys()),
            format_func=lambda x: f"🏢 {NIFTY_50_DATA[x]['Company']} ({x})",
            label_visibility="visible"
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
        
        # Enhanced expandable detailed analysis with attractive styling
        with st.expander(""):
            pass
        
        # Custom styled header for detailed breakdown
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a4d7a 0%, #2d6fa3 100%); 
                    padding: 20px 25px; border-radius: 12px; margin: 20px 0; 
                    border-left: 6px solid #ffd700; cursor: pointer; 
                    box-shadow: 0 4px 15px rgba(0, 51, 102, 0.3);">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h2 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">
                        📊 DETAILED VALUATION BREAKDOWN
                    </h2>
                    <p style="color: #b0d4ff; margin: 8px 0 0 0; font-size: 13px;">
                        Click below to explore comprehensive valuation analysis
                    </p>
                </div>
                <div style="font-size: 32px;">📈</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("**Show Full Analysis →**", expanded=False):
            
            # -------- COMPARABLE MULTIPLES SECTION --------
            st.markdown('<div style="background-color: #f0f7ff; padding: 15px; border-left: 5px solid #003366; border-radius: 8px; margin-bottom: 20px;"><h3 style="color: #003366; margin: 0 0 10px 0;">💰 COMPARABLE MULTIPLES VALUATION</h3></div>', unsafe_allow_html=True)
            
            sector = NIFTY_50_DATA[selected_ticker]['Sector']
            
            # Display sector info prominently
            col_sector_info1, col_sector_info2 = st.columns([1, 3])
            with col_sector_info1:
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 12px; border-radius: 6px; text-align: center;">
                    <div style="font-size: 12px; color: #666;">SECTOR</div>
                    <div style="font-weight: bold; color: #003366; margin-top: 5px; font-size: 14px;">{sector}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Get peer companies in same sector
            peer_companies = [
                (ticker, data['Company']) 
                for ticker, data in NIFTY_50_DATA.items() 
                if data['Sector'] == sector and ticker != selected_ticker
            ]
            
            if peer_companies:
                with col_sector_info2:
                    st.markdown(f"""
                    <div style="background-color: #f3e5f5; padding: 12px; border-radius: 6px;">
                        <div style="font-size: 12px; color: #666; margin-bottom: 8px;">👥 PEER COMPANIES ({len(peer_companies[:5])} selected)</div>
                        <div style="font-weight: bold; color: #6a1b9a; font-size: 13px; line-height: 1.6;">
                        {', '.join([name for _, name in peer_companies[:5]])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Fetch metrics for peer companies
                peer_metrics = []
                st.markdown("**📊 Fetching peer company multiples...**")
                for peer_ticker, peer_name in peer_companies[:5]:
                    peer_info = fetch_stock_info(peer_ticker)
                    if peer_info:
                        peer_data = {
                            'Company': peer_name,
                            'P/E': peer_info.get('trailingPE'),
                            'P/B': peer_info.get('priceToBook'),
                            'P/S': peer_info.get('priceToSalesTrailing12Months'),
                            'EV/EBITDA': peer_info.get('enterpriseToEbitda'),
                        }
                        peer_metrics.append(peer_data)
                
                if peer_metrics:
                    st.markdown("**Peer Company Multiples:**")
                    df_peers = pd.DataFrame(peer_metrics)
                    
                    # Format for display
                    df_peers_display = df_peers.copy()
                    for col in ['P/E', 'P/B', 'P/S', 'EV/EBITDA']:
                        df_peers_display[col] = df_peers_display[col].apply(
                            lambda x: f"{x:.2f}x" if pd.notna(x) else "N/A"
                        )
                    
                    st.dataframe(df_peers_display, use_container_width=True, hide_index=True)
                    
                    st.markdown("---")
                    
                    # Calculate sector average multiples
                    st.markdown("**Sector Average Multiples:**")
                    
                    sector_pe_avg = df_peers[df_peers['P/E'].notna()]['P/E'].mean() if len(df_peers['P/E'].dropna()) > 0 else metrics.get('P/E Ratio')
                    sector_pb_avg = df_peers[df_peers['P/B'].notna()]['P/B'].mean() if len(df_peers['P/B'].dropna()) > 0 else metrics.get('P/B Ratio')
                    sector_ps_avg = df_peers[df_peers['P/S'].notna()]['P/S'].mean() if len(df_peers['P/S'].dropna()) > 0 else metrics.get('P/S Ratio')
                    sector_ev_avg = df_peers[df_peers['EV/EBITDA'].notna()]['EV/EBITDA'].mean() if len(df_peers['EV/EBITDA'].dropna()) > 0 else metrics.get('EV/EBITDA')
                    
                    col_sector1, col_sector2, col_sector3, col_sector4 = st.columns(4)
                    
                    with col_sector1:
                        st.metric("Avg P/E", f"{sector_pe_avg:.2f}x" if sector_pe_avg else "N/A")
                    with col_sector2:
                        st.metric("Avg P/B", f"{sector_pb_avg:.2f}x" if sector_pb_avg else "N/A")
                    with col_sector3:
                        st.metric("Avg P/S", f"{sector_ps_avg:.2f}x" if sector_ps_avg else "N/A")
                    with col_sector4:
                        st.metric("Avg EV/EBITDA", f"{sector_ev_avg:.2f}x" if sector_ev_avg else "N/A")
                    
                    st.markdown("---")
                    
                    # Implied valuation comparison
                    st.markdown("**Implied Valuation vs Peer Multiples:**")
                    
                    current_price = metrics.get('Current Price', 0)
                    shares_outstanding = info.get('sharesOutstanding', 1000000) / 1000000  # in millions
                    
                    implied_data = []
                    
                    # P/E based valuation
                    if metrics.get('P/E Ratio') and sector_pe_avg:
                        pe_multiple = sector_pe_avg
                        net_income = info.get('marketCap', 0) / (metrics.get('P/E Ratio', 1) or 1)
                        implied_price_pe = net_income / shares_outstanding if shares_outstanding > 0 else current_price
                        upside_pe = ((implied_price_pe - current_price) / current_price * 100) if current_price > 0 else 0
                        implied_data.append({
                            'Method': 'P/E Ratio',
                            'Sector Multiple': f"{pe_multiple:.2f}x",
                            'Implied Price': f"₹{implied_price_pe:.0f}",
                            'Upside/Downside': f"{upside_pe:+.1f}%"
                        })
                    
                    # P/B based valuation
                    if metrics.get('P/B Ratio') and sector_pb_avg:
                        pb_multiple = sector_pb_avg
                        book_value = info.get('marketCap', 0) / (metrics.get('P/B Ratio', 1) or 1)
                        implied_price_pb = book_value / shares_outstanding if shares_outstanding > 0 else current_price
                        upside_pb = ((implied_price_pb - current_price) / current_price * 100) if current_price > 0 else 0
                        implied_data.append({
                            'Method': 'P/B Ratio',
                            'Sector Multiple': f"{pb_multiple:.2f}x",
                            'Implied Price': f"₹{implied_price_pb:.0f}",
                            'Upside/Downside': f"{upside_pb:+.1f}%"
                        })
                    
                    # P/S based valuation
                    if metrics.get('P/S Ratio') and sector_ps_avg:
                        ps_multiple = sector_ps_avg
                        revenue = info.get('marketCap', 0) / (metrics.get('P/S Ratio', 1) or 1)
                        implied_price_ps = revenue / shares_outstanding if shares_outstanding > 0 else current_price
                        upside_ps = ((implied_price_ps - current_price) / current_price * 100) if current_price > 0 else 0
                        implied_data.append({
                            'Method': 'P/S Ratio',
                            'Sector Multiple': f"{ps_multiple:.2f}x",
                            'Implied Price': f"₹{implied_price_ps:.0f}",
                            'Upside/Downside': f"{upside_ps:+.1f}%"
                        })
                    
                    # EV/EBITDA based valuation
                    if metrics.get('EV/EBITDA') and sector_ev_avg:
                        ev_multiple = sector_ev_avg
                        ebitda = (info.get('marketCap', 0) + info.get('totalDebt', 0) - info.get('totalCash', 0)) / (metrics.get('EV/EBITDA', 1) or 1)
                        implied_price_ev = ebitda / shares_outstanding if shares_outstanding > 0 else current_price
                        upside_ev = ((implied_price_ev - current_price) / current_price * 100) if current_price > 0 else 0
                        implied_data.append({
                            'Method': 'EV/EBITDA',
                            'Sector Multiple': f"{ev_multiple:.2f}x",
                            'Implied Price': f"₹{implied_price_ev:.0f}",
                            'Upside/Downside': f"{upside_ev:+.1f}%"
                        })
                    
                    if implied_data:
                        df_implied = pd.DataFrame(implied_data)
                        st.dataframe(df_implied, use_container_width=True, hide_index=True)
                        
                        st.info(
                            f"""
                            **Current Price:** ₹{current_price:.0f}
                            
                            Green = Undervalued | Yellow = Fair Value | Red = Overvalued
                            """
                        )
            
            st.markdown("---")
            
            # METRIC-BY-METRIC ANALYSIS
            st.subheader("🔍 Metric Analysis")
            
            for idx, (metric_name, metric_data) in enumerate(signal_analysis['metrics'].items(), 1):
                colors_map = {
                    'green': ('#2ecc71', '#d4edda', '#155724'),
                    'lightgreen': ('#7cb342', '#e8f5e9', '#2e7d32'),
                    'yellow': ('#f1c40f', '#fff3cd', '#856404'),
                    'orange': ('#ff9800', '#fff3e0', '#e65100'),
                    'red': ('#e74c3c', '#f8d7da', '#721c24')
                }
                
                color_tuple = colors_map.get(metric_data['color'], ('#95a5a6', '#f0f0f0', '#555'))
                main_color, bg_color, text_color = color_tuple
                signal_emoji = '🟢' if metric_data['status'] == 'Undervalued' else ('🟡' if metric_data['status'] == 'Fair' else '🔴')
                
                html_block = f"""
                <div style="background-color: {bg_color}; border-left: 5px solid {main_color}; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div style="font-weight: bold; font-size: 16px; color: {text_color};">{idx}. {metric_name}</div>
                        <div style="background-color: {main_color}; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 14px;">{metric_data['value']:.2f}x</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <div style="margin-bottom: 10px;"><span style="font-weight: bold; color: {text_color};">Status:</span> <span style="color: {text_color};">{signal_emoji} {metric_data['status']}</span></div>
                            <div><span style="font-weight: bold; color: {text_color};">Severity:</span> <span style="background-color: {main_color}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px;">{metric_data['severity']}</span></div>
                        </div>
                        <div>
                            <div style="font-weight: bold; color: {text_color}; margin-bottom: 5px;">💡 Reasoning:</div>
                            <div style="color: {text_color}; font-size: 13px;">{metric_data['reasoning']}</div>
                        </div>
                    </div>
                    <div style="margin-top: 12px;">
                        <div style="font-weight: bold; color: {text_color}; font-size: 12px; margin-bottom: 5px;">Valuation Level:</div>
                        <div style="width: 100%; height: 8px; background-color: #e0e0e0; border-radius: 4px; overflow: hidden;">
                            <div style="width: {min(max((metric_data['value'] / 30) * 100, 5), 100)}%; height: 100%; background: linear-gradient(90deg, #2ecc71 0%, #f1c40f 50%, #e74c3c 100%);"></div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(html_block, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # VALUATION SCORE BREAKDOWN
            st.subheader("📊 Valuation Score Breakdown")
            
            score_col1, score_col2, score_col3, score_col4 = st.columns(4)
            
            undervalued_count = signal_analysis['undervalued_count']
            fair_count = signal_analysis['fair_count']
            overvalued_count = signal_analysis['overvalued_count']
            total_metrics = max(undervalued_count + fair_count + overvalued_count, 1)
            
            with score_col1:
                st.markdown(f"""<div style="background-color: #d4edda; border-left: 4px solid #28a745; padding: 15px; border-radius: 6px; text-align: center;"><div style="font-size: 28px;">🟢</div><div style="font-weight: bold; color: #155724; margin: 8px 0;">Undervalued</div><div style="font-size: 24px; font-weight: bold; color: #28a745;">{undervalued_count}</div><div style="font-size: 11px; color: #155724; margin-top: 5px;">{(undervalued_count/total_metrics)*100:.0f}%</div></div>""", unsafe_allow_html=True)
            
            with score_col2:
                st.markdown(f"""<div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 6px; text-align: center;"><div style="font-size: 28px;">🟡</div><div style="font-weight: bold; color: #856404; margin: 8px 0;">Fair Valued</div><div style="font-size: 24px; font-weight: bold; color: #ffc107;">{fair_count}</div><div style="font-size: 11px; color: #856404; margin-top: 5px;">{(fair_count/total_metrics)*100:.0f}%</div></div>""", unsafe_allow_html=True)
            
            with score_col3:
                st.markdown(f"""<div style="background-color: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; border-radius: 6px; text-align: center;"><div style="font-size: 28px;">🔴</div><div style="font-weight: bold; color: #721c24; margin: 8px 0;">Overvalued</div><div style="font-size: 24px; font-weight: bold; color: #dc3545;">{overvalued_count}</div><div style="font-size: 11px; color: #721c24; margin-top: 5px;">{(overvalued_count/total_metrics)*100:.0f}%</div></div>""", unsafe_allow_html=True)
            
            with score_col4:
                st.markdown(f"""<div style="background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; border-radius: 6px; text-align: center;"><div style="font-size: 28px;">📊</div><div style="font-weight: bold; color: #0d47a1; margin: 8px 0;">Total</div><div style="font-size: 24px; font-weight: bold; color: #2196f3;">{total_metrics}</div><div style="font-size: 11px; color: #0d47a1; margin-top: 5px;">Metrics</div></div>""", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # INVESTMENT RECOMMENDATION
            st.subheader("💡 Investment Recommendation")
            
            if "UNDERVALUED" in signal_analysis['overall']:
                rec_text = "🟢 **BUY SIGNAL** - Stock appears undervalued. Potential for upside returns."
                rec_color = "#d4edda"
                rec_border = "#28a745"
            elif "FAIRLY" in signal_analysis['overall']:
                rec_text = "🟡 **HOLD SIGNAL** - Stock at reasonable valuations. Balanced risk-reward."
                rec_color = "#fff3cd"
                rec_border = "#ffc107"
            else:
                rec_text = "🔴 **SELL SIGNAL** - Stock appears overvalued. Limited upside, downside risk."
                rec_color = "#f8d7da"
                rec_border = "#dc3545"
            
            st.markdown(f"""<div style="background-color: {rec_color}; border-left: 5px solid {rec_border}; padding: 15px; border-radius: 8px;">{rec_text}</div>""", unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("⚠️ This analysis is educational. Always conduct due diligence and consult financial advisors before investing.")
        
        st.markdown("---")
        
        # Price Chart
        st.markdown("### 📉 PRICE CHART & TECHNICAL ANALYSIS")
        
        hist_data = fetch_stock_data(selected_ticker, period)
        
        if hist_data is not None and len(hist_data) > 0:
            try:
                # Extract close prices - handle all formats
                try:
                    if isinstance(hist_data.columns, pd.MultiIndex):
                        close_prices = hist_data[('Close', selected_ticker)]
                    else:
                        close_prices = hist_data['Close']
                except:
                    close_prices = hist_data['Close'] if 'Close' in hist_data.columns else hist_data.iloc[:, 0]
                
                # Ensure 1D array
                if isinstance(close_prices, pd.DataFrame):
                    close_prices = close_prices.iloc[:, 0]
                
                close_prices = pd.to_numeric(close_prices, errors='coerce')
                
                # Create clean dataframe
                df = pd.DataFrame({
                    'Date': close_prices.index,
                    'Close': close_prices.values
                }).dropna()
                
                if len(df) < 5:
                    st.info("Insufficient data points for chart")
                else:
                    # Calculate moving averages
                    df['MA20'] = df['Close'].rolling(window=20, min_periods=1).mean()
                    df['MA50'] = df['Close'].rolling(window=50, min_periods=1).mean()
                    
                    # Create chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=df['Date'], 
                        y=df['Close'], 
                        name='Close Price', 
                        line=dict(color='#003366', width=3)
                    ))
                    fig.add_trace(go.Scatter(
                        x=df['Date'], 
                        y=df['MA20'], 
                        name='20-Day MA', 
                        line=dict(color='#4472C4', width=2, dash='dash')
                    ))
                    fig.add_trace(go.Scatter(
                        x=df['Date'], 
                        y=df['MA50'], 
                        name='50-Day MA', 
                        line=dict(color='#FF7C1F', width=2, dash='dot')
                    ))
                    
                    fig.update_layout(
                        title=f'{company_name} - Stock Price Analysis ({period})',
                        xaxis_title='Date',
                        yaxis_title='Price (₹)',
                        template='plotly_white',
                        height=450,
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Chart Error: {str(e)}")
                st.info("Try selecting a different time period or stock")
        else:
            st.warning("No historical data available")

elif analysis_mode == "Sector Comparison":
    st.markdown("### 📊 SECTOR COMPARISON ANALYSIS")
    st.markdown("---")
    
    # Select sector
    sectors = sorted(list(set([data['Sector'] for data in NIFTY_50_DATA.values()])))
    selected_sector = st.selectbox("Select Sector:", sectors)
    
    # Get all stocks in sector
    sector_stocks = [(ticker, data['Company']) for ticker, data in NIFTY_50_DATA.items() 
                     if data['Sector'] == selected_sector]
    
    if sector_stocks:
        st.write(f"**Stocks in {selected_sector} Sector:** {len(sector_stocks)}")
        
        # Fetch data for all stocks in sector
        sector_data = []
        with st.spinner(f"Analyzing {selected_sector} sector..."):
            for ticker, company_name in sector_stocks:
                info = fetch_stock_info(ticker)
                if info:
                    sector_data.append({
                        'Company': company_name,
                        'Ticker': ticker,
                        'Price': info.get('currentPrice'),
                        'P/E': info.get('trailingPE'),
                        'P/B': info.get('priceToBook'),
                        'P/S': info.get('priceToSalesTrailing12Months'),
                        'Market Cap (B)': info.get('marketCap', 0) / 1e9 if info.get('marketCap') else 0,
                    })
        
        if sector_data:
            df_sector = pd.DataFrame(sector_data)
            
            # Display comparison table
            st.markdown("**Sector Stocks Valuation Comparison:**")
            st.dataframe(
                df_sector.style.format({
                    'Price': '₹{:.0f}',
                    'P/E': '{:.2f}x',
                    'P/B': '{:.2f}x',
                    'P/S': '{:.2f}x',
                    'Market Cap (B)': '₹{:.0f}B'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Sector averages
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_pe = df_sector['P/E'].mean()
                st.metric("Avg P/E", f"{avg_pe:.2f}x" if pd.notna(avg_pe) else "N/A")
            
            with col2:
                avg_pb = df_sector['P/B'].mean()
                st.metric("Avg P/B", f"{avg_pb:.2f}x" if pd.notna(avg_pb) else "N/A")
            
            with col3:
                avg_ps = df_sector['P/S'].mean()
                st.metric("Avg P/S", f"{avg_ps:.2f}x" if pd.notna(avg_ps) else "N/A")
            
            with col4:
                total_market_cap = df_sector['Market Cap (B)'].sum()
                st.metric("Total Mkt Cap", f"₹{total_market_cap:.0f}B")
            
            st.markdown("---")
            st.info("**Insight:** Stocks with P/E, P/B, P/S below sector averages are relatively undervalued within the sector.")

elif analysis_mode == "Multi-Stock Comparison":
    st.markdown("### 📊 MULTI-STOCK COMPARISON")
    st.markdown("---")
    
    # Select multiple stocks
    all_tickers = [ticker for ticker in NIFTY_50_DATA.keys()]
    all_companies = [f"{ticker} - {NIFTY_50_DATA[ticker]['Company']}" for ticker in all_tickers]
    
    selected_companies = st.multiselect(
        "Select stocks to compare (choose 2-5 stocks):",
        all_companies,
        default=[all_companies[0], all_companies[1]]
    )
    
    if selected_companies:
        selected_tickers = [comp.split(" - ")[0] for comp in selected_companies]
        
        # Fetch data for selected stocks
        comparison_data = []
        with st.spinner("Analyzing selected stocks..."):
            for ticker in selected_tickers:
                info = fetch_stock_info(ticker)
                if info:
                    comparison_data.append({
                        'Company': NIFTY_50_DATA[ticker]['Company'],
                        'Ticker': ticker,
                        'Sector': NIFTY_50_DATA[ticker]['Sector'],
                        'Price': info.get('currentPrice'),
                        'P/E': info.get('trailingPE'),
                        'P/B': info.get('priceToBook'),
                        'P/S': info.get('priceToSalesTrailing12Months'),
                        'Dividend Yield %': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                    })
        
        if comparison_data:
            df_compare = pd.DataFrame(comparison_data)
            
            st.markdown("**Multi-Stock Comparison Table:**")
            st.dataframe(
                df_compare.style.format({
                    'Price': '₹{:.0f}',
                    'P/E': '{:.2f}x',
                    'P/B': '{:.2f}x',
                    'P/S': '{:.2f}x',
                    'Dividend Yield %': '{:.2f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Comparative metrics
            st.markdown("**Comparative Analysis:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_pe_stock = df_compare.loc[df_compare['P/E'].idxmin(), 'Company']
                min_pe = df_compare['P/E'].min()
                st.write(f"**Lowest P/E:** {min_pe_stock}\n{min_pe:.2f}x")
            
            with col2:
                min_pb_stock = df_compare.loc[df_compare['P/B'].idxmin(), 'Company']
                min_pb = df_compare['P/B'].min()
                st.write(f"**Lowest P/B:** {min_pb_stock}\n{min_pb:.2f}x")
            
            with col3:
                max_div_stock = df_compare.loc[df_compare['Dividend Yield %'].idxmax(), 'Company']
                max_div = df_compare['Dividend Yield %'].max()
                st.write(f"**Highest Dividend:** {max_div_stock}\n{max_div:.2f}%")
            
            st.markdown("---")
            st.success(f"Comparing {len(selected_tickers)} stocks across key valuation metrics.")

else:  # Relative Valuation Matrix
    st.markdown("### 📊 RELATIVE VALUATION MATRIX")
    st.markdown("---")
    
    st.write("**All NIFTY 50 Stocks Valuation Matrix**")
    
    # Fetch all stocks data
    all_matrix_data = []
    with st.spinner("Building valuation matrix for all NIFTY 50 stocks..."):
        for ticker in NIFTY_50_DATA.keys():
            info = fetch_stock_info(ticker)
            if info:
                all_matrix_data.append({
                    'Ticker': ticker,
                    'Company': NIFTY_50_DATA[ticker]['Company'],
                    'Sector': NIFTY_50_DATA[ticker]['Sector'],
                    'Price': info.get('currentPrice'),
                    'P/E': info.get('trailingPE'),
                    'P/B': info.get('priceToBook'),
                    'EV/EBITDA': info.get('enterpriseToEbitda'),
                })
    
    if all_matrix_data:
        df_matrix = pd.DataFrame(all_matrix_data)
        
        # Filter by sector if needed
        sectors = sorted(df_matrix['Sector'].unique())
        sector_filter = st.selectbox("Filter by Sector (optional):", ["All Sectors"] + sectors)
        
        if sector_filter != "All Sectors":
            df_matrix = df_matrix[df_matrix['Sector'] == sector_filter]
        
        st.markdown(f"**Showing {len(df_matrix)} stocks**")
        
        st.dataframe(
            df_matrix.style.format({
                'Price': '₹{:.0f}',
                'P/E': '{:.2f}x',
                'P/B': '{:.2f}x',
                'EV/EBITDA': '{:.2f}x'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Summary statistics
        st.markdown("**Matrix Summary Statistics:**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Median P/E", f"{df_matrix['P/E'].median():.2f}x")
        
        with col2:
            st.metric("Median P/B", f"{df_matrix['P/B'].median():.2f}x")
        
        with col3:
            st.metric("Median EV/EBITDA", f"{df_matrix['EV/EBITDA'].median():.2f}x")
        
        with col4:
            st.metric("Total Stocks", len(df_matrix))
        
        st.markdown("---")
        st.info("Use this matrix to identify undervalued and overvalued stocks across the entire NIFTY 50 index.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #003366; font-size: 12px;">
    <p><b>THE MOUNTAIN PATH - WORLD OF FINANCE</b></p>
    <p>Prof. V. Ravichandran | Advanced Finance Education & Research</p>
</div>
""", unsafe_allow_html=True)
