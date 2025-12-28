"""
ADVANCED FINANCIAL ANALYSIS EXAMPLES
THE MOUNTAIN PATH - WORLD OF FINANCE
Prof. V. Ravichandran

This script demonstrates advanced usage of the financial risk modeling module
with real-world examples and comprehensive analysis workflows.
"""

import numpy as np
import pandas as pd
from financial_risk_modeling import (
    RelativeValuation,
    FinancialRiskModel,
    SectorValuationAnalysis,
    FinancialHealthAnalysis,
    PortfolioAnalysis,
    compare_multiples,
    generate_valuation_report
)

# ============================================================================
# EXAMPLE 1: COMPREHENSIVE SINGLE STOCK VALUATION ANALYSIS
# ============================================================================

def example_single_stock_analysis():
    """
    Analyze a single stock using complete relative valuation framework
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: SINGLE STOCK RELATIVE VALUATION ANALYSIS")
    print("="*80)
    
    # Sample data for TCS (Tata Consultancy Services)
    company_data = {
        'current_price': 3500,
        'earnings_per_share': 185,
        'book_value_per_share': 850,
        'sales_per_share': 2100,
        'ebitda': 45000,  # in crores
        'revenue': 250000,  # in crores
        'market_cap': 1250000,  # in crores
        'debt': 2000,
        'cash': 150000,
        'dividends_per_share': 45,
        'earnings_growth_rate': 18  # percentage
    }
    
    # Initialize valuation model
    val_model = RelativeValuation(company_data)
    
    # Calculate all metrics
    metrics = val_model.calculate_all_metrics()
    
    # Get valuation score
    score = val_model.get_valuation_score()
    
    # Display results
    print("\nCOMPANY: TCS (Tata Consultancy Services)")
    print("SECTOR: IT & Software")
    print("\nVALUATION METRICS:")
    print("-" * 40)
    
    for metric, value in metrics.items():
        if value is not None:
            if 'Yield' in metric or 'Growth' in metric:
                print(f"  {metric:.<30} {value:>8.2f}%")
            else:
                print(f"  {metric:.<30} {value:>8.2f}")
    
    print(f"\nVALUATION SCORE (0-100): {score:.0f}")
    print("\nINTERPRETATION:")
    if score > 70:
        print("  ✓ Stock appears UNDERVALUED")
    elif score > 50:
        print("  ○ Stock appears FAIRLY VALUED")
    else:
        print("  ✗ Stock appears OVERVALUED")
    
    if val_model.risk_signals:
        print("\nVALUATION SIGNALS:")
        for signal in val_model.risk_signals:
            print(f"  ⚠ {signal}")
    
    return val_model

# ============================================================================
# EXAMPLE 2: FINANCIAL HEALTH AND RISK ASSESSMENT
# ============================================================================

def example_financial_health_analysis():
    """
    Analyze financial health, leverage, and solvency
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: FINANCIAL HEALTH AND LEVERAGE ANALYSIS")
    print("="*80)
    
    # Financial data for a hypothetical company
    financial_data = {
        'total_debt': 50000,  # in crores
        'equity': 200000,     # in crores
        'ebit': 45000,        # in crores
        'interest_expense': 2000,  # in crores
        'current_assets': 80000,   # in crores
        'current_liabilities': 45000,  # in crores
        'quick_assets': 60000,  # in crores
        'operating_cash_flow': 35000,  # in crores
        'net_income': 20000   # in crores
    }
    
    # Initialize health analysis
    health_model = FinancialHealthAnalysis(financial_data)
    
    # Calculate metrics
    de_ratio = health_model.calculate_debt_to_equity()
    ic_ratio = health_model.calculate_interest_coverage()
    cr = health_model.calculate_current_ratio()
    qr = health_model.calculate_quick_ratio()
    health_score = health_model.calculate_financial_health_score()
    
    print("\nFINANCIAL HEALTH METRICS:")
    print("-" * 40)
    print(f"  Debt-to-Equity Ratio:    {de_ratio:.2f}")
    print(f"  Interest Coverage:       {ic_ratio:.2f}x")
    print(f"  Current Ratio:           {cr:.2f}")
    print(f"  Quick Ratio:             {qr:.2f}")
    print(f"\nFINANCIAL HEALTH SCORE:  {health_score:.0f}/100")
    
    # Interpretation
    print("\nINTERPRETATION:")
    print("-" * 40)
    
    if de_ratio < 1:
        print(f"  ✓ D/E Ratio of {de_ratio:.2f} indicates LOW financial risk")
    elif de_ratio < 2:
        print(f"  ○ D/E Ratio of {de_ratio:.2f} indicates MODERATE leverage")
    else:
        print(f"  ✗ D/E Ratio of {de_ratio:.2f} indicates HIGH financial risk")
    
    if ic_ratio > 5:
        print(f"  ✓ Interest coverage of {ic_ratio:.2f}x is STRONG (can service debt easily)")
    elif ic_ratio > 2.5:
        print(f"  ○ Interest coverage of {ic_ratio:.2f}x is ADEQUATE")
    else:
        print(f"  ✗ Interest coverage of {ic_ratio:.2f}x is WEAK (debt servicing concern)")
    
    if 1.5 < cr < 3:
        print(f"  ✓ Current ratio of {cr:.2f} indicates HEALTHY short-term liquidity")
    elif cr < 1:
        print(f"  ✗ Current ratio of {cr:.2f} indicates LIQUIDITY RISK")
    
    return health_model

# ============================================================================
# EXAMPLE 3: FINANCIAL RISK MODELING & VAR ANALYSIS
# ============================================================================

def example_risk_analysis():
    """
    Calculate Value at Risk and other risk metrics
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: FINANCIAL RISK MODELING & VALUE AT RISK")
    print("="*80)
    
    # Generate sample daily returns (normal distribution)
    np.random.seed(42)
    daily_returns = np.random.normal(0.0005, 0.015, 252)  # 1 year of data
    
    # Market returns
    market_returns = np.random.normal(0.0004, 0.012, 252)
    
    # Initialize risk model
    risk_model = FinancialRiskModel(daily_returns, market_returns)
    
    # Calculate risk metrics
    var_95 = risk_model.calculate_var(0.95)
    cvar_95 = risk_model.calculate_cvar(0.95)
    sharpe = risk_model.calculate_sharpe_ratio()
    sortino = risk_model.calculate_sortino_ratio()
    max_dd = risk_model.calculate_maximum_drawdown()
    volatility = risk_model.calculate_volatility()
    beta = risk_model.calculate_beta()
    
    print("\nRISK METRICS:")
    print("-" * 40)
    print(f"  Annual Volatility:       {volatility*100:.2f}%")
    print(f"  Beta:                    {beta:.2f}")
    print(f"  Sharpe Ratio:            {sharpe:.2f}")
    print(f"  Sortino Ratio:           {sortino:.2f}")
    print(f"  Maximum Drawdown:        {max_dd*100:.2f}%")
    print(f"\n  Value at Risk (95%):     {var_95*100:.2f}%")
    print(f"  Conditional VaR (95%):   {cvar_95*100:.2f}%")
    
    print("\nINTERPRETATION:")
    print("-" * 40)
    print(f"  • Daily loss exceeds {abs(var_95)*100:.2f}% only 5% of the time")
    print(f"  • On a bad day, expected loss is {abs(cvar_95)*100:.2f}%")
    print(f"  • {volatility*100:.2f}% annualized volatility indicates...")
    
    if volatility < 0.12:
        print(f"    LOW risk profile")
    elif volatility < 0.20:
        print(f"    MODERATE risk profile")
    else:
        print(f"    HIGH risk profile")
    
    if beta < 1:
        print(f"  • Beta of {beta:.2f} means stock is LESS volatile than market")
    elif beta > 1:
        print(f"  • Beta of {beta:.2f} means stock is MORE volatile than market")
    else:
        print(f"  • Beta of {beta:.2f} means stock moves WITH market")
    
    if sharpe > 1:
        print(f"  ✓ Sharpe ratio of {sharpe:.2f} indicates GOOD risk-adjusted returns")
    elif sharpe > 0.5:
        print(f"  ○ Sharpe ratio of {sharpe:.2f} indicates ACCEPTABLE returns")
    else:
        print(f"  ✗ Sharpe ratio of {sharpe:.2f} indicates POOR risk-adjusted returns")
    
    return risk_model

# ============================================================================
# EXAMPLE 4: SECTOR-WISE VALUATION COMPARISON
# ============================================================================

def example_sector_analysis():
    """
    Compare valuation metrics across sectors
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: SECTOR-WISE RELATIVE VALUATION COMPARISON")
    print("="*80)
    
    # Sample data for different sectors
    sector_data = {
        'IT & Software': [
            {'Company': 'TCS', 'P/E': 22.5, 'P/B': 3.2, 'P/S': 4.1, 'EV/EBITDA': 18, 'Dividend Yield %': 1.3, 'Market Cap': 1250000},
            {'Company': 'Infosys', 'P/E': 24.1, 'P/B': 2.8, 'P/S': 3.9, 'EV/EBITDA': 19.5, 'Dividend Yield %': 1.5, 'Market Cap': 850000},
            {'Company': 'Wipro', 'P/E': 20.3, 'P/B': 2.1, 'P/S': 2.8, 'EV/EBITDA': 15.2, 'Dividend Yield %': 2.1, 'Market Cap': 680000},
        ],
        'Financial Services': [
            {'Company': 'HDFC Bank', 'P/E': 24.0, 'P/B': 1.8, 'P/S': 5.2, 'EV/EBITDA': 12.5, 'Dividend Yield %': 1.2, 'Market Cap': 1420000},
            {'Company': 'ICICI Bank', 'P/E': 22.5, 'P/B': 1.5, 'P/S': 4.8, 'EV/EBITDA': 11.2, 'Dividend Yield %': 2.1, 'Market Cap': 980000},
            {'Company': 'Axis Bank', 'P/E': 20.8, 'P/B': 1.3, 'P/S': 4.2, 'EV/EBITDA': 9.8, 'Dividend Yield %': 2.8, 'Market Cap': 630000},
        ],
        'Energy & Utilities': [
            {'Company': 'Reliance', 'P/E': 11.2, 'P/B': 1.1, 'P/S': 0.8, 'EV/EBITDA': 7.5, 'Dividend Yield %': 4.2, 'Market Cap': 1850000},
            {'Company': 'NTPC', 'P/E': 9.5, 'P/B': 0.9, 'P/S': 0.6, 'EV/EBITDA': 6.2, 'Dividend Yield %': 5.3, 'Market Cap': 420000},
        ]
    }
    
    # Initialize sector analysis
    sector_analysis = SectorValuationAnalysis(sector_data)
    
    # Calculate metrics
    sector_metrics = sector_analysis.calculate_sector_metrics()
    ranked_sectors = sector_analysis.rank_sectors_by_valuation()
    
    print("\nSECTOR VALUATION SUMMARY:")
    print("-" * 80)
    print(ranked_sectors.to_string(index=False))
    
    print("\n\nDETAILED SECTOR ANALYSIS:")
    print("-" * 80)
    
    for sector, metrics_dict in sector_analysis.sector_metrics.items():
        print(f"\n{sector}:")
        print(f"  • Companies:             {metrics_dict['Stock Count']}")
        print(f"  • Average P/E:           {metrics_dict['Avg P/E']:.2f}")
        print(f"  • Average P/B:           {metrics_dict['Avg P/B']:.2f}")
        print(f"  • Average P/S:           {metrics_dict['Avg P/S']:.2f}")
        print(f"  • Avg Dividend Yield:    {metrics_dict['Avg Div Yield %']:.2f}%")
        print(f"  • Total Market Cap:      ₹{metrics_dict['Total Market Cap']:,.0f} Cr")
    
    return sector_analysis

# ============================================================================
# EXAMPLE 5: PORTFOLIO ANALYSIS
# ============================================================================

def example_portfolio_analysis():
    """
    Analyze portfolio-level valuation metrics
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: PORTFOLIO VALUATION ANALYSIS")
    print("="*80)
    
    # Portfolio holdings
    holdings = [
        {'Company': 'TCS', 'P/E': 22.5, 'P/B': 3.2, 'Dividend Yield %': 1.3, 'Weight': 0.25},
        {'Company': 'HDFC Bank', 'P/E': 24.0, 'P/B': 1.8, 'Dividend Yield %': 1.2, 'Weight': 0.35},
        {'Company': 'Reliance', 'P/E': 11.2, 'P/B': 1.1, 'Dividend Yield %': 4.2, 'Weight': 0.25},
        {'Company': 'Infosys', 'P/E': 24.1, 'P/B': 2.8, 'Dividend Yield %': 1.5, 'Weight': 0.15},
    ]
    
    weights = [h['Weight'] for h in holdings]
    
    # Initialize portfolio analysis
    portfolio = PortfolioAnalysis(holdings, weights)
    
    # Calculate metrics
    portfolio_metrics = portfolio.calculate_all_portfolio_metrics()
    
    print("\nPORTFOLIO COMPOSITION:")
    print("-" * 60)
    print(f"{'Stock':<20} {'Allocation':<15} {'P/E':<10} {'P/B':<10}")
    print("-" * 60)
    
    for holding in holdings:
        print(f"{holding['Company']:<20} {holding['Weight']*100:>6.1f}%{'':<8} {holding['P/E']:>6.2f}{'':<3} {holding['P/B']:>6.2f}")
    
    print("\nPORTFOLIO METRICS:")
    print("-" * 60)
    print(f"  Weighted Average P/E:    {portfolio_metrics['Portfolio P/E']:.2f}")
    print(f"  Weighted Average P/B:    {portfolio_metrics['Portfolio P/B']:.2f}")
    print(f"  Portfolio Div Yield:     {portfolio_metrics['Portfolio Div Yield %']:.2f}%")
    
    print("\nCOMPARISON TO BENCHMARKS:")
    print("-" * 60)
    print("  Market Average P/E:      ~20.5")
    print(f"  Portfolio P/E vs Market: {portfolio_metrics['Portfolio P/E']/20.5:.2f}x")
    
    return portfolio

# ============================================================================
# EXAMPLE 6: VALUATION COMPARISON AND SIGNAL GENERATION
# ============================================================================

def example_valuation_comparison():
    """
    Compare stock multiples to sector and generate signals
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: COMPARATIVE VALUATION & SIGNAL GENERATION")
    print("="*80)
    
    # Stock data
    stock_pe = 15.5
    sector_avg_pe = 22.0
    
    # Compare
    comparison = compare_multiples(stock_pe, sector_avg_pe)
    
    print("\nVALUATION COMPARISON:")
    print("-" * 40)
    print(f"  Stock P/E:               {stock_pe:.2f}")
    print(f"  Sector Average P/E:      {sector_avg_pe:.2f}")
    print(f"  Relative to Sector:      {comparison['Relative to Sector %']:.1f}%")
    print(f"  Signal:                  {comparison['Signal']}")
    
    if comparison['Relative to Sector %'] < -30:
        print("\n  ✓ STRONG BUY - Trading at significant discount to peers")
    elif comparison['Relative to Sector %'] < -10:
        print("\n  ○ BUY - Trading at discount to peers")
    elif comparison['Relative to Sector %'] < 10:
        print("\n  ○ HOLD - Trading in line with peers")
    else:
        print("\n  ✗ SELL - Trading at premium to peers")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Execute all examples
    """
    print("\n\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "THE MOUNTAIN PATH - WORLD OF FINANCE".center(78) + "║")
    print("║" + "Advanced Financial Analysis Examples".center(78) + "║")
    print("║" + "Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    # Run all examples
    val_model = example_single_stock_analysis()
    health_model = example_financial_health_analysis()
    risk_model = example_risk_analysis()
    sector_analysis = example_sector_analysis()
    portfolio = example_portfolio_analysis()
    example_valuation_comparison()
    
    print("\n" + "="*80)
    print("SUMMARY & INSIGHTS")
    print("="*80)
    
    print("""
KEY TAKEAWAYS:

1. RELATIVE VALUATION:
   - Never rely on single metric
   - Compare to peers and sector averages
   - Consider growth rates (PEG analysis)
   - Understand metric limitations

2. FINANCIAL HEALTH:
   - Assess leverage and solvency
   - Monitor interest coverage
   - Check liquidity ratios
   - Evaluate cash flow health

3. RISK ASSESSMENT:
   - Use quantitative risk metrics
   - Understand downside risk
   - Monitor volatility and beta
   - Calculate Value at Risk

4. SECTOR ANALYSIS:
   - Compare within same sector
   - Identify sector trends
   - Assess relative attractiveness
   - Monitor sector rotation

5. PORTFOLIO MANAGEMENT:
   - Use weighted average metrics
   - Diversify across sectors
   - Balance valuation and growth
   - Monitor portfolio risk

================================================================================
For more information, visit: https://www.mountainpathfinance.com
================================================================================
    """)

if __name__ == "__main__":
    main()
