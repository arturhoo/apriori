# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib.mlab import griddata
import numpy as np
from matplotlib import pyplot as plt, rcParams, rc
rc('font', **{'family': 'serif', 'serif': ['Times'], 'size': 11})
rcParams['text.usetex'] = True
rcParams['text.latex.unicode'] = True
colors = ['b', 'r', 'g', 'k', 'm', 'c', 'y']
symbols = ['-', '--', '-.']
nc = len(colors)
ns = len(symbols)


def execution_time():
    fig = plt.figure(figsize=(6, 3))
    ax = fig.add_subplot(111, projection='3d')
    x = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    y = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
    z = [2.094, 1.381, 1.208, 0.873, 0.779, 0.674, 0.692, 2.106, 1.369, 1.024, 0.796, 0.71, 0.668, 0.697, 2.092, 1.37, 1.023, 0.8, 0.708, 0.659, 0.71, 2.098, 1.447, 1.002, 0.785, 0.678, 0.667, 0.649, 2.047, 1.361, 1.019, 0.779, 0.677, 0.656, 0.686, 2.049, 1.358, 0.987, 0.817, 0.655, 0.649, 0.647, 2.093, 1.367, 1.048, 0.879, 0.7, 0.665, 0.681]
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))

    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)

    surf = ax.plot_surface(X, Y, Z, rstride=2, cstride=2, cmap=cm.jet,
                           linewidth=0, antialiased=False)

    ax.set_zlim3d(np.min(Z), np.max(Z))
    ax.set_xlabel('minsup', linespacing=2)
    ax.set_ylabel('minconf', linespacing=2)
    ax.set_zlabel(u'tempo de execução (s)', linespacing=1)
    fig.colorbar(surf)
    plt.savefig('execution_time.pdf', bbox_inches='tight')


def rules():
    fig = plt.figure(figsize=(6, 3))
    ax = fig.add_subplot(111, projection='3d')
    x = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    y = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
    z = [416, 128, 36, 8, 2, 0, 0, 398, 128, 36, 8, 2, 0, 0, 337, 116, 36, 8, 2, 0, 0, 274, 101, 35, 8, 2, 0, 0, 200, 60, 23, 7, 2, 0, 0, 158, 43, 16, 5, 2, 0, 0, 74, 13, 5, 1, 1, 0, 0]
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))

    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)

    surf = ax.plot_surface(X, Y, Z, rstride=2, cstride=2, cmap=cm.jet,
                           linewidth=0, antialiased=False)

    ax.set_zlim3d(np.min(Z), np.max(Z))
    ax.set_xlabel(u'minsup', linespacing=2)
    ax.set_ylabel(u'minconf', linespacing=2)
    ax.set_zlabel(u'regras', linespacing=1)
    fig.colorbar(surf)
    plt.savefig('rules.pdf', bbox_inches='tight')


def top_15_1_itemsets():
    f = open('../1-itemsets.txt', 'r')
    one_itemsets = []
    for line in f:
        one_itemsets.append(tuple(line.strip().split()))
        one_itemsets[-1][0].replace('<', '\<')
    sorted_one_itemsets = sorted(one_itemsets, key=lambda tup: -float(tup[1]))

    x, y = map(list, zip(*sorted_one_itemsets))

    # attrs = set()
    # for item in x:
    #     attr = item.split('=')[0]
    #     attrs.add(attr)
    # print attrs

    y = map(float, y)
    cap = 15
    y = y[:cap]
    x = x[:cap]
    ind = range(len(y))
    print ind
    print y
    fig = plt.figure(figsize=(9, 3.5))
    ax = fig.add_subplot(111)
    width = 0.55
    rects1 = ax.bar(ind, y, width, align='center', hatch='///', color='w')

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                     round(height, 2), ha='center', va='bottom')
    autolabel(rects1)
    ax.set_xticks(ind)
    ax.set_xticklabels(x)
    fig.autofmt_xdate(rotation=55)
    # ax.set_xlabel(xlabel)
    ax.set_ylabel(u'Suporte')
    ax.set_ylim(0, 1)
    ax.set_xlim(ind[0] - 0.5, ind[-1] + 0.5)
    ax.autoscale_view()
    ax.grid(True)
    plt.savefig('top_15_1_itemsets.pdf', bbox_inches='tight')


def atm():
    fig = plt.figure(figsize=(6, 3))
    host = fig.add_subplot(111)
    par1 = host.twinx()
    host.set_xlabel(ur'\textit{atm}')
    host.set_ylabel('regras')
    par1.set_ylabel(u'tempo de execução (s)')
    # ax.set_xlim(x[0] - 1, x[-1] + 1)
    atm_values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    l1 = [146, 92, 74, 66, 60, 59, 59, 57, 55]
    ref = [23] * len(atm_values)
    l2 = [45.508, 42.347, 43.119, 44.094, 44.818, 44.472, 43.291, 42.25, 43.719]
    host.set_ylim(0, max(l1) + 10)
    par1.set_ylim(0, 50)
    p1, = host.plot(atm_values, l1, 'b-', label=u'Regras', linewidth=2)
    p2, = host.plot(atm_values, ref, 'k--', label=ur'Regras sem \textit{atm}', linewidth=2)
    p3, = par1.plot(atm_values, l2, 'r-', label=u'Tempo de execução', linewidth=2)
    host.autoscale_view()
    par1.autoscale_view()
    host.grid(True)

    box = host.get_position()
    host.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8])
    box = par1.get_position()
    par1.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8])
    lines = [p1, p2, p3]
    fig.legend(lines, [l.get_label() for l in lines], loc='upper center',
               ncol=3, bbox_to_anchor=(0.5, 0.15), prop={'size': 10})

    plt.savefig('atm_impact.pdf')
    # plt.savefig('test.png', bbox_inches='tight')


if __name__ == '__main__':
    top_15_1_itemsets()
    execution_time()
    rules()
    atm()
