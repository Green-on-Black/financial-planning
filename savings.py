import yfinance as yf

# Present value of the investment
# In the future, I want to change this to be a variable passed from 
# the user during runtime
pv = 100000

# Taxes. What everybody loves /s
fed_bracket =   0.24
ny_state_tax =  0.0685
nyc_local_tax = 0.0388
# Net Investment Income Tax (NIIT) is an additional tax of 3.8% that 
# applies to high earners making over $200K for single filers or 
# $250K for married couples filing jointly).
# Zero this out if this doesn't apply to you.
niit_surtax =   0.038

# Calculate the tax burden. Boo hoo, no fun!
f_tax = fed_bracket + ny_state_tax + nyc_local_tax + niit_surtax
m_tax = ny_state_tax + nyc_local_tax

# Get the yields for ETFs from Yahoo! Finance (via yfinance)
def get_etf_yield(ticker_symbol):
    """
    Gets the yields for ETFs using yfinance.
    Returns the yield as a decimal (e.g., 0.0336 for 3.36%).
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Yahoo is annoying and sometimes stores ETF yields in 
        # 'yield' or 'dividendYield'. To figure this out, check both 
        # keys and return the first one that exists.
        fund_yield = info.get('yield') or info.get('dividendYield')
        
        if fund_yield is not None:
            return fund_yield
        else:
            print(f"Could not find the yield for {ticker_symbol}. Defaulting to 0.")
            return 0.0
            
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return 0.0

# Fetch yields dynamically!
nyf_yield_live = get_etf_yield("NYF")
fmny_yield_live = get_etf_yield("FMNY")

# This is where the magic happens!
# For each fund, calculate the pre-tax return based on the present 
# yield. This is the `_pre` variable. Then, calculate the post-tax
# return based on the pre-tax return and the applicable tax rate.
# Note: Not all funds are subject to the same tax rate. For example,
# FSNXX is a triple tax-exempt municipal money market fund, so it is 
# not subject to federal, state, or local taxes. Therefore, its 
# post-tax return is equal to its pre-tax return.
# Like the present value, I'll one day get around to making this a 
# variable passed during runtime
fzdxx_pre = pv * 0.0347
fzdxx_post = fzdxx_pre * (1 - f_tax)

fzcxx_pre = pv * 0.0339
fzcxx_post = fzcxx_pre * (1 - f_tax)

fzexx_pre = pv * 0.0254
fzexx_post = fzexx_pre * (1 - m_tax)

fsnxx_yield = 0.0254
fsnxx_pre = pv * fsnxx_yield
fsnxx_post = fsnxx_pre

tbill_pre = pv * 0.0364                                  # 8-wk yield
tbill_post = tbill_pre * (1 - fed_bracket)

nyf_pre = pv * nyf_yield_live
nyf_post = nyf_pre

fmny_pre = pv * fmny_yield_live
fmny_post = fmny_pre

print(f"SYMBOL    FUND CATEGORY           30-DAY YIELD   PRE-TAX        POST-TAX")
print(f"==========================================================================")
print(f"FMNY      Muni New York Long ETF  {fmny_yield_live*100:.2f} %         $ {fmny_pre:,.2f}     $ {fmny_post:,.2f}")
print(f"NYF       Muni New York Long ETF  {nyf_yield_live*100:.2f} %         $ {nyf_pre:,.2f}     $ {nyf_post:,.2f}")
print(f"T-Bill    Treasury Bills                         $ {tbill_pre:,.2f}     $ {tbill_post:,.2f}")
print(f"FSNXX     Money Market-Tax-Free                  $ {fsnxx_pre:,.2f}     $ {fsnxx_post:,.2f}")
print(f"FZEXX     Money Market-Taxable                   $ {fzexx_pre:,.2f}     $ {fzexx_post:,.2f}")
print(f"FZDXX     Prime Money Market                     $ {fzdxx_pre:,.2f}     $ {fzdxx_post:,.2f}")
print(f"FZCXX     Money Market-Taxable                   $ {fzcxx_pre:,.2f}     $ {fzcxx_post:,.2f}")

# This is how we can determine when it makes sense to switch from a 
# triple tax-exempt municipal money market to one that is taxable.
def calculate_switching_funds(muni_yield, fed, niit, state, local):
    """
    Calculate the *exact* yield required for other funds to beat
    a triple tax-exempt municipal money market fund.
    """
    f_tax = fed + niit + state + local
    m_tax = state + local
    
    # Calculate the breakeven points
    taxable_threshold = muni_yield / (1 - f_tax)
    national_muni_threshold = muni_yield / (1 - m_tax)
    
    print(f"\n------------ WHEN TO SWITCH ------------")
    print(f"CURRENT TARGET ................................................................................. {muni_yield*100:.2f}% Post-tax")
    print(f"To beat a NYS/NYC Municipal money market, a Fully Taxable fund must yield MORE than: ........... {taxable_threshold*100:.2f}%")
    print(f"To beat a National/out-of-state municipal fund, a NYS/NYC Taxable fund must yield MORE than: ... {national_muni_threshold*100:.2f}%")

# Crunch zee numbers! again! ^_^
calculate_switching_funds(
    muni_yield  =   fsnxx_yield,
    fed         =   fed_bracket,
    niit        =   niit_surtax,
    state       =   ny_state_tax,
    local       =   nyc_local_tax
)
