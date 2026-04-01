import streamlit as st

# --- ACTUAL DATA FROM MARCH 2026 BILL ---
TATA_RATES = {
    "slabs": [(100, 2.00), (200, 5.20), (200, 10.79), (float('inf'), 11.79)],
    "wheeling_rate": 2.93,
    "fixed_base": 160.0,
    "fixed_addon": 250.0, # For 3-phase/Load > 10kW
    "tose_rate": 0.3594,
    "wheeling_loss_factor": 1.0536 # 5.36% adjustment
}

def calculate_accurate_bill(metered_units, phase_type="3 Phase"):
    # 1. Calculate Billed Units (Account for Wheeling Loss)
    billed_units = metered_units * TATA_RATES["wheeling_loss_factor"]
    
    # 2. Energy Charges (Slab-wise)
    energy_charge = 0
    temp_units = billed_units
    for limit, rate in TATA_RATES["slabs"]:
        if temp_units <= 0: break
        consumed = min(temp_units, limit)
        energy_charge += consumed * rate
        temp_units -= consumed
        
    # 3. Fixed Charges
    fixed = TATA_RATES["fixed_base"]
    if phase_type == "3 Phase":
        fixed += TATA_RATES["fixed_addon"]
        
    # 4. Other Components
    wheeling = billed_units * TATA_RATES["wheeling_rate"]
    tose = billed_units * TATA_RATES["tose_rate"]
    
    # 5. Taxes (16% Duty on Energy + Wheeling + Fixed)
    subtotal = energy_charge + wheeling + fixed
    e_duty = subtotal * 0.16
    
    total = subtotal + tose + e_duty
    return round(total), round(billed_units, 1)

# --- STREAMLIT UI ---
st.title("⚡ Society Flat Bill Decoder (March 2026) - Tejas")
st.info("Logic calibrated as per Tata Power Bill")

m_units = st.number_input("Enter METERED Units (from your meter):", value=465)
phase = st.selectbox("Connection Type:", ["3 Phase", "1 Phase"])

if st.button("Analyze My Bill"):
    total_amt, b_units = calculate_accurate_bill(m_units, phase)
    
    st.metric("Estimated Total Bill", f"₹{total_amt}")
    st.write(f"**Note:** Your metered {m_units} units become **{b_units} billed units** due to the 5.36% Malad network loss.")
    
    if total_amt > 6000:
        st.warning("Your bill is in the high-usage slab (>300 units). Consider shifting heavy loads to 'Solar Hours' if you have a smart meter.")
