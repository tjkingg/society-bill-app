import streamlit as st

# --- LATEST TARIFF DATA (MERC ORDER FY 2026-27) ---
# Adani & Tata rates reduced as per newest regulations
TARIFFS = {
    "Adani Electricity (Malad)": {
        "slabs": [(100, 2.65), (200, 5.85), (200, 7.10), (float('inf'), 8.35)],
        "wheeling": 2.28,
        "fixed": 135.0,
        "tod_rebate": 0.55  # 2026 Solar Hour Rebate
    },
    "Tata Power": {
        "slabs": [(100, 2.05), (200, 5.00), (200, 10.50), (float('inf'), 11.50)],
        "wheeling": 3.05,
        "fixed": 135.0,
        "tod_rebate": 0.85
    }
}

def calculate_bill(units, provider, solar_units=0):
    data = TARIFFS[provider]
    energy_charge = 0
    temp_units = units
    
    # Slab-wise Calculation
    for limit, rate in data["slabs"]:
        if temp_units <= 0: break
        consumed = min(temp_units, limit)
        energy_charge += consumed * rate
        temp_units -= consumed
        
    wheeling = units * data["wheeling"]
    rebate = solar_units * data["tod_rebate"]
    
    # Adding fixed charges and estimated 16% Govt Duty
    subtotal = energy_charge + wheeling + data["fixed"] - rebate
    total_with_tax = subtotal * 1.16 
    
    return round(total_with_tax, 2), round(energy_charge, 2), round(wheeling, 2), round(rebate, 2)

# --- UI SETUP ---
st.set_page_config(page_title="Society Bill Finder", page_icon="⚡")
st.title("⚡ Mumbai Society Electricity Clarifier")
st.info("Updated with April 2026 Tariff Cuts")

units = st.number_input("Enter Monthly Units from Bill:", min_value=0, value=250)
solar_units = st.slider("Units used during day (9 AM - 5 PM):", 0, units, 50)

if st.button("Compare Providers"):
    col1, col2 = st.columns(2)
    
    a_total, a_ec, a_wc, a_rb = calculate_bill(units, "Adani Electricity (Malad)", solar_units)
    t_total, t_ec, t_wc, t_rb = calculate_bill(units, "Tata Power", solar_units)
    
    with col1:
        st.metric("Adani Total", f"₹{a_total}")
        st.caption(f"Energy: ₹{a_ec} | Wheel: ₹{a_wc}")
        
    with col2:
        st.metric("Tata Total", f"₹{t_total}")
        st.caption(f"Energy: ₹{t_ec} | Wheel: ₹{t_wc}")

    diff = round(abs(a_total - t_total), 2)
    cheaper = "Tata" if t_total < a_total else "Adani"
    st.success(f"**{cheaper}** saves you approximately **₹{diff}** per month!")
