import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches




def plot_divYield_PE(stocks):
    return _scatter_plot_with_labels(stocks,
                                     lambda s: s.PE or -10.0, 'PE',
                                     lambda s: s.dividendYield or 0.0, 'divYield',
                                     lambda s: s.symbol,
                                     lambda s: str(s.sector),
                                     lambda s: (s.PE or -10.0) > 100)

def _make_color_map(item_list):
    item_types = set(item_list)
    i = 0
    d = {}
    for item in item_types:
        d[item] = i
        i += 1
    return d

def _map_stocks_dict(stocks, color_lambda):
    d = {}
    for s in stocks:
        c = color_lambda(s)
        if c in d:
            d[c].append(s)
        else:
            d[c] = [s]
    return d

def _scatter_plot_with_labels(
        stocks, x_lambda, x_name, y_lambda, y_name, label_lambda,
        color_lambda, filter=None):
    plt.rcParams['lines.markersize'] = 1
    colormap = _make_color_map(color_lambda(s) for s in stocks)
    stockmap = _map_stocks_dict(stocks, color_lambda)
    fig, ax = plt.subplots()
    for stockType, typeStocks in stockmap.items():
        x = []
        y = []
        labels = []
        colors = []
        for stock in typeStocks:
            if filter and filter(stock):
                continue
            x.append(x_lambda(stock))
            y.append(y_lambda(stock))
            labels.append(label_lambda(stock))
            colors.append(colormap[stockType])
        ax.scatter(x, y, marker=',', label=stockType)
        for i, txt in enumerate(labels):
            ax.annotate(txt, (x[i], y[i]), size=1)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    ax.legend()
    ax.grid(True)
    # plt.legend(handles=[patches.Patch(color=v, label=k) for k, v in colormap.items()])



    return fig
