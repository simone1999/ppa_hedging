import numpy as np
import pandas as pd
import streamlit as st

ccgt_efficiency = st.number_input("ccgt efficiency", value=0.52)
ccgt_eua_per_mwh = st.number_input("ccgt eua per MWh", value=0.39)
ccgt_operation_cost_per_mwh = st.number_input("ccgt additional cost per MWh", value=12)
additional_power_plant_price_per_mwh = st.number_input("mean missing price for marginal plants", value=30)
solar_ppa_established = st.checkbox("was solar PPA Contract established", value=True)
wind_ppa_established = st.checkbox("was wind PPA Contract established", value=True)

current_position_baseload_mw = pd.Series({
    2022: 0,
    2023: -10,
    2024: -10,
    2025: 0,
    2026: 5,
    2027: 5,
    2028: 5,
    2029: 10,
    2030: 10,
    2031: 10,
})
'''Current Position in baseload MW'''
st.dataframe(current_position_baseload_mw.to_frame().transpose().style.format("{:6.2f}"))

ppa_wind_gwh = pd.Series({
    2022: 100,
    2023: 100,
    2024: 100,
    2025: 100,
    2026: 100,
    2027: 100,
    2028: 100,
    2029: 100,
    2030: 100,
    2031: 100,
})
'''Wind PPA in GWh'''
st.dataframe(ppa_wind_gwh.to_frame().transpose().style.format("{:6.2f}"))

ppa_solar_gwh = pd.Series({
    2022: 80,
    2023: 80,
    2024: 80,
    2025: 80,
    2026: 80,
    2027: 0,
    2028: 0,
    2029: 0,
    2030: 0,
    2031: 0,
})
'''Solar PPA in GWh'''
st.dataframe(ppa_solar_gwh.to_frame().transpose().style.format("{:6.2f}"))

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
'''Electricity Price forward Curve in €/MWH'''
st.dataframe(price_forward.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(price_forward)

gas_forward = pd.Series({
    2022: 20.2,
    2023: 18.2,
    2024: 17.1,
    2025: 16.5,
    2026: 16.4,
    2027: 16.5,
    2028: 16.7,
    2029: 16.9,
    2030: 17.0,
    2031: 17.1,
})
'''Gas forward Curve in €/MWh'''
st.dataframe(gas_forward.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(gas_forward)

eua_forward = pd.Series({
    2022: 49.9,
    2023: 50.4,
    2024: 51.2,
    2025: 52.1,
    2026: 53.3,
    2027: 54.5,
    2028: 55.7,
    2029: 56.9,
    2030: 58.1,
    2031: 59.3,
})
'''EUA forward Curve in €/Mg_CO2'''
st.dataframe(eua_forward.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(eua_forward)

inflation = pd.Series({
    2022: 0.035,
    2023: 0.03,
    2024: 0.025,
    2025: 0.02,
    2026: 0.02,
    2027: 0.02,
    2028: 0.02,
    2029: 0.02,
    2030: 0.02,
    2031: 0.02,
})
'''European Inflation in %'''
st.dataframe(inflation.to_frame().transpose().style.format("{:6.1%}"))
st.bar_chart(inflation)

inflation_acc = (inflation + 1).cumprod() - 1
'''European Inflation accumulated in %'''
st.dataframe(inflation_acc.to_frame().transpose().style.format("{:6.1%}"))
st.bar_chart(inflation_acc)

marginal_plants = pd.DataFrame.from_dict({
    2022: {
        "CCGT": 90,
        "Wind/Solar": 3,
    },
    2026: {
        "CCGT": 75,
        "Wind/Solar": 10,
    },
    2030: {
        "CCGT": 70,
        "Wind/Solar": 15,
    },
}, orient='index')
'''Forecasted price setting Energy Sources in %'''
st.dataframe(marginal_plants.transpose().style.format("{:6.2f}"))


marginal_plants_interpolated = pd.DataFrame(index=gas_forward.index)
for column_name in marginal_plants:
    marginal_plants_interpolated[column_name] = np.interp(gas_forward.index, marginal_plants.index, marginal_plants[column_name])
marginal_plants_interpolated["Other"] = 100 - marginal_plants_interpolated.sum(axis=1)
'''Forecasted price setting Energy Sources in % interpolated'''
st.dataframe(marginal_plants_interpolated.transpose().style.format("{:6.2f}"))
st.bar_chart(marginal_plants_interpolated)

current_position = current_position_baseload_mw * 365 * 24 / 1_000  # mw baseload to gwh
'''current Position in GWh
(MW_Baseload \* 365 \* 24 / 1_000)'''
st.dataframe(current_position.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(current_position)

expectet_position = current_position.copy()
if solar_ppa_established: expectet_position += ppa_solar_gwh
if wind_ppa_established: expectet_position += ppa_wind_gwh
'''
Position after PPA in GWh \n
_current Position + Solar PPA + Wind PPA_
'''
st.dataframe(expectet_position.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(expectet_position)

ccgt_operation_costs = 1/ccgt_efficiency * gas_forward + ccgt_eua_per_mwh * eua_forward + ccgt_operation_cost_per_mwh
'''
ccgt operation costs in €/MWh \n
_1/ccgt_efficiency \* gas_forward + ccgt_eua_per_mwh \* eua_forward + ccgt_operation_cost_per_mwh_
'''
st.dataframe(ccgt_operation_costs.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(ccgt_operation_costs)

fundamental_price = marginal_plants_interpolated["CCGT"]/100 * ccgt_operation_costs + \
    marginal_plants_interpolated["Other"]/100 * additional_power_plant_price_per_mwh
'''
fundamental electricity Price in €/MWh \n
_CCGT price setting percentage \* CCGT_operation_costs + unknown_powerplant_price_setting_hours \* unknown_powerplant_operation costs_
'''
st.dataframe(fundamental_price.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(fundamental_price)

price_difference = fundamental_price - price_forward
'''price discrepancy to electricity futures in €'''
st.dataframe(price_difference.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(price_difference)

price_difference_pct = price_difference / price_forward
'''price discrepancy in % (from current future prices to fundamental prices)'''
st.dataframe(price_difference_pct.to_frame().transpose().style.format("{:6.2%}"))
st.bar_chart(price_difference_pct)

price_difference_pct_one_year = price_difference_pct.diff()
price_difference_pct_one_year[2022] = price_difference_pct[2022]
'''price discrepancy in % (from current future prices to next years future Price)'''
st.dataframe(price_difference_pct_one_year.to_frame().transpose().style.format("{:6.2%}"))
st.bar_chart(price_difference_pct_one_year)

price_difference_pct_pa = ((1 + price_difference_pct) ** (1 / (np.arange(len(price_difference_pct)) + 1))) - 1
'''price discrepancy in % Anualized'''
st.dataframe(price_difference_pct_pa.to_frame().transpose().style.format("{:6.2%}"))
st.bar_chart(price_difference_pct_pa)

# copied!
'''Position after PPA in GWh'''
st.dataframe(expectet_position.to_frame().transpose().style.format("{:6.2f}"))
st.bar_chart(expectet_position)

pass
