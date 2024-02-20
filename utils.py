import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
plt.style.use('ggplot')

def plot_harmonics(es_df, total_pathes_df,
                   diapazon_week,
                   harmonics,
                   diapazon_ser,
                   min_date, max_date,
                   min_harmonic=-6,
                   percentage_threshold: float = 0.25):
    plt.figure(figsize=(15, 10), )
    prices = es_df.loc[min_date: max_date, 'close']
    prices.plot(zorder=0, marker='o', markersize=2,
                title=f'All support for {diapazon_week} harmonics')
    unique_met_hormonics = [
        x for x in total_pathes_df.loc[diapazon_week].dropna().unique() 
        if x > min_harmonic
    ]
    harmonic_window = diapazon_ser[diapazon_week]
    colormap = colormaps['Dark2']
    # Generate a list of unique colors from the colormap
    colors = [colormap(i) for i in np.linspace(0, 1, harmonics.shape[1])]

    for idx, level in enumerate(unique_met_hormonics):
        harmonic_level_week = harmonics.loc[diapazon_week, level]
        
        upper_bound = harmonic_level_week + harmonic_window * percentage_threshold
        if (upper_bound > prices.max() or upper_bound < prices.min()):
            continue
        lower_bound = harmonic_level_week - harmonic_window * percentage_threshold
        max_x = prices.loc[min_date: max_date].index[-1]
        plt.hlines(harmonic_level_week, min_date, max_x, color=colors[idx], linestyle='--')
        plt.fill_between(prices.loc[min_date: max_date].index, lower_bound, upper_bound, alpha=0.3)

        plt.text(max_x, harmonic_level_week, f'  {level:.0f}', color=colors[idx],
                 verticalalignment='center', horizontalalignment='left')
    plt.show()
    