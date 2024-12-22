import uuid

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


data = pd.read_csv('population.csv')
data.rename(columns={
    '1': 'Year',
    '2': 'Total',
    '3': 'Male',
    '4': 'Female',
    '5': 'people +/-',
    '6': 'density',
    '7': 'Growth_Rate'
}, inplace=True)
data = data.drop('8', axis=1)

data = data[['Year', 'Total']]  # Выберите нужные столбцы

y = data['Total'].values

# Построение модели ARIMA
model_arima = ARIMA(y, order=(50, 2, 6))  # Параметры (p, d, q) можно подобрать
model_arima_fit = model_arima.fit()

def get_prediction(year_to_predict: int):

    last_year = data['Year'].max()

    future_years = np.arange(last_year + 1, year_to_predict + 1).reshape(-1, 1)

    # Прогноз на будущее
    future_steps = len(future_years)
    future_predictions_arima = model_arima_fit.forecast(steps=future_steps)

    # Визуализация
    plt.figure(figsize=(8, 4))
    plt.plot(data['Year'], data['Total'], label="Фактические данные", color="blue")
    plt.plot(future_years, future_predictions_arima, label="Прогноз ARIMA", color="purple", linestyle="--")
    plt.xlabel("Год")
    plt.ylabel("Численность населения")
    plt.title("Прогноз численности населения (ARIMA)")
    plt.legend()
    plt.grid()
    plt.savefig(f'forecasts/population_forecast_{year_to_predict}.png', format='png', dpi=300)

    # Закрытие графика
    plt.close()

    return int(future_predictions_arima[-1])
