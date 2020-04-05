import numpy as np
import matplotlib.pyplot as plt




def plot_divYield_PE(stocks):
    return _scatter_plot_with_labels(stocks,
                                     lambda s: s.PE, 'PE',
                                     lambda s: s.dividendYield or 0.0, 'divYield',
                                     lambda s: s.symbol,
                                     lambda s: s.PE > 100)

def _scatter_plot_with_labels(
        stocks, x_lambda, x_name, y_lambda, y_name, label_lambda, filter=None):
    x = []
    y = []
    labels = []
    for stock in stocks:
        if filter and filter(stock):
            continue
        x.append(x_lambda(stock))
        y.append(y_lambda(stock))
        labels.append(label_lambda(stock))

    plt.rcParams['lines.markersize'] =1
    fig, ax = plt.subplots()
    ax.scatter(x, y, marker=',')
    plt.xlabel(x_name)
    plt.ylabel(y_name)

    for i, txt in enumerate(labels):
        ax.annotate(txt, (x[i], y[i]),size=3)

    return fig
