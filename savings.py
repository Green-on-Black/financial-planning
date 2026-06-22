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

# Crunch zee numbers <_<
f_tax = fed_bracket + ny_state_tax + nyc_local_tax + niit_surtax
m_tax = ny_state_tax + nyc_local_tax

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

fsnxx_pre = pv * 0.0254
fsnxx_post = fsnxx_pre

tbill_pre = pv * 0.0364                                  # 8-wk yield
tbill_post = tbill_pre * (1 - fed_bracket)

print(f"\nFZDXX: Pre-tax={fzdxx_pre:.2f}, Post-tax={fzdxx_post:.2f}")
print(f"FZCXX:  Pre-tax={fzcxx_pre:.2f}, Post-tax={fzcxx_post:.2f}")
print(f"FZEXX:  Pre-tax={fzexx_pre:.2f}, Post-tax={fzexx_post:.2f}")
print(f"FSNXX:  Pre-tax={fsnxx_pre:.2f}, Post-tax={fsnxx_post:.2f}")
print(f"T-Bill: Pre-tax={tbill_pre:.2f}, Post-tax={tbill_post:.2f}")

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

# Test with your client's current setup
calculate_switching_funds(
    muni_yield=0.0254,  # FSNXX at 2.54%
    fed=0.24,           # 24% Federal Bracket
    niit=0.038,         # 3.8% NIIT Surtax
    state=0.0685,       # 6.85% NY State Tax
    local=0.0388        # 3.88% NYC Local Tax
)
