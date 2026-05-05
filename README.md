# Solar Project Financial Calculator

A web-based financial modeling dashboard for US residential rooftop solar projects. Built with Python and Streamlit.

The app uses two key inputs: a US state and system size, then returns a full 25-year cash flow projection, including project IRR payback period, annual energy savings, and upfront cost after the federal Investment Tax Credit (ITC).

Live demo: https://solarproject-hans.streamlit.app

(rest of README below)

---

## What it does

Key Input:
- US State --> Determines the residential electricity rate (¢/kWh)
- System size (kW DC) --> Determines system cost, generation, and O&M

Key Output:
- System upfront price --> Gross installed cost before incentives
- Net cost after ITC --> Effective cost after 30% federal tax credit
- Annual generation --> Estimated kWh generated per year
- Project IRR --> 25-year internal rate of return (unlevered)
- Payback period --> Year when cumulative cash flow turns positive
- 25-year cash flow table --> Year-by-year breakdown of all cash flows

---

## Setup instructions

Step 1 — Download the code
Download the GitHub repo (default in ZIP) → unzip the folder

Step 2 — Install dependencies
Open Terminal (Mac) or Command Prompt (Windows), locate the unzipped folder, and run:

    pip install -r requirements.txt

Step 3 — Run the app
    streamlit run app.py

The app opens automatically in your browser (localhost)


## Files in this repo

solar-dashboard/
1. app.py                  # Main application with all calculations and dashboard UI connected to Streamlit
2. requirements.txt        # Python libraries needed to run the app
3. README.md               # This file

---

## Library Dependencies

- streamlit --> Dashboard framework and UI
- pandas --> Cash flow table
- numpy & numpy-financial --> Numerical & IRR calculation

---

## Data source

Residential electricity rates by state sourced from https://www.electricchoice.com/electricity-prices-by-state/ (May 2026). Rates are hardcoded under the `STATE_RATES` dictionary