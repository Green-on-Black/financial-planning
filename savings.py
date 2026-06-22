pv = 100000

# Tax Bracket Inputs for an NYC Resident
fed_bracket =   0.24
niit_surtax =   0.038
ny_state_tax =  0.0685
nyc_local_tax = 0.0388

# Combined Math Variables for the Logic Engine
f_tax = fed_bracket + niit_surtax + ny_state_tax + nyc_local_tax    # 0.3853
m_tax = ny_state_tax + nyc_local_tax                                # 0.1073

fzdxx_pre = pv * 0.0347
fzdxx_post = fzdxx_pre * (1 - f_tax)

fzcxx_pre = pv * 0.0339
fzcxx_post = fzcxx_pre * (1 - f_tax)

fzexx_pre = pv * 0.0254
fzexx_post = fzexx_pre * (1 - m_tax)

fsnxx_pre = pv * 0.0254
fsnxx_post = fsnxx_pre

tbill_pre = pv * 0.0364                                            # 8-wk yield
tbill_post = tbill_pre * (1 - fed_bracket)

print(f"FZDXX: Pre-tax={fzdxx_pre:.2f}, Post-tax={fzdxx_post:.2f}")
print(f"FZCXX: Pre-tax={fzcxx_pre:.2f}, Post-tax={fzcxx_post:.2f}")
print(f"FZEXX: Pre-tax={fzexx_pre:.2f}, Post-tax={fzexx_post:.2f}")
print(f"FSNXX: Pre-tax={fsnxx_pre:.2f}, Post-tax={fsnxx_post:.2f}")
print(f"T-Bill: Pre-tax={tbill_pre:.2f}, Post-tax={tbill_post:.2f}")

def calculate_switching_thresholds(muni_yield, fed, niit, state, local):
    """
    Calculates the exact yields required for other funds to beat
    a triple tax-exempt municipal money market fund.
    """
    f_tax = fed + niit + state + local
    m_tax = state + local
    
    # Calculate the breakeven switching points
    taxable_threshold = muni_yield / (1 - f_tax)
    national_muni_threshold = muni_yield / (1 - m_tax)
    
    print(f"--- Client Switching Thresholds (Targeting {muni_yield*100:.2f}% Tax-Free) ---")
    print(f"1. A Fully Taxable Fund must yield MORE than: {taxable_threshold*100:.2f}%")
    print(f"2. A National/Out-of-State Muni Fund must yield MORE than: {national_muni_threshold*100:.2f}%")

# Test with your client's current setup
calculate_switching_thresholds(
    muni_yield=0.0254,  # FSNXX at 2.54%
    fed=0.24,           # 24% Federal Bracket
    niit=0.038,         # 3.8% NIIT Surtax
    state=0.0685,       # 6.85% NY State Tax
    local=0.0388        # 3.88% NYC Local Tax
)
