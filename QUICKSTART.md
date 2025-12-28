# QUICK START GUIDE
## THE MOUNTAIN PATH - WORLD OF FINANCE
### Dynamic Nifty Stock Relative Valuation Model

**Prof. V. Ravichandran**  
28+ Years Corporate Finance & Banking Experience

---

## ⚡ 5-MINUTE QUICK START

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed streamlit pandas numpy yfinance plotly scipy...
```

### Step 2: Run the Application
```bash
streamlit run nifty_valuation_model.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 3: Open in Browser
- Automatically opens to http://localhost:8501
- Or manually navigate to the URL shown

### Step 4: Start Analyzing!
1. Select analysis mode from sidebar
2. Choose stocks or sectors
3. Explore the visualizations
4. Review valuation metrics

---

## 📦 INSTALLATION DETAILS

### Windows Users

#### Option 1: Using Command Prompt
```cmd
# Navigate to project folder
cd path\to\nifty-valuation-model

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run nifty_valuation_model.py
```

#### Option 2: Using PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run nifty_valuation_model.py
```

### macOS Users

```bash
# Navigate to project folder
cd path/to/nifty-valuation-model

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run nifty_valuation_model.py
```

### Linux Users

```bash
# Navigate to project folder
cd ~/nifty-valuation-model

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run nifty_valuation_model.py
```

---

## 🔧 TROUBLESHOOTING

### Issue: "Command 'streamlit' not found"

**Solution:**
```bash
# Reinstall streamlit
pip uninstall streamlit -y
pip install streamlit

# Or use python module
python -m streamlit run nifty_valuation_model.py
```

### Issue: "ModuleNotFoundError: No module named 'yfinance'"

**Solution:**
```bash
# Install yfinance
pip install yfinance --upgrade

# Or reinstall all requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: "No module named 'plotly'"

**Solution:**
```bash
pip install plotly --upgrade
```

### Issue: Application runs but no data appears

**Solution:**
1. Check internet connection (needs Yahoo Finance access)
2. Wait 10 seconds for data to load
3. Try refreshing the browser (F5)
4. Restart the application

### Issue: "Port 8501 already in use"

**Solution:**
```bash
# Use different port
streamlit run nifty_valuation_model.py --server.port 8502

# Or kill existing process
# Windows:
netstat -ano | findstr :8501
taskkill /PID [PID] /F

# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

---

## 💡 COMMON USAGE SCENARIOS

### Scenario 1: Analyze a Single Stock (TCS)

1. **Launch Application**
   ```bash
   streamlit run nifty_valuation_model.py
   ```

2. **Select Mode:** "Single Stock Analysis"

3. **Choose Stock:** "TCS" from dropdown

4. **Review Metrics:**
   - Current Price
   - P/E, P/B, P/S Ratios
   - EV/EBITDA
   - Dividend Yield
   - Valuation Signal
   - Price Chart

5. **Interpret Results:**
   - Compare metrics to historical norms
   - Check if undervalued or overvalued
   - Look at trend in price chart

### Scenario 2: Compare Sectors

1. **Select Mode:** "Sector Comparison"

2. **Choose Sector:** "IT & Software"

3. **Review:**
   - All IT companies in table
   - Comparative bar charts for P/E and P/B
   - Sector summary statistics

4. **Identify:**
   - Best and worst valued stocks
   - Sector average metrics
   - Comparative opportunities

### Scenario 3: Build Portfolio Analysis

1. **Select Mode:** "Multi-Stock Comparison"

2. **Choose Stocks (up to 6):**
   - TCS (IT & Software)
   - HDFC Bank (Financial Services)
   - Reliance (Energy)
   - Titan (Consumer FMCG)

3. **Analyze:**
   - Comparative table
   - Radar chart for multi-dimensional view
   - Identify balanced portfolio

### Scenario 4: Market-wide Screening

1. **Select Mode:** "Relative Valuation Matrix"

2. **Choose Sectors:** Select multiple sectors

3. **Generate:**
   - Comprehensive valuation matrix
   - Sector heatmaps
   - Distribution analysis
   - Identify most attractive sectors

---

## 🎯 KEY METRICS EXPLAINED

### Quick Reference Guide

#### **P/E Ratio (Price-to-Earnings)**
```
What: Stock Price / Earnings Per Share
Range: 0 - ∞ (typically 5-50 for Indian stocks)
Low (<12): Usually undervalued
High (>25): Usually overvalued
Use: Quick valuation check
```

#### **P/B Ratio (Price-to-Book)**
```
What: Stock Price / Book Value Per Share
Range: 0 - ∞ (typically 0.5-5)
<1: Trading below book value (deep value)
>3: Potentially overvalued
Use: Asset-based valuation
```

#### **P/S Ratio (Price-to-Sales)**
```
What: Market Cap / Total Revenue
Range: 0 - ∞ (typically 0.5-5)
<1: Potentially undervalued
>3: Potentially overvalued
Use: Less manipulation-prone than P/E
```

#### **EV/EBITDA**
```
What: Enterprise Value / EBITDA
Range: 5-20 (typically)
<8: Potentially undervalued
>15: Potentially overvalued
Use: Capital structure neutral
```

#### **PEG Ratio**
```
What: P/E / Earnings Growth Rate
<1: Undervalued for growth
=1: Fairly valued
>1.5: Overvalued for growth
Use: Growth companies
```

#### **Dividend Yield**
```
What: Annual Dividends / Current Price (%)
Range: 0-10% (typically)
High yield: Income-focused stocks
Low yield: Growth-focused stocks
Use: Income analysis
```

---

## 📊 DATA INTERPRETATION GUIDE

### Understanding Valuation Signals

#### Signal: "Undervalued"
**What it means:**
- Stock trading below intrinsic value
- Favorable valuation metrics
- Potentially good buying opportunity

**Next steps:**
- Check financial health
- Verify earnings quality
- Compare to peers
- Assess growth prospects

#### Signal: "Fair Valued"
**What it means:**
- Stock price reflects fair value
- Metrics aligned with fundamentals
- Balanced risk-reward

**Next steps:**
- Monitor for changes
- Compare relative value
- Check sector trends
- Watch earnings announcements

#### Signal: "Overvalued"
**What it means:**
- Stock trading above intrinsic value
- Premium valuation metrics
- Risk of correction

**Next steps:**
- Identify reason for premium
- Check growth prospects
- Monitor earnings delivery
- Consider waiting for entry

---

## 🔐 DATA FRESHNESS & UPDATES

### Data Update Frequency
- **Stock Prices:** Updated every hour (automatic caching)
- **Company Metrics:** Updated daily
- **Sector Data:** Updated weekly

### Manual Refresh
- **Clear Cache:** Restart the application
- **Force Refresh:** Modify analysis parameters
- **Hard Refresh:** Browser F5 or Ctrl+Shift+R

---

## 📈 ANALYSIS WORKFLOW

### Recommended Analysis Process

#### Step 1: Identify Candidate
```
Start with sector or company interest
↓
Use single stock analysis
↓
Note valuation metrics and signals
```

#### Step 2: Comparative Analysis
```
Identify peer group
↓
Use sector comparison
↓
Compare metrics to peers
```

#### Step 3: Financial Health Check
```
(Use external financial statements)
↓
Check debt levels
↓
Verify earnings quality
↓
Assess cash flows
```

#### Step 4: Risk Assessment
```
(Use financial_risk_modeling.py)
↓
Calculate volatility
↓
Assess drawdown risk
↓
Calculate risk-adjusted returns
```

#### Step 5: Decision
```
Integrate all analyses
↓
Develop investment thesis
↓
Make informed decision
```

---

## 🎓 LEARNING RESOURCES

### Using the Examples

#### Run Educational Examples
```bash
python examples_and_tutorials.py
```

This demonstrates:
- Single stock analysis
- Financial health assessment
- Risk modeling
- Sector analysis
- Portfolio analysis
- Valuation comparisons

### Module Import Examples

#### Example 1: Quick Stock Analysis
```python
from financial_risk_modeling import RelativeValuation

company = {
    'current_price': 2500,
    'earnings_per_share': 150,
    'book_value_per_share': 400,
    'sales_per_share': 1000,
    'ebitda': 50000,
    'revenue': 500000,
    'market_cap': 500000,
    'debt': 100000,
    'cash': 50000,
    'dividends_per_share': 50,
    'earnings_growth_rate': 15
}

model = RelativeValuation(company)
metrics = model.calculate_all_metrics()
score = model.get_valuation_score()

print(f"Valuation Score: {score:.0f}/100")
```

#### Example 2: Risk Analysis
```python
from financial_risk_modeling import FinancialRiskModel
import numpy as np

# Historical daily returns
returns = np.random.normal(0.0005, 0.015, 252)

risk_model = FinancialRiskModel(returns)
metrics = risk_model.calculate_all_risk_metrics()

print(f"Annual Volatility: {metrics['Volatility']*100:.2f}%")
print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
print(f"Max Drawdown: {metrics['Max Drawdown']*100:.2f}%")
```

---

## 🚀 ADVANCED CUSTOMIZATION

### Adding New Stocks

Edit `NIFTY_50_DATA` in `nifty_valuation_model.py`:

```python
NIFTY_50_DATA = {
    'TCS.NS': {'Company': 'TCS', 'Sector': 'IT & Software'},
    'INFY.NS': {'Company': 'Infosys', 'Sector': 'IT & Software'},
    'NEW_SYMBOL.NS': {'Company': 'New Company', 'Sector': 'New Sector'},  # Add here
}
```

### Changing Sector List

```python
# Define custom sectors
custom_sectors = [
    'Pharma & Healthcare',
    'Infrastructure',
    'Consumer Discretionary'
]

# Use in selectbox
selected_sector = st.selectbox("Select Sector:", custom_sectors)
```

### Modifying Valuation Thresholds

Edit the `get_valuation_signal()` function:

```python
def get_valuation_signal(pe, pb, ps):
    signals = []
    
    # Adjust thresholds
    if pe and pe < 14:  # Changed from 12
        signals.append("Undervalued (P/E)")
    elif pe and pe > 28:  # Changed from 25
        signals.append("Overvalued (P/E)")
    
    # ... rest of function
```

---

## ⚙️ PERFORMANCE OPTIMIZATION

### Tips for Faster Performance

1. **Limit Data Loading**
   ```python
   # In nifty_valuation_model.py, reduce number of stocks loaded
   filtered_tickers = filtered_tickers[:15]  # Load only 15 instead of all
   ```

2. **Reduce Update Frequency**
   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def fetch_stock_info(ticker):
       # ... function code
   ```

3. **Use Faster Calculations**
   - Sector comparison over market-wide analysis
   - Single stock analysis over full matrix

---

## 🔐 SECURITY NOTES

### Data Privacy
- All data comes from Yahoo Finance (public source)
- No personal data is collected or stored
- Browser local storage is not used

### Safe Practices
- Don't modify API endpoints
- Keep financial_risk_modeling.py unmodified for reliability
- Test changes in development before deployment

---

## 📞 GETTING HELP

### Common Questions

**Q: How do I interpret P/E ratio?**
A: Lower P/E (12-15) usually indicates undervalued. Higher P/E (>25) indicates overvalued. Compare to sector average and historical levels.

**Q: What's the difference between P/E and PEG?**
A: P/E compares price to current earnings. PEG compares price to earnings growth. PEG is better for growing companies.

**Q: How often is data updated?**
A: Stock prices cached for 1 hour, company metrics for same period. Internet connection required for real-time data.

**Q: Can I use this for actual trading?**
A: This is for educational and analysis purposes. Always conduct your own due diligence and consult advisors before trading.

**Q: What if I need more stocks?**
A: Edit NIFTY_50_DATA dictionary to add more ticker symbols from Yahoo Finance.

---

## 📚 DOCUMENTATION FILES

### Project Structure
```
nifty-valuation-model/
├── nifty_valuation_model.py          # Main Streamlit app
├── financial_risk_modeling.py        # Advanced calculations
├── examples_and_tutorials.py         # Learning examples
├── requirements.txt                  # Dependencies
├── README.md                         # Full documentation
└── QUICKSTART.md                     # This file
```

### File Purposes

| File | Purpose |
|------|---------|
| `nifty_valuation_model.py` | Main user interface |
| `financial_risk_modeling.py` | Backend calculations |
| `examples_and_tutorials.py` | Educational examples |
| `requirements.txt` | Package list |
| `README.md` | Comprehensive guide |
| `QUICKSTART.md` | This quick reference |

---

## ✅ VERIFICATION CHECKLIST

After installation, verify:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created (recommended)
- [ ] Requirements installed: `pip install -r requirements.txt`
- [ ] Can run examples: `python examples_and_tutorials.py`
- [ ] Streamlit runs: `streamlit run nifty_valuation_model.py`
- [ ] Browser opens to http://localhost:8501
- [ ] Can select stocks and view data
- [ ] Charts load correctly
- [ ] All analysis modes work

---

## 🎉 YOU'RE READY!

You now have a powerful financial analysis tool. Start with:

1. **Single Stock Analysis** - Learn one stock well
2. **Sector Comparison** - Compare peers
3. **Portfolio Analysis** - Build your watchlist
4. **Full Matrix** - Market-wide screening

---

## 📧 SUPPORT

For questions or issues:

1. Check README.md for detailed documentation
2. Review examples_and_tutorials.py for code examples
3. Check common troubleshooting section above
4. Verify all dependencies installed

---

## 📝 NOTES

- This tool is for **educational purposes**
- Data comes from Yahoo Finance
- Always verify data from multiple sources
- Consult financial advisors before decisions
- Past performance ≠ future results

---

**Happy Analyzing!** 📊

*The Mountain Path - World of Finance*

---

**Last Updated:** December 2025
**Version:** 1.0
**Status:** Production Ready
