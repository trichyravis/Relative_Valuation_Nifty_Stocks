
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

def get_valuation_signal(pe, pb, ps):
    """Generate valuation signal based on multiples"""
    signals = []
    
    if pe and pe < 15:
        signals.append("Undervalued (P/E)")
    elif pe and pe > 25:
        signals.append("Overvalued (P/E)")
    
    if pb and pb < 1:
        signals.append("Undervalued (P/B)")
    elif pb and pb > 3:
        signals.append("Overvalued (P/B)")
    
    if ps and ps < 1:
        signals.append("Undervalued (P/S)")
    elif ps and ps > 3:
        signals.append("Overvalued (P/S)")
    
    if not signals:
        signals.append("Fair Valued")
    
    return ", ".join(signals)

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
    st.markdown("### ⚙️ ANALYSIS PARAMETERS")
    
    analysis_mode = st.radio(
        "Select Analysis Mode:",
        ["Single Stock Analysis", "Sector Comparison", "Multi-Stock Comparison", 
         "Relative Valuation Matrix"],
        help="Choose how you want to analyze stocks"
    )
    
    period = st.selectbox(
        "Select Time Period:",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        help="Historical data period for charts"
    )
    
    sectors = list(set([data['Sector'] for data in NIFTY_50_DATA.values()]))
    sectors.sort()
    
    st.markdown("---")

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
            signal = get_valuation_signal(
                metrics.get('P/E Ratio'),
                metrics.get('P/B Ratio'),
                metrics.get('P/S Ratio')
            )
            st.markdown(f"""
            <div class="metric-card">
            <div style="text-align: center; padding: 20px;">
                <div style="color: #003366; font-size: 18px; font-weight: bold; margin-bottom: 10px;">
                {signal}
                </div>
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
