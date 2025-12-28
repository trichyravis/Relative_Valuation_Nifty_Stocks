"""
COMPARABLE MULTIPLES INTEGRATION
Code to add relative valuation to Single Stock Analysis
Add this to your nifty_valuation_model.py in the Single Stock Analysis section
"""

# Add this to the imports at the top of nifty_valuation_model.py:
# from comparable_multiples import get_sector_multiples, calculate_implied_valuation, get_valuation_summary

# Then add this code after the Price Chart section (around line 560):

st.markdown("---")
st.markdown("### 💰 RELATIVE VALUATION USING COMPARABLE MULTIPLES")

st.markdown("""
**How it works:** This section uses valuation multiples from comparable companies in the same sector 
to calculate an implied valuation for the selected company.
""")

# Get sector for the selected stock
sector = NIFTY_50_DATA[selected_ticker]['Sector']
sector_multiples = get_sector_multiples(sector)

if sector_multiples:
    # Prepare financials dictionary
    company_financials = {
        'market_cap': info.get('marketCap', 0) / 10000000,  # Convert to crores
        'net_income': metrics.get('Net Income (Implied)', 0) if 'Net Income (Implied)' in metrics else (
            metrics.get('Current Price', 0) * info.get('sharesOutstanding', 0) / 100  # Rough estimate
        ),
        'book_value': info.get('bookValue', 0) * info.get('sharesOutstanding', 0) / 10000000 if info.get('bookValue') else None,
        'revenue': (info.get('marketCap', 0) / 10000000) / metrics.get('P/S Ratio', 1) if metrics.get('P/S Ratio') else 0,
        'ebitda': (info.get('marketCap', 0) / 10000000) / metrics.get('EV/EBITDA', 1) if metrics.get('EV/EBITDA') else 0,
        'shares_outstanding': info.get('sharesOutstanding', 0) / 10000000,
        'share_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
        'net_debt': info.get('totalDebt', 0) - info.get('totalCash', 0)
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
                    col1, col2, col3, col4 = st.columns(4)
                    
                    for idx, (method, result) in enumerate(pe_results.items()):
                        with [col1, col2, col3, col4][idx]:
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
                    
                    # Detailed comparison
                    col_pe1, col_pe2 = st.columns(2)
                    
                    with col_pe1:
                        st.markdown("**Sector P/E Range**")
                        pe_range = sector_multiples['multiples']['P/E']
                        st.write(f"High: {pe_range['high']:.2f}x")
                        st.write(f"Average: {pe_range['avg']:.2f}x")
                        st.write(f"Median: {pe_range['median']:.2f}x")
                        st.write(f"Low: {pe_range['low']:.2f}x")
                    
                    with col_pe2:
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
                    col1, col2, col3, col4 = st.columns(4)
                    
                    for idx, (method, result) in enumerate(pb_results.items()):
                        with [col1, col2, col3, col4][idx]:
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
                    
                    col_pb1, col_pb2 = st.columns(2)
                    
                    with col_pb1:
                        st.markdown("**Sector P/B Range**")
                        pb_range = sector_multiples['multiples']['P/B']
                        st.write(f"High: {pb_range['high']:.2f}x")
                        st.write(f"Average: {pb_range['avg']:.2f}x")
                        st.write(f"Median: {pb_range['median']:.2f}x")
                        st.write(f"Low: {pb_range['low']:.2f}x")
                    
                    with col_pb2:
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
            
            if company_financials['revenue'] and company_financials['revenue'] > 0:
                ps_results = calculate_implied_valuation(
                    company_financials, 
                    sector_multiples['multiples'], 
                    'P/S'
                )
                
                if ps_results:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    for idx, (method, result) in enumerate(ps_results.items()):
                        with [col1, col2, col3, col4][idx]:
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
                    
                    col_ps1, col_ps2 = st.columns(2)
                    
                    with col_ps1:
                        st.markdown("**Sector P/S Range**")
                        ps_range = sector_multiples['multiples']['P/S']
                        st.write(f"High: {ps_range['high']:.2f}x")
                        st.write(f"Average: {ps_range['avg']:.2f}x")
                        st.write(f"Median: {ps_range['median']:.2f}x")
                        st.write(f"Low: {ps_range['low']:.2f}x")
                    
                    with col_ps2:
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
            
            if company_financials['ebitda'] and company_financials['ebitda'] > 0:
                ev_results = calculate_implied_valuation(
                    company_financials, 
                    sector_multiples['multiples'], 
                    'EV/EBITDA'
                )
                
                if ev_results:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    for idx, (method, result) in enumerate(ev_results.items()):
                        with [col1, col2, col3, col4][idx]:
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
                    
                    col_ev1, col_ev2 = st.columns(2)
                    
                    with col_ev1:
                        st.markdown("**Sector EV/EBITDA Range**")
                        ev_range = sector_multiples['multiples']['EV/EBITDA']
                        st.write(f"High: {ev_range['high']:.2f}x")
                        st.write(f"Average: {ev_range['avg']:.2f}x")
                        st.write(f"Median: {ev_range['median']:.2f}x")
                        st.write(f"Low: {ev_range['low']:.2f}x")
                    
                    with col_ev2:
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
