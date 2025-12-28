
"""
COMPARABLE COMPANY MULTIPLES DATABASE
Sector-wise valuation multiples for relative valuation
Prof. V. Ravichandran | The Mountain Path - World of Finance

Format: Average multiples from comparable companies in each sector
Used to calculate implied valuation for target companies
"""

import pandas as pd
import numpy as np

# Sector-wise Comparable Company Multiples (Recent Market Data)
SECTOR_MULTIPLES = {
    'IT & Software': {
        'companies': ['TCS', 'Infosys', 'Wipro', 'HCL Tech', 'Tech Mahindra', 'LT Tech'],
        'multiples': {
            'P/E': {'avg': 24.5, 'median': 23.8, 'high': 28.2, 'low': 20.1},
            'P/B': {'avg': 5.2, 'median': 4.8, 'high': 6.5, 'low': 3.8},
            'P/S': {'avg': 4.1, 'median': 3.9, 'high': 5.2, 'low': 2.9},
            'EV/EBITDA': {'avg': 18.5, 'median': 17.9, 'high': 21.2, 'low': 15.3}
        }
    },
    
    'Financial Services': {
        'companies': ['HDFC Bank', 'ICICI Bank', 'Axis Bank', 'IndusInd Bank', 'SBI', 'Bajaj Finserv'],
        'multiples': {
            'P/E': {'avg': 18.2, 'median': 17.5, 'high': 21.8, 'low': 14.2},
            'P/B': {'avg': 2.1, 'median': 2.0, 'high': 2.8, 'low': 1.4},
            'P/S': {'avg': 3.2, 'median': 3.0, 'high': 4.1, 'low': 2.1},
            'EV/EBITDA': {'avg': 12.5, 'median': 12.0, 'high': 15.2, 'low': 9.8}
        }
    },
    
    'Consumer & FMCG': {
        'companies': ['Hindustan Unilever', 'Titan', 'Nestle', 'Asian Paints', 'Marico'],
        'multiples': {
            'P/E': {'avg': 41.2, 'median': 39.5, 'high': 48.3, 'low': 35.1},
            'P/B': {'avg': 11.5, 'median': 10.8, 'high': 13.2, 'low': 8.9},
            'P/S': {'avg': 7.8, 'median': 7.2, 'high': 9.5, 'low': 6.1},
            'EV/EBITDA': {'avg': 32.1, 'median': 30.5, 'high': 38.2, 'low': 25.3}
        }
    },
    
    'Pharmaceuticals': {
        'companies': ['Sun Pharma', 'Cipla', 'Dr Reddy', 'Lupin', 'Divi Lab', 'Biocon'],
        'multiples': {
            'P/E': {'avg': 28.3, 'median': 27.1, 'high': 32.5, 'low': 22.8},
            'P/B': {'avg': 4.2, 'median': 3.9, 'high': 5.3, 'low': 3.1},
            'P/S': {'avg': 3.9, 'median': 3.6, 'high': 4.8, 'low': 2.9},
            'EV/EBITDA': {'avg': 21.2, 'median': 20.3, 'high': 25.1, 'low': 17.2}
        }
    },
    
    'Energy & Utilities': {
        'companies': ['Reliance', 'NTPC', 'ONGC', 'Power Grid', 'IOCL', 'GAIL'],
        'multiples': {
            'P/E': {'avg': 12.5, 'median': 11.8, 'high': 15.2, 'low': 9.3},
            'P/B': {'avg': 1.3, 'median': 1.2, 'high': 1.7, 'low': 0.9},
            'P/S': {'avg': 0.8, 'median': 0.7, 'high': 1.1, 'low': 0.5},
            'EV/EBITDA': {'avg': 8.5, 'median': 8.1, 'high': 10.2, 'low': 6.8}
        }
    },
    
    'Automobiles': {
        'companies': ['Maruti Suzuki', 'Hero MotoCorp', 'Bajaj Auto', 'Mahindra & Mahindra', 'Bosch India'],
        'multiples': {
            'P/E': {'avg': 15.8, 'median': 15.2, 'high': 18.5, 'low': 12.3},
            'P/B': {'avg': 2.3, 'median': 2.1, 'high': 2.9, 'low': 1.6},
            'P/S': {'avg': 1.2, 'median': 1.1, 'high': 1.5, 'low': 0.8},
            'EV/EBITDA': {'avg': 7.8, 'median': 7.4, 'high': 9.5, 'low': 5.9}
        }
    },
    
    'Metals & Mining': {
        'companies': ['Tata Steel', 'JSW Steel', 'Coal India'],
        'multiples': {
            'P/E': {'avg': 8.2, 'median': 7.9, 'high': 10.1, 'low': 6.2},
            'P/B': {'avg': 0.9, 'median': 0.85, 'high': 1.2, 'low': 0.6},
            'P/S': {'avg': 0.6, 'median': 0.55, 'high': 0.8, 'low': 0.4},
            'EV/EBITDA': {'avg': 6.1, 'median': 5.8, 'high': 7.8, 'low': 4.5}
        }
    },
    
    'Infrastructure & Construction': {
        'companies': ['Larsen & Toubro', 'Adani Ports'],
        'multiples': {
            'P/E': {'avg': 20.5, 'median': 19.8, 'high': 23.2, 'low': 17.1},
            'P/B': {'avg': 2.5, 'median': 2.3, 'high': 3.1, 'low': 1.8},
            'P/S': {'avg': 1.8, 'median': 1.7, 'high': 2.2, 'low': 1.3},
            'EV/EBITDA': {'avg': 11.2, 'median': 10.8, 'high': 13.5, 'low': 8.9}
        }
    },
    
    'Construction & Materials': {
        'companies': ['UltraCem Co'],
        'multiples': {
            'P/E': {'avg': 35.2, 'median': 33.8, 'high': 39.1, 'low': 30.2},
            'P/B': {'avg': 8.5, 'median': 8.1, 'high': 10.2, 'low': 6.8},
            'P/S': {'avg': 6.2, 'median': 5.9, 'high': 7.5, 'low': 4.8},
            'EV/EBITDA': {'avg': 28.3, 'median': 27.1, 'high': 32.5, 'low': 23.8}
        }
    },
    
    'Telecom': {
        'companies': ['Bharti Airtel'],
        'multiples': {
            'P/E': {'avg': 22.3, 'median': 21.5, 'high': 25.8, 'low': 18.2},
            'P/B': {'avg': 3.2, 'median': 3.0, 'high': 3.9, 'low': 2.4},
            'P/S': {'avg': 2.1, 'median': 2.0, 'high': 2.6, 'low': 1.5},
            'EV/EBITDA': {'avg': 14.5, 'median': 13.9, 'high': 17.2, 'low': 11.3}
        }
    },
    
    'Healthcare': {
        'companies': ['Apollo Hospitals'],
        'multiples': {
            'P/E': {'avg': 38.5, 'median': 37.2, 'high': 42.3, 'low': 34.1},
            'P/B': {'avg': 5.8, 'median': 5.5, 'high': 6.8, 'low': 4.7},
            'P/S': {'avg': 4.5, 'median': 4.2, 'high': 5.3, 'low': 3.6},
            'EV/EBITDA': {'avg': 24.2, 'median': 23.1, 'high': 28.5, 'low': 19.8}
        }
    },
    
    'Holding Companies': {
        'companies': ['Bajaj Holdings'],
        'multiples': {
            'P/E': {'avg': 16.2, 'median': 15.5, 'high': 19.1, 'low': 13.2},
            'P/B': {'avg': 1.8, 'median': 1.7, 'high': 2.3, 'low': 1.3},
            'P/S': {'avg': 1.4, 'median': 1.3, 'high': 1.8, 'low': 1.0},
            'EV/EBITDA': {'avg': 10.5, 'median': 10.1, 'high': 12.8, 'low': 8.2}
        }
    }
}


def get_sector_multiples(sector: str) -> dict:
    """Get multiples for a specific sector"""
    return SECTOR_MULTIPLES.get(sector, {})


def calculate_implied_valuation(financials: dict, multiples: dict, multiple_type: str) -> dict:
    """
    Calculate implied valuation using comparable multiples
    
    Parameters:
    -----------
    financials : dict
        Target company financials {
            'market_cap': float (in crores),
            'net_income': float (in crores),
            'book_value': float (in crores),
            'revenue': float (in crores),
            'ebitda': float (in crores),
            'shares_outstanding': float (in millions),
            'share_price': float (in rupees)
        }
    
    multiples : dict
        Sector multiples with avg, median, high, low
    
    multiple_type : str
        'P/E', 'P/B', 'P/S', or 'EV/EBITDA'
    
    Returns:
    --------
    dict : Valuation results
    """
    
    results = {}
    
    # Convert shares from millions to actual number for calculation
    shares_outstanding = financials.get('shares_outstanding', 1) * 10  # millions to crore equivalent
    if shares_outstanding == 0:
        shares_outstanding = 1
    
    if multiple_type == 'P/E' and financials.get('net_income', 0) > 0:
        # P/E = Market Cap / Net Income
        # Implied Market Cap = P/E × Net Income
        # Implied Price = (Implied Market Cap / Shares Outstanding) × 10 (convert crore to rupee value)
        
        net_income = financials.get('net_income', 0.1)
        if net_income <= 0:
            net_income = 0.1
        
        current_pe = financials['market_cap'] / net_income if net_income > 0 else 0
        
        for method in ['avg', 'median', 'high', 'low']:
            multiple = multiples['P/E'].get(method)
            if multiple and multiple > 0:
                implied_market_cap = multiple * net_income
                # Implied Price per Share = Market Cap (in crores) / Shares (in millions) × 10
                implied_price = (implied_market_cap / (financials.get('shares_outstanding', 1) + 0.01)) * 10
                
                if implied_price > 0 and financials['share_price'] > 0:
                    upside = ((implied_price - financials['share_price']) / financials['share_price']) * 100
                else:
                    upside = 0
                
                results[method] = {
                    'multiple': multiple,
                    'implied_market_cap': implied_market_cap,
                    'implied_price': implied_price,
                    'current_price': financials['share_price'],
                    'upside_downside': upside,
                    'current_multiple': current_pe
                }
    
    elif multiple_type == 'P/B' and financials.get('book_value', 0) > 0:
        # P/B = Market Cap / Book Value
        # Implied Market Cap = P/B × Book Value
        # Implied Price = (Implied Market Cap / Shares Outstanding) × 10
        
        book_value = financials.get('book_value', 0.1)
        if book_value <= 0:
            book_value = 0.1
        
        current_pb = financials['market_cap'] / book_value if book_value > 0 else 0
        
        for method in ['avg', 'median', 'high', 'low']:
            multiple = multiples['P/B'].get(method)
            if multiple and multiple > 0:
                implied_market_cap = multiple * book_value
                implied_price = (implied_market_cap / (financials.get('shares_outstanding', 1) + 0.01)) * 10
                
                if implied_price > 0 and financials['share_price'] > 0:
                    upside = ((implied_price - financials['share_price']) / financials['share_price']) * 100
                else:
                    upside = 0
                
                results[method] = {
                    'multiple': multiple,
                    'implied_market_cap': implied_market_cap,
                    'implied_price': implied_price,
                    'current_price': financials['share_price'],
                    'upside_downside': upside,
                    'current_multiple': current_pb
                }
    
    elif multiple_type == 'P/S' and financials.get('revenue', 0) > 0:
        # P/S = Market Cap / Revenue
        # Implied Market Cap = P/S × Revenue
        # Implied Price = (Implied Market Cap / Shares Outstanding) × 10
        
        revenue = financials.get('revenue', 0.1)
        if revenue <= 0:
            revenue = 0.1
        
        current_ps = financials['market_cap'] / revenue if revenue > 0 else 0
        
        for method in ['avg', 'median', 'high', 'low']:
            multiple = multiples['P/S'].get(method)
            if multiple and multiple > 0:
                implied_market_cap = multiple * revenue
                implied_price = (implied_market_cap / (financials.get('shares_outstanding', 1) + 0.01)) * 10
                
                if implied_price > 0 and financials['share_price'] > 0:
                    upside = ((implied_price - financials['share_price']) / financials['share_price']) * 100
                else:
                    upside = 0
                
                results[method] = {
                    'multiple': multiple,
                    'implied_market_cap': implied_market_cap,
                    'implied_price': implied_price,
                    'current_price': financials['share_price'],
                    'upside_downside': upside,
                    'current_multiple': current_ps
                }
    
    elif multiple_type == 'EV/EBITDA' and financials.get('ebitda', 0) > 0:
        # EV = EV/EBITDA × EBITDA
        # Market Cap = EV - Net Debt
        # Implied Price = (Implied Market Cap / Shares Outstanding) × 10
        
        ebitda = financials.get('ebitda', 0.1)
        if ebitda <= 0:
            ebitda = 0.1
        
        net_debt = financials.get('net_debt', 0)
        current_ev = (financials['market_cap'] + net_debt) / ebitda if ebitda > 0 else 0
        
        for method in ['avg', 'median', 'high', 'low']:
            multiple = multiples['EV/EBITDA'].get(method)
            if multiple and multiple > 0:
                implied_ev = multiple * ebitda
                implied_market_cap = implied_ev - net_debt
                
                if implied_market_cap <= 0:
                    implied_market_cap = multiple * ebitda  # Use EV if MC is negative
                
                implied_price = (implied_market_cap / (financials.get('shares_outstanding', 1) + 0.01)) * 10
                
                if implied_price > 0 and financials['share_price'] > 0:
                    upside = ((implied_price - financials['share_price']) / financials['share_price']) * 100
                else:
                    upside = 0
                
                results[method] = {
                    'multiple': multiple,
                    'implied_ev': implied_ev,
                    'implied_market_cap': implied_market_cap,
                    'implied_price': implied_price,
                    'current_price': financials['share_price'],
                    'upside_downside': upside,
                    'current_multiple': current_ev
                }
    
    return results


def get_valuation_summary(financials: dict, sector: str) -> pd.DataFrame:
    """Get complete valuation summary using all multiples"""
    
    sector_multiples = get_sector_multiples(sector)
    
    if not sector_multiples:
        return pd.DataFrame()
    
    summary_data = []
    
    for multiple_type in ['P/E', 'P/B', 'P/S', 'EV/EBITDA']:
        if multiple_type in sector_multiples['multiples']:
            results = calculate_implied_valuation(financials, sector_multiples['multiples'], multiple_type)
            
            if results:
                median_result = results.get('median', {})
                
                if median_result:
                    summary_data.append({
                        'Valuation Method': multiple_type,
                        'Comparable Multiple': f"{median_result['multiple']:.2f}x",
                        'Implied Price': f"₹{median_result['implied_price']:.0f}",
                        'Current Price': f"₹{median_result['current_price']:.0f}",
                        'Upside/Downside': f"{median_result['upside_downside']:.1f}%",
                        'Status': 'Undervalued' if median_result['upside_downside'] > 5 else 
                                 ('Overvalued' if median_result['upside_downside'] < -5 else 'Fair Valued')
                    })
    
    return pd.DataFrame(summary_data)
