# Solar Project Financial Calculator — Documentation

## 1. Key assumptions

- Installed cost : $2.50/W
- Annual generation (Location-agnostic) : 1,400 kWh/kW
- Electricity price escalation : 2.5%/yr
- O&M cost : $15/kW/yr
- Investment Tax Credit (ITC) : 30%
- Project lifetime : 25 years
- Financing : All-equity, No debt
- Degradation : None
- Electricity rates : State-level residential average, Source: ElectricChoice.com (May 2026)

--

## 2. Financial model structure

- Year 0 : upfront investment

The project begins with a one-time cash outflow representing the benefits of ITC

Gross cost  = System size (kW) × 1,000 × $2.50/W
ITC credit  = Gross cost × 30%
Net cost    = Gross cost − ITC credit

- Years 1–25 : annual cash flows

Each year generates a net cash flow based on avoided electricity cost minus O&M:

Escalated rate ($/kWh) = Base rate × (1 + 2.5%)^(n − 1)
Energy savings ($)     = Annual generation (kWh) × Escalated rate ($/kWh)
O&M cost ($)           = System size (kW) × $15/kW  [flat, no escalation]
Net cash flow ($)      = Energy savings − O&M cost

- Cumulative cash flow and payback

The cumulative cash flow tracks the running total from Year 0 onward:

Cumulative (Year 0) = − Net cost
Cumulative (Year N) = Cumulative (Year N−1) + Net cash flow (Year N)

Payback period is the first year in which the cumulative cash flow turns positive, which means the project has recovered its initial investment.

- Internal Rate of Return (IRR)

The project IRR is the discount rate that sets the net present value (NPV) of all cash flows to zero

Calculated using npf.irr()

--

## 3. Technical architecture

Language : Python, Standard for financial modeling
Dashboard framework & hosting : Streamlit, read a Python script into a web app, and deploys directly from GitHub
Data tables : Pandas, tabular data library
Financial math : numpy-financial, provides necessary calculation functions

Limitations
- Generation assumes a flat 1,400 kWh/kW regardless of location
- No panel degradation rate is modeled (typically 0.5%/year)
- No financing & rates scenarios (debt, lease, PPA) included
