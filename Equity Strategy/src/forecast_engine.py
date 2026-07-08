from src.models import CleanedFinancials, ForecastAssumptions, ForecastYear


def build_forecast(cleaned: CleanedFinancials, assumptions: ForecastAssumptions) -> list[ForecastYear]:
    if assumptions.forecast_years <= 0:
        raise ValueError("Forecast horizon must be positive.")
    if len(assumptions.revenue_growth) != assumptions.forecast_years:
        raise ValueError("Revenue growth assumptions must match forecast_years.")
    if len(assumptions.ebit_margin) != assumptions.forecast_years:
        raise ValueError("EBIT margin assumptions must match forecast_years.")

    forecast: list[ForecastYear] = []
    previous_revenue = cleaned.latest.revenue
    previous_nwc = cleaned.latest.net_working_capital

    for index in range(assumptions.forecast_years):
        year = cleaned.latest.year + index + 1
        revenue = previous_revenue * (1 + assumptions.revenue_growth[index])
        ebit = revenue * assumptions.ebit_margin[index]
        nopat = ebit * (1 - assumptions.tax_rate)
        da = revenue * assumptions.depreciation_amortisation_to_sales
        capex = revenue * assumptions.capex_to_sales
        nwc = revenue * assumptions.nwc_to_sales
        change_in_nwc = nwc - previous_nwc
        fcff = nopat + da - capex - change_in_nwc
        forecast.append(
            ForecastYear(
                year=year,
                revenue=revenue,
                ebit=ebit,
                nopat=nopat,
                depreciation_amortisation=da,
                capex=capex,
                net_working_capital=nwc,
                change_in_nwc=change_in_nwc,
                fcff=fcff,
            )
        )
        previous_revenue = revenue
        previous_nwc = nwc

    return forecast

