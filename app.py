# ============================================================
# SOLAR PROJECT FINANCIAL CALCULATOR
# Built with Streamlit — a Python library that turns a
# regular Python script into an interactive web dashboard.
#
# How Streamlit works:
# - Every time the user changes an input, the whole script
#   runs top to bottom again automatically.
# - st.something() functions display things on the page.
# - That's it. No HTML, no JavaScript needed.
# ============================================================

import streamlit as st        # the dashboard framework
import pandas as pd            # for creating and displaying tables
import numpy_financial as npf  # for IRR calculation (npf.irr)

# ── PAGE CONFIGURATION ───────────────────────────────────────
# Must be the first Streamlit command in the script.
# Sets the browser tab title and uses wide layout.
st.set_page_config(
    page_title="Solar Project Calculator",
    layout="wide"
)

# ── TITLE & DESCRIPTION ──────────────────────────────────────
st.title("Solar Project Financial Calculator")
st.caption("25-year cash flow model · All-equity · No financing costs")

# ── MODEL ASSUMPTIONS (CONSTANTS) ────────────────────────────
# These never change — they are the financial model assumptions.
# Defining them at the top makes them easy to find and update.

COST_PER_W  = 2.50    # $2.50 per watt installed cost
GEN_PER_KW  = 1400    # 1,400 kWh generated per kW per year
ESCALATION  = 0.025   # electricity price grows 2.5% per year
OM_PER_KW   = 15      # $15 per kW per year for operations & maintenance
ITC         = 0.30    # 30% Investment Tax Credit applied in Year 0
YEARS       = 25      # project lifetime

# ── ELECTRICITY RATES BY STATE ───────────────────────────────
# Dictionary: state name → residential electricity rate in ¢/kWh
# Source: ElectricChoice.com, May 2026

STATE_RATES = {
    "Alabama": 16.79, "Alaska": 26.57, "Arizona": 15.62,
    "Arkansas": 13.32, "California": 33.75, "Colorado": 16.33,
    "Connecticut": 27.84, "Delaware": 18.39, "District of Columbia": 24.03,
    "Florida": 15.77, "Georgia": 14.60, "Hawaii": 39.89,
    "Idaho": 12.51, "Illinois": 18.82, "Indiana": 17.42,
    "Iowa": 13.54, "Kansas": 15.23, "Kentucky": 13.68,
    "Louisiana": 12.44, "Maine": 29.55, "Maryland": 22.40,
    "Massachusetts": 31.51, "Michigan": 20.55, "Minnesota": 16.44,
    "Mississippi": 14.53, "Missouri": 13.01, "Montana": 14.33,
    "Nebraska": 13.19, "Nevada": 13.83, "New Hampshire": 25.12,
    "New Jersey": 22.48, "New Mexico": 15.09, "New York": 23.44,
    "North Carolina": 14.37, "North Dakota": 12.71, "Ohio": 16.81,
    "Oklahoma": 13.44, "Oregon": 14.22, "Pennsylvania": 18.15,
    "Rhode Island": 28.43, "South Carolina": 15.22, "South Dakota": 14.11,
    "Tennessee": 13.77, "Texas": 15.10, "Utah": 12.89,
    "Vermont": 22.76, "Virginia": 15.92, "Washington": 12.93,
    "West Virginia": 13.11, "Wisconsin": 18.06, "Wyoming": 12.55
}

# ── KEY INPUTS ───────────────────────────────
st.subheader("Inputs")
col1, col2 = st.columns(2)

# Dropdown to select a US state
# sorted() sorts the state names alphabetically

with col1 :
    selected_state = st.selectbox(
    label="US State",
    options=sorted(STATE_RATES.keys()),  # list of all state names
    index=sorted(STATE_RATES.keys()).index("New York")  # default to New York
)

# Number input for system size
with col2 :
    system_size_kw = st.number_input(
    label="System size (kW DC)",
    min_value=1,
    max_value=1000,
    value=10,      # default value
    step=1,         # how much each click of the arrow changes it
    key="system_size"
)

st.button("Calculate",type="primary")

# ── SIDEBAR  ───────────────────────────────────────────

# Show the model assumptions in the sidebar so the user can see them
st.sidebar.subheader("Model assumptions")
st.sidebar.caption(f"Installed cost: ${COST_PER_W}/W")
st.sidebar.caption(f"Generation: {GEN_PER_KW:,} kWh/kW/yr")
st.sidebar.caption(f"Electricity escalation: {ESCALATION*100:.1f}%/yr")
st.sidebar.caption(f"O&M cost: ${OM_PER_KW}/kW/yr")
st.sidebar.caption(f"ITC: {int(ITC*100)}% in Year 0")
st.sidebar.caption("Source: ElectricChoice.com (May 2026)")

# ── FINANCIAL CALCULATIONS ───────────────────────────────────
# All the math happens here, using the inputs from the sidebar.
# This section runs every time the user changes an input.

# Look up the electricity rate for the selected state
rate_cents = STATE_RATES[selected_state]  # ¢/kWh

# --- Upfront costs ---
gross_cost  = system_size_kw * 1000 * COST_PER_W   # total before ITC
itc_credit  = gross_cost * ITC                       # 30% tax credit
net_cost    = gross_cost - itc_credit                # actual cash out Year 0

# --- Annual generation ---
annual_gen  = system_size_kw * GEN_PER_KW   # kWh/year
annual_om   = system_size_kw * OM_PER_KW    # $/year O&M cost

# --- Build 25-year cash flow model ---
# We store each year's data in a list of dictionaries,
# then convert to a pandas DataFrame for easy display.

cashflows   = [-net_cost]   # Year 0 is a cash outflow (investment)
rows        = []            # will become the table
cumulative  = -net_cost     # running total starts at Year 0 outflow
payback_year = None         # track when cumulative turns positive

for year in range(1, YEARS + 1):
    # range(1, 26) gives us [1, 2, 3, ... 25]

    # Electricity rate escalates 2.5% per year
    # Year 1: rate × 1.025^0 = unchanged
    # Year 2: rate × 1.025^1 = +2.5%
    # Year 3: rate × 1.025^2 = +5.06% etc.
    rate_this_year = (rate_cents / 100) * (1 + ESCALATION) ** (year - 1)
    # ** is Python's exponentiation operator (same as Math.pow in JS)

    # Energy savings = electricity avoided × rate
    energy_savings = annual_gen * rate_this_year

    # Net cash flow = savings minus O&M cost
    net_cf = energy_savings - annual_om

    # Update running cumulative total
    cumulative += net_cf   # += means cumulative = cumulative + net_cf

    # Add to IRR cash flow array
    cashflows.append(net_cf)

    # Detect payback year (first year cumulative goes non-negative)
    if payback_year is None and cumulative >= 0:
        payback_year = year

    # Store this year's data as a dictionary in the rows list
    rows.append({
        "Year":               year,
        "Generation (kWh)":   int(annual_gen),
        "Rate (¢/kWh)":       round(rate_this_year * 100, 2),
        "Energy Savings ($), annual generation x rate": round(energy_savings, 0),
        "O&M Cost ($)":       round(annual_om, 0),
        "Net Cash Flow ($), energy savings - annual O&M":  round(net_cf, 0),
        "Cumulative of net cash flow ($)":     round(cumulative, 0),
    })

# Calculate IRR using numpy_financial
# npf.irr() takes a list of cash flows and returns the IRR as a decimal
irr = npf.irr(cashflows)

# ── METRIC CARDS (KEY OUTPUTS) ───────────────────────────────
# st.columns(n) splits the page into n equal columns side by side.
# We use this to show multiple metric cards in a row.

st.subheader("Key metrics")
col1, col2, col3, col4, col5 = st.columns(5)

# st.metric() displays a labeled number — built into Streamlit
with col1:
    st.metric(
        label="System upfront price",
        value=f"${gross_cost:,.0f}",   # :,.0f = comma-separated, no decimals
        help="Total installed cost before the ITC tax credit"
    )

with col2:
    st.metric(
        label="Net cost after ITC",
        value=f"${net_cost:,.0f}",
        help="Upfront cost after applying the 30% Investment Tax Credit"
    )

with col3:
    st.metric(
        label="Annual generation",
        value=f"{annual_gen:,.0f} kWh",
        help="Estimated annual energy production (location-agnostic)"
    )

with col4:
    st.metric(
        label="Project IRR",
        value=f"{irr*100:.1f}%",       # multiply by 100 to convert to %
        help="Internal Rate of Return over 25 years, unlevered"
    )

with col5:
    st.metric(
        label="Payback period",
        value=f"{payback_year} yrs" if payback_year else ">25 yrs",
        help="Year when cumulative cash flow turns positive"
    )

# ── CASH FLOW TABLE ───────────────────────────────────────────
st.divider()
st.subheader("25-year cash flow table")

# Add the Year 0 row at the top (the investment year)
year_zero = {
    "Year":               0,
    "Generation (kWh)":   "—",
    "Rate (¢/kWh)":       "—",
    "Energy Savings ($), annual generation x rate": f"ITC: +${itc_credit:,.0f}",
    "O&M Cost ($)":       "—",
    "Net Cash Flow ($), energy savings - annual O&M":  round(-net_cost, 0),
    "Cumulative of net cash flow ($)":     round(-net_cost, 0),
}

# Convert rows list to a pandas DataFrame
# A DataFrame is like a spreadsheet in Python — rows and columns
df = pd.DataFrame([year_zero] + rows)

# Display the table using Streamlit
# hide_index=True removes the default 0,1,2... row numbers on the left
st.dataframe(
    df,
    hide_index=True,
    use_container_width=True   # stretches the table to fill the full width
)
