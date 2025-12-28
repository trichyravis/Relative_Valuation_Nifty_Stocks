
"""
FINANCIAL RISK MODELING MODULE
Advanced Relative Valuation & Risk Analysis Framework
Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience

This module provides comprehensive tools for:
1. Relative Valuation Analysis (P/E, P/B, P/S, EV/EBITDA)
2. Financial Risk Modeling (VAR, CVaR, Sharpe Ratio)
3. Portfolio Risk Assessment
4. Sector Risk Metrics
5. Liquidity & Solvency Analysis
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. RELATIVE VALUATION MODULE
# ============================================================================

class RelativeValuation:
    """
    Comprehensive Relative Valuation Analysis
    
    Valuation Multiples:
    - Earnings Multiple: P/E Ratio
    - Book Value Multiple: P/B Ratio
    - Sales Multiple: P/S Ratio
    - Enterprise Value Multiples: EV/EBITDA, EV/Revenue
    - PEG Ratio (Price/Earnings to Growth)
    - Dividend Yield
    """
    
    def __init__(self, company_data):
        """
        Initialize with company financial data
        
        company_data: dict with keys:
        - current_price: float
        - earnings_per_share: float
        - book_value_per_share: float
        - sales_per_share: float
        - ebitda: float
        - revenue: float
        - market_cap: float
        - debt: float
        - cash: float
        - dividends_per_share: float
        - earnings_growth_rate: float
        """
        self.data = company_data
        self.valuation_metrics = {}
        self.risk_signals = []
        
    def calculate_pe_ratio(self):
        """
        Price-to-Earnings Ratio
        P/E = Current Price / Earnings Per Share
        
        Interpretation:
        - P/E < 12: Potentially Undervalued
        - P/E 12-18: Fair Value
        - P/E > 25: Potentially Overvalued
        """
        if self.data.get('earnings_per_share', 0) == 0:
            return None
        
        pe = self.data['current_price'] / self.data['earnings_per_share']
        self.valuation_metrics['P/E'] = pe
        
        if pe < 12:
            self.risk_signals.append("P/E suggests undervaluation")
        elif pe > 25:
            self.risk_signals.append("P/E suggests overvaluation")
        
        return pe
    
    def calculate_pb_ratio(self):
        """
        Price-to-Book Ratio
        P/B = Current Price / Book Value Per Share
        
        Interpretation:
        - P/B < 1: Trading below book value (potential value play)
        - P/B 1-3: Fair value range
        - P/B > 3: Potentially overvalued
        """
        if self.data.get('book_value_per_share', 0) == 0:
            return None
        
        pb = self.data['current_price'] / self.data['book_value_per_share']
        self.valuation_metrics['P/B'] = pb
        
        if pb < 1:
            self.risk_signals.append("P/B suggests deep value opportunity")
        elif pb > 3:
            self.risk_signals.append("P/B suggests potential overvaluation")
        
        return pb
    
    def calculate_ps_ratio(self):
        """
        Price-to-Sales Ratio
        P/S = Market Cap / Total Sales Revenue
        
        Advantages: Not affected by accounting policies
        Interpretation:
        - P/S < 1: Undervalued
        - P/S 1-3: Fair value
        - P/S > 3: Potentially overvalued
        """
        if self.data.get('sales_per_share', 0) == 0:
            return None
        
        ps = self.data['current_price'] / self.data['sales_per_share']
        self.valuation_metrics['P/S'] = ps
        
        return ps
    
    def calculate_ev_ebitda(self):
        """
        Enterprise Value / EBITDA Multiple
        EV = Market Cap + Debt - Cash
        EV/EBITDA = (Market Cap + Debt - Cash) / EBITDA
        
        This is capital structure neutral
        Interpretation:
        - EV/EBITDA < 8: Potentially undervalued
        - EV/EBITDA 8-12: Fair value
        - EV/EBITDA > 15: Potentially overvalued
        """
        enterprise_value = (self.data['market_cap'] + 
                           self.data.get('debt', 0) - 
                           self.data.get('cash', 0))
        
        if self.data.get('ebitda', 0) == 0:
            return None
        
        ev_ebitda = enterprise_value / self.data['ebitda']
        self.valuation_metrics['EV/EBITDA'] = ev_ebitda
        
        if ev_ebitda < 8:
            self.risk_signals.append("EV/EBITDA suggests undervaluation")
        elif ev_ebitda > 15:
            self.risk_signals.append("EV/EBITDA suggests overvaluation")
        
        return ev_ebitda
    
    def calculate_peg_ratio(self):
        """
        Price/Earnings to Growth Ratio
        PEG = P/E Ratio / Earnings Growth Rate (%)
        
        Interpretation:
        - PEG < 1: Stock may be undervalued relative to growth
        - PEG = 1: Fair valuation
        - PEG > 1: Stock may be overvalued relative to growth
        
        Better than P/E for high-growth companies
        """
        pe = self.valuation_metrics.get('P/E')
        if pe is None:
            pe = self.calculate_pe_ratio()
        
        earnings_growth = self.data.get('earnings_growth_rate', 0)
        
        if earnings_growth == 0 or pe is None:
            return None
        
        peg = pe / earnings_growth
        self.valuation_metrics['PEG'] = peg
        
        if peg < 1:
            self.risk_signals.append("PEG suggests undervaluation for growth rate")
        elif peg > 1.5:
            self.risk_signals.append("PEG suggests overvaluation for growth rate")
        
        return peg
    
    def calculate_dividend_yield(self):
        """
        Dividend Yield
        Dividend Yield = Annual Dividends Per Share / Current Price
        
        Expressed as percentage
        """
        if self.data['current_price'] == 0:
            return None
        
        div_yield = (self.data.get('dividends_per_share', 0) / 
                    self.data['current_price']) * 100
        
        self.valuation_metrics['Dividend Yield %'] = div_yield
        
        return div_yield
    
    def calculate_all_metrics(self):
        """Calculate all relative valuation metrics at once"""
        self.calculate_pe_ratio()
        self.calculate_pb_ratio()
        self.calculate_ps_ratio()
        self.calculate_ev_ebitda()
        self.calculate_peg_ratio()
        self.calculate_dividend_yield()
        
        return self.valuation_metrics
    
    def get_valuation_score(self):
        """
        Generate composite valuation score (0-100)
        Higher score = More undervalued
        """
        score = 50  # Neutral starting point
        
        pe = self.valuation_metrics.get('P/E')
        if pe and pe < 15:
            score += 10
        elif pe and pe > 25:
            score -= 10
        
        pb = self.valuation_metrics.get('P/B')
        if pb and pb < 1:
            score += 15
        elif pb and pb > 3:
            score -= 10
        
        ps = self.valuation_metrics.get('P/S')
        if ps and ps < 1:
            score += 10
        elif ps and ps > 3:
            score -= 10
        
        ev_ebitda = self.valuation_metrics.get('EV/EBITDA')
        if ev_ebitda and ev_ebitda < 8:
            score += 10
        elif ev_ebitda and ev_ebitda > 15:
            score -= 10
        
        peg = self.valuation_metrics.get('PEG')
        if peg and peg < 1:
            score += 10
        
        return np.clip(score, 0, 100)

# ============================================================================
# 2. FINANCIAL RISK MODELING
# ============================================================================

class FinancialRiskModel:
    """
    Advanced Financial Risk Analysis
    
    Risk Metrics:
    - Value at Risk (VAR)
    - Conditional Value at Risk (CVaR/Expected Shortfall)
    - Sharpe Ratio
    - Sortino Ratio
    - Maximum Drawdown
    - Beta
    - Financial Leverage Risk
    """
    
    def __init__(self, returns_data, market_returns=None, risk_free_rate=0.04):
        """
        Initialize risk model
        
        returns_data: array of historical returns
        market_returns: array of market returns (for beta calculation)
        risk_free_rate: annual risk-free rate (default 4% for India)
        """
        self.returns = np.array(returns_data)
        self.market_returns = np.array(market_returns) if market_returns is not None else None
        self.risk_free_rate = risk_free_rate
        self.risk_metrics = {}
    
    def calculate_var(self, confidence_level=0.95):
        """
        Value at Risk (VAR)
        VAR(95%) = Maximum expected loss with 95% confidence
        
        Using historical simulation method
        """
        var = np.percentile(self.returns, (1 - confidence_level) * 100)
        self.risk_metrics[f'VAR_{confidence_level}'] = var
        
        return var
    
    def calculate_cvar(self, confidence_level=0.95):
        """
        Conditional Value at Risk / Expected Shortfall
        Average of returns worse than VAR
        
        More comprehensive risk measure than VAR
        """
        var = self.calculate_var(confidence_level)
        cvar = self.returns[self.returns <= var].mean()
        
        self.risk_metrics[f'CVaR_{confidence_level}'] = cvar
        
        return cvar
    
    def calculate_sharpe_ratio(self):
        """
        Sharpe Ratio
        Sharpe = (Average Return - Risk-Free Rate) / Standard Deviation
        
        Measures risk-adjusted return
        """
        avg_return = self.returns.mean() * 252  # Annualized
        std_dev = self.returns.std() * np.sqrt(252)
        
        sharpe = (avg_return - self.risk_free_rate) / std_dev if std_dev != 0 else 0
        self.risk_metrics['Sharpe Ratio'] = sharpe
        
        return sharpe
    
    def calculate_sortino_ratio(self, target_return=0):
        """
        Sortino Ratio
        Sortino = (Average Return - Target) / Downside Deviation
        
        Only penalizes downside volatility
        """
        avg_return = self.returns.mean() * 252
        downside_returns = self.returns[self.returns < target_return]
        downside_std = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        
        sortino = (avg_return - target_return) / downside_std if downside_std != 0 else 0
        self.risk_metrics['Sortino Ratio'] = sortino
        
        return sortino
    
    def calculate_maximum_drawdown(self):
        """
        Maximum Drawdown
        Maximum peak-to-trough decline
        
        Key measure of downside risk
        """
        cumulative = (1 + self.returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        self.risk_metrics['Max Drawdown'] = max_drawdown
        
        return max_drawdown
    
    def calculate_beta(self):
        """
        Beta Coefficient
        Measures systematic risk relative to market
        
        Beta > 1: More volatile than market
        Beta = 1: Moves with market
        Beta < 1: Less volatile than market
        """
        if self.market_returns is None:
            return None
        
        covariance = np.cov(self.returns, self.market_returns)[0, 1]
        market_variance = np.var(self.market_returns)
        
        beta = covariance / market_variance if market_variance != 0 else 0
        self.risk_metrics['Beta'] = beta
        
        return beta
    
    def calculate_volatility(self):
        """
        Annualized Volatility
        Standard deviation of returns
        """
        volatility = self.returns.std() * np.sqrt(252)
        self.risk_metrics['Volatility'] = volatility
        
        return volatility
    
    def calculate_all_risk_metrics(self):
        """Calculate all risk metrics"""
        self.calculate_volatility()
        self.calculate_sharpe_ratio()
        self.calculate_sortino_ratio()
        self.calculate_maximum_drawdown()
        self.calculate_var(0.95)
        self.calculate_cvar(0.95)
        
        if self.market_returns is not None:
            self.calculate_beta()
        
        return self.risk_metrics

# ============================================================================
# 3. SECTOR RELATIVE VALUATION
# ============================================================================

class SectorValuationAnalysis:
    """
    Sector-wise Relative Valuation Comparison
    
    Identifies:
    - Best valued sectors
    - Sector momentum
    - Relative attractiveness
    """
    
    def __init__(self, sector_stocks_data):
        """
        sector_stocks_data: dict with sector name as key,
        list of stock dictionaries as value
        """
        self.sector_data = sector_stocks_data
        self.sector_metrics = {}
    
    def calculate_sector_metrics(self):
        """Calculate aggregate metrics for each sector"""
        for sector, stocks in self.sector_data.items():
            if len(stocks) == 0:
                continue
            
            metrics_df = pd.DataFrame(stocks)
            
            sector_metrics = {
                'Sector': sector,
                'Stock Count': len(stocks),
                'Avg P/E': metrics_df['P/E'].mean(),
                'Median P/E': metrics_df['P/E'].median(),
                'Avg P/B': metrics_df['P/B'].mean(),
                'Avg P/S': metrics_df['P/S'].mean(),
                'Avg EV/EBITDA': metrics_df['EV/EBITDA'].mean(),
                'Avg Div Yield %': metrics_df['Dividend Yield %'].mean(),
                'Total Market Cap': metrics_df['Market Cap'].sum(),
            }
            
            self.sector_metrics[sector] = sector_metrics
        
        return pd.DataFrame(list(self.sector_metrics.values()))
    
    def rank_sectors_by_valuation(self):
        """Rank sectors from most to least attractive"""
        sector_df = self.calculate_sector_metrics()
        
        # Create scoring system
        sector_df['PE_Score'] = 100 / (sector_df['Avg P/E'] / sector_df['Avg P/E'].mean())
        sector_df['PB_Score'] = 100 / (sector_df['Avg P/B'] / sector_df['Avg P/B'].mean())
        
        sector_df['Valuation_Score'] = (sector_df['PE_Score'] + sector_df['PB_Score']) / 2
        sector_df = sector_df.sort_values('Valuation_Score', ascending=False)
        
        return sector_df[['Sector', 'Stock Count', 'Avg P/E', 'Avg P/B', 'Avg Div Yield %', 'Valuation_Score']]

# ============================================================================
# 4. FINANCIAL LEVERAGE & SOLVENCY ANALYSIS
# ============================================================================

class FinancialHealthAnalysis:
    """
    Financial health and leverage metrics
    
    Measures:
    - Debt-to-Equity Ratio
    - Interest Coverage Ratio
    - Current Ratio
    - Quick Ratio
    - Cash Flow Analysis
    """
    
    def __init__(self, financial_data):
        """
        financial_data: dict with keys:
        - total_debt
        - equity
        - ebit
        - interest_expense
        - current_assets
        - current_liabilities
        - quick_assets
        - operating_cash_flow
        - net_income
        """
        self.data = financial_data
        self.health_metrics = {}
    
    def calculate_debt_to_equity(self):
        """
        Debt-to-Equity Ratio = Total Debt / Equity
        
        Higher ratio = Higher financial risk
        Typical healthy range: 0.5-2.0 depending on industry
        """
        if self.data.get('equity', 0) == 0:
            return None
        
        de_ratio = self.data.get('total_debt', 0) / self.data['equity']
        self.health_metrics['D/E Ratio'] = de_ratio
        
        return de_ratio
    
    def calculate_interest_coverage(self):
        """
        Interest Coverage Ratio = EBIT / Interest Expense
        
        Higher ratio = Better ability to service debt
        Minimum healthy level: > 2.5
        """
        if self.data.get('interest_expense', 0) == 0:
            return None
        
        ic_ratio = self.data.get('ebit', 0) / self.data['interest_expense']
        self.health_metrics['Interest Coverage'] = ic_ratio
        
        return ic_ratio
    
    def calculate_current_ratio(self):
        """
        Current Ratio = Current Assets / Current Liabilities
        
        Measures short-term liquidity
        Healthy range: 1.5-3.0
        """
        if self.data.get('current_liabilities', 0) == 0:
            return None
        
        cr = self.data.get('current_assets', 0) / self.data['current_liabilities']
        self.health_metrics['Current Ratio'] = cr
        
        return cr
    
    def calculate_quick_ratio(self):
        """
        Quick Ratio = (Current Assets - Inventory) / Current Liabilities
        
        More conservative liquidity measure
        Healthy range: 1.0-1.5
        """
        if self.data.get('current_liabilities', 0) == 0:
            return None
        
        qr = self.data.get('quick_assets', 0) / self.data['current_liabilities']
        self.health_metrics['Quick Ratio'] = qr
        
        return qr
    
    def calculate_financial_health_score(self):
        """Generate overall financial health score (0-100)"""
        score = 50  # Neutral starting point
        
        de = self.health_metrics.get('D/E Ratio')
        if de and de < 1:
            score += 15
        elif de and de > 2:
            score -= 15
        
        ic = self.health_metrics.get('Interest Coverage')
        if ic and ic > 5:
            score += 15
        elif ic and ic < 2:
            score -= 15
        
        cr = self.health_metrics.get('Current Ratio')
        if cr and 1.5 < cr < 3:
            score += 10
        elif cr and cr < 1:
            score -= 10
        
        return np.clip(score, 0, 100)

# ============================================================================
# 5. PORTFOLIO ANALYSIS
# ============================================================================

class PortfolioAnalysis:
    """
    Portfolio-level valuation and risk analysis
    """
    
    def __init__(self, holdings, weights):
        """
        holdings: list of stock data dictionaries
        weights: list of portfolio weights (must sum to 1)
        """
        self.holdings = holdings
        self.weights = np.array(weights)
        
        if abs(self.weights.sum() - 1.0) > 0.001:
            self.weights = self.weights / self.weights.sum()
        
        self.portfolio_metrics = {}
    
    def calculate_portfolio_pe(self):
        """Weighted average P/E ratio"""
        pe_values = [h.get('P/E', 0) for h in self.holdings]
        portfolio_pe = np.average(pe_values, weights=self.weights)
        
        self.portfolio_metrics['Portfolio P/E'] = portfolio_pe
        return portfolio_pe
    
    def calculate_portfolio_pb(self):
        """Weighted average P/B ratio"""
        pb_values = [h.get('P/B', 0) for h in self.holdings]
        portfolio_pb = np.average(pb_values, weights=self.weights)
        
        self.portfolio_metrics['Portfolio P/B'] = portfolio_pb
        return portfolio_pb
    
    def calculate_portfolio_dividend_yield(self):
        """Weighted average dividend yield"""
        div_yields = [h.get('Dividend Yield %', 0) for h in self.holdings]
        portfolio_div = np.average(div_yields, weights=self.weights)
        
        self.portfolio_metrics['Portfolio Div Yield %'] = portfolio_div
        return portfolio_div
    
    def calculate_all_portfolio_metrics(self):
        """Calculate all portfolio metrics"""
        self.calculate_portfolio_pe()
        self.calculate_portfolio_pb()
        self.calculate_portfolio_dividend_yield()
        
        return self.portfolio_metrics

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def compare_multiples(stock_multiple, sector_avg, industry_avg=None):
    """
    Compare stock multiple to benchmarks
    
    Returns:
    - Relative valuation to sector
    - Signal: Undervalued, Fair, Overvalued
    """
    relative_to_sector = (stock_multiple / sector_avg - 1) * 100
    
    if relative_to_sector < -15:
        signal = "Significantly Undervalued"
    elif relative_to_sector < -5:
        signal = "Moderately Undervalued"
    elif relative_to_sector < 5:
        signal = "Fair Valued"
    elif relative_to_sector < 15:
        signal = "Moderately Overvalued"
    else:
        signal = "Significantly Overvalued"
    
    return {
        'Relative to Sector %': relative_to_sector,
        'Signal': signal
    }

def generate_valuation_report(stock_name, valuation_metrics, health_metrics):
    """Generate comprehensive valuation report"""
    report = f"""
    ================================================================================
    RELATIVE VALUATION REPORT: {stock_name}
    ================================================================================
    
    VALUATION MULTIPLES:
    - P/E Ratio: {valuation_metrics.get('P/E', 'N/A'):.2f}
    - P/B Ratio: {valuation_metrics.get('P/B', 'N/A'):.2f}
    - P/S Ratio: {valuation_metrics.get('P/S', 'N/A'):.2f}
    - EV/EBITDA: {valuation_metrics.get('EV/EBITDA', 'N/A'):.2f}
    - PEG Ratio: {valuation_metrics.get('PEG', 'N/A'):.2f}
    - Dividend Yield: {valuation_metrics.get('Dividend Yield %', 'N/A'):.2f}%
    
    FINANCIAL HEALTH:
    - Debt-to-Equity: {health_metrics.get('D/E Ratio', 'N/A'):.2f}
    - Interest Coverage: {health_metrics.get('Interest Coverage', 'N/A'):.2f}x
    - Current Ratio: {health_metrics.get('Current Ratio', 'N/A'):.2f}
    - Quick Ratio: {health_metrics.get('Quick Ratio', 'N/A'):.2f}
    ================================================================================
    """
    
    return report

# Example usage
if __name__ == "__main__":
    
    # Sample company data
    company_data = {
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
    
    # Calculate relative valuation
    val_model = RelativeValuation(company_data)
    metrics = val_model.calculate_all_metrics()
    
    print("Valuation Metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.2f}")
    
    print(f"\nValuation Score: {val_model.get_valuation_score():.0f}/100")
