import numpy as np
import pandas as pd
import streamlit as st

expected_prices = pd.Series({
    2022: 65.38,
    2023: 60.19,
    2024: 56.80,
    2025: 54.34,
    2026: 52.74,
    2027: 52.43,
    2028: 52.23,
    2029: 52.02,
    2030: 51.65,
    2031: 52.11,
})
'''expected Prices in €/MWh'''
st.bar_chart(expected_prices)

constant_price_offset = st.number_input("constant price offset", value=5)
price_slope_offset = st.number_input("Price slope offset", value=0)
fees_per_mwh = st.number_input("Future Fees per MWh", value=0.0125, format="%.4f")

prices = expected_prices + constant_price_offset + np.arange(10) * price_slope_offset
'''Prices after offset in €/MWh'''
st.bar_chart(prices)

price_delta = prices - expected_prices
'''price delta in €/MWh'''
st.bar_chart(price_delta)


annual_future_price_increase_pct = pd.Series({
    2022: 0.0753,
    2023: 0.1096,
    2024: 0.1210,
    2025: 0.1279,
    2026: 0.0775,
    2027: 0.0969,
    2028: 0.0447,
    2029: 0.0359,
    2030: 0.0156,
    2031: 0.0267,
})
price_forward = pd.Series({
    2022: 60.8,
    2023: 50.8,
    2024: 43.5,
    2025: 37.9,
    2026: 34.9,
    2027: 32.6,
    2028: 31.6,
    2029: 30.8,
    2030: 30.3,
    2031: 30.1,
})
original_positions = pd.Series({
    2022: 180.000,
    2023: 92.400,
    2024: 92.400,
    2025: 180.000,
    2026: 223.800,
    2027: 143.800,
    2028: 143.800,
    2029: 187.600,
    2030: 187.600,
    2031: 187.600,
})

'''# no Hedge'''
positions = original_positions.copy()
'''current Positions in GWh'''
st.bar_chart(positions)

delta_earnings = price_delta * positions * 1_000
'''earnings Delta without anny Hedge'''
st.bar_chart(delta_earnings)

value_change = np.sum(delta_earnings)
yearly_gains = np.sum(annual_future_price_increase_pct * positions * 1_000 * expected_prices)
total_value = np.sum(positions * 1_000 * price_forward)
traded_mwh = (positions - original_positions) * 1_000
cost_of_realocation = np.sum(price_forward * traded_mwh + np.abs(traded_mwh) * fees_per_mwh)
'''gains for Position reallocation'''
st.text("{:,.0f}".format(-cost_of_realocation) + "€")
'''total Value of Position in current Futures Prices'''
st.text("{:,.0f}".format(total_value) + "€")
'''total change of Value due to delivery price discrepancy'''
st.text("{:,.0f}".format(value_change) + "€")
'''comming year Gains due to Future Price Increase'''
st.text("{:,.0f}".format(yearly_gains) + "€")


'''# full Hedge'''
positions = np.zeros(10)
positions = pd.Series(positions, np.arange(2022, 2032))
'''Positions completely Hedged in GWh'''
st.bar_chart(positions)

delta_earnings = price_delta * positions
'''earnings Delta with everything hedged'''
st.bar_chart(delta_earnings)

value_change = np.sum(delta_earnings)
yearly_gains = np.sum(annual_future_price_increase_pct * positions * 1_000 * expected_prices)
total_value = np.sum(positions * 1_000 * price_forward)
traded_mwh = (positions - original_positions) * 1_000
cost_of_realocation = np.sum(price_forward * traded_mwh + np.abs(traded_mwh) * fees_per_mwh)
'''gains for Position reallocation'''
st.text("{:,.0f}".format(-cost_of_realocation) + "€")
'''total Value of Position in current Futures Prices'''
st.text("{:,.0f}".format(total_value) + "€")
'''total change of Value due to delivery price discrepancy'''
st.text("{:,.0f}".format(value_change) + "€")
'''comming year Gains due to Future Price Increase'''
st.text("{:,.0f}".format(yearly_gains) + "€")


'''# first half constant Hedge'''
positions = original_positions.copy()
positions[:5] = -np.mean(positions[5:])
'''Positions first half constant Hedge in GWh'''
st.bar_chart(positions)

delta_earnings = price_delta * positions * 1_000
'''earnings Delta with first half constant Hedge'''
st.bar_chart(delta_earnings)

value_change = np.sum(delta_earnings)
yearly_gains = np.sum(annual_future_price_increase_pct * positions * 1_000 * expected_prices)
total_value = np.sum(positions * 1_000 * price_forward)
traded_mwh = (positions - original_positions) * 1_000
cost_of_realocation = np.sum(price_forward * traded_mwh + np.abs(traded_mwh) * fees_per_mwh)
'''gains for Position reallocation'''
st.text("{:,.0f}".format(-cost_of_realocation) + "€")
'''total Value of Position in current Futures Prices'''
st.text("{:,.0f}".format(total_value) + "€")
'''total change of Value due to delivery price discrepancy'''
st.text("{:,.0f}".format(value_change) + "€")
'''comming year Gains due to Future Price Increase'''
st.text("{:,.0f}".format(yearly_gains) + "€")


'''# first half pivot Hedge'''
'''from now on all Positions are at constant 150 GWh per year to simplify the explanation'''
positions = np.ones(10) * 2_000
positions[:5] = -2_000
positions[0] += 10_000
positions[1] += 5_000
positions[2] += 0
positions[3] += -5_000
positions[4] += -10_000
positions *= 0.075
positions = pd.Series(positions, np.arange(2022, 2032))
'''Positions first half pivot Hedge in GWh'''
st.bar_chart(positions)

delta_earnings = price_delta * positions * 1_000
'''earnings Delta with first half pivot Hedge'''
st.bar_chart(delta_earnings)

value_change = np.sum(delta_earnings)
yearly_gains = np.sum(annual_future_price_increase_pct * positions * 1_000 * expected_prices)
total_value = np.sum(positions * 1_000 * price_forward)
traded_mwh = (positions - original_positions) * 1_000
cost_of_realocation = np.sum(price_forward * traded_mwh + np.abs(traded_mwh) * fees_per_mwh)
'''gains for Position reallocation'''
st.text("{:,.0f}".format(-cost_of_realocation) + "€")
'''total Value of Position in current Futures Prices'''
st.text("{:,.0f}".format(total_value) + "€")
'''total change of Value due to delivery price discrepancy'''
st.text("{:,.0f}".format(value_change) + "€")
'''comming year Gains due to Future Price Increase'''
st.text("{:,.0f}".format(yearly_gains) + "€")


'''
# calculation of the Pivot Hedge
there are 2 Formulars that need to be true
- sum(positions) = 0
- sum(for i=0 to (total_years - 1): year[i] * (i - (total_years - 1) / 2)) = 0
'''


'''# first two pivot Hedge'''
positions = np.ones(10) * 2_000
positions[:2] -= 10_000
positions[0] += 80_000
positions[1] -= 80_000
positions *= 0.075
positions = pd.Series(positions, np.arange(2022, 2032))
'''Positions first two pivot Hedge in GWh'''
st.bar_chart(positions)

delta_earnings = price_delta * positions * 1_000
'''earnings Delta with first two pivot Hedge'''
st.bar_chart(delta_earnings)

value_change = np.sum(delta_earnings)
yearly_gains = np.sum(annual_future_price_increase_pct * positions * 1_000 * expected_prices)
total_value = np.sum(positions * 1_000 * price_forward)
traded_mwh = (positions - original_positions) * 1_000
cost_of_realocation = np.sum(price_forward * traded_mwh + np.abs(traded_mwh) * fees_per_mwh)
'''gains for Position reallocation'''
st.text("{:,.0f}".format(-cost_of_realocation) + "€")
'''total Value of Position in current Futures Prices'''
st.text("{:,.0f}".format(total_value) + "€")
'''total change of Value due to delivery price discrepancy'''
st.text("{:,.0f}".format(value_change) + "€")
'''comming year Gains due to Future Price Increase'''
st.text("{:,.0f}".format(yearly_gains) + "€")


'''# annual return optimized pivot Hedge'''
positions = np.ones(10) * 2_000
positions[0] += -10_000  # -20_000
positions[1] += 5_000
positions[2] += 7_000
positions[3] += 3_000 + 18_000  # 8_000 + 53_000
positions[4] += -25_000 - 18_000  # -20_000 - 53_000
positions *= 0.075
positions = pd.Series(positions, np.arange(2022, 2032))
'''Positions annual return optimized pivot Hedge in GWh'''
st.bar_chart(positions)

delta_earnings = price_delta * positions * 1_000
'''earnings Delta with annual return optimized pivot Hedge'''
st.bar_chart(delta_earnings)

value_change = np.sum(delta_earnings)
yearly_gains = np.sum(annual_future_price_increase_pct * positions * 1_000 * expected_prices)
total_value = np.sum(positions * 1_000 * price_forward)
traded_mwh = (positions - original_positions) * 1_000
cost_of_realocation = np.sum(price_forward * traded_mwh + np.abs(traded_mwh) * fees_per_mwh)
'''gains for Position reallocation'''
st.text("{:,.0f}".format(-cost_of_realocation) + "€")
'''total Value of Position in current Futures Prices'''
st.text("{:,.0f}".format(total_value) + "€")
'''total change of Value due to delivery price discrepancy'''
st.text("{:,.0f}".format(value_change) + "€")
'''comming year Gains due to Future Price Increase'''
st.text("{:,.0f}".format(yearly_gains) + "€")


'''# annual return optimized pivot Hedge with flattened front Year'''
positions = np.ones(10) * 2_000
positions[0] = 0
positions[1] += 3_000
positions[2] += 3_000
positions[3] += 2_000 + 1_000  # 8_000 + 53_000
positions[4] += -26_000 - 1_000  # -20_000 - 53_000
positions *= 0.075
positions = pd.Series(positions, np.arange(2022, 2032))
'''Positions annual return optimized pivot Hedge in GWh'''
st.bar_chart(positions)

delta_earnings = price_delta * positions * 1_000
'''earnings Delta with annual return optimized pivot Hedge'''
st.bar_chart(delta_earnings)

value_change = np.sum(delta_earnings)
yearly_gains = np.sum(annual_future_price_increase_pct * positions * 1_000 * expected_prices)
total_value = np.sum(positions * 1_000 * price_forward)
traded_mwh = (positions - original_positions) * 1_000
cost_of_realocation = np.sum(price_forward * traded_mwh + np.abs(traded_mwh) * fees_per_mwh)
'''gains for Position reallocation'''
st.text("{:,.0f}".format(-cost_of_realocation) + "€")
'''total Value of Position in current Futures Prices'''
st.text("{:,.0f}".format(total_value) + "€")
'''total change of Value due to delivery price discrepancy'''
st.text("{:,.0f}".format(value_change) + "€")
'''comming year Gains due to Future Price Increase'''
st.text("{:,.0f}".format(yearly_gains) + "€")


'''
# Fundamentals hedge
Positions can be Hedged with Fundamentals\n
1MWh Gas Power is approximately:
- 1.96 MWh Gas
- 0.39 EUA
- Constant Costs of 12€

combined with the forecastet marginal plants and the fundamental Asset for the non CCGT or Wind/Solar Power Plant\n
Electricity can be Hedged with fundamentals

Fundamentals Futures Price does not decline in long distance Futures\n
short Positions can be Hedged with Fundamentals nearly for free\n
long Positions can be Hedged with Electricity futures with an large annual return\n
Fundamental Futures provide additional Liquidity\n
'''


'''# annual return optimized pivot Hedge with partly fundamental Hedging'''
positions = np.ones(10) * 2_000
positions[0] += -10_000  # -20_000
positions[1] += 5_000
positions[2] += 7_000
positions[3] += 3_000 + 18_000  # 8_000 + 53_000
positions[4] += -25_000 - 18_000  # -20_000 - 53_000
positions *= 0.075

positions_fundamental = np.zeros_like(positions)
positions_energy = np.zeros_like(positions)
for i in range(10):
    if positions[i] < 0:
        positions_fundamental[i] = positions[i]
    else:
        positions_energy[i] = positions[i]
positions = pd.Series(positions, np.arange(2022, 2032))
positions_mixed = pd.DataFrame({"electricity futures": positions_energy, "fundamental futures": positions_fundamental}, np.arange(2022, 2032))
'''Positions annual return optimized pivot Hedge with partly fundamental Hedging in GWh'''
st.bar_chart(positions_mixed)

delta_earnings = price_delta * positions * 1_000
'''earnings Delta with annual return optimized pivot Hedge with partly fundamental Hedging'''
st.bar_chart(delta_earnings)

value_change = np.sum(delta_earnings)
yearly_gains = np.sum(annual_future_price_increase_pct * positions_energy * 1_000 * expected_prices)
fundamentals_value = positions_mixed["fundamental futures"] * 1_000 * expected_prices
total_value = np.sum(positions_mixed["electricity futures"] * 1_000 * price_forward + fundamentals_value)
traded_mwh_electricity = (positions_mixed["electricity futures"] - original_positions) * 1_000
cost_of_realocation = np.sum(price_forward * traded_mwh_electricity + fundamentals_value)
'''gains for Position reallocation'''
st.text("{:,.0f}".format(-cost_of_realocation) + "€")
'''total Value of Position in current Futures Prices'''
st.text("{:,.0f}".format(total_value) + "€")
'''total change of Value due to delivery price discrepancy'''
st.text("{:,.0f}".format(value_change) + "€")
'''comming year Gains due to Future Price Increase'''
st.text("{:,.0f}".format(yearly_gains) + "€")


'''
# Statistical Arbitrage
Since this Market seems verry imbalanced, even statistical Arbitrage is possible
- take hughe long Position on Electricity Futures
- Hedge Position with fundamental Futures
- profit is annual Return of electricity Futures - annual costs of Fundamental Futures (nearly free)
'''