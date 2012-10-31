# -*- coding: utf-8 -*-
from sys import exit, exc_info
from itertools import combinations
from collections import defaultdict


def load_data(file_name):
    try:
        with open(file_name) as f:
            content = f.readlines()
            f.close()
    except IOError as e:
        print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
        exit()
    except:
        print "Unexpected error:", exc_info()[0]
        exit()
    return content


def remove_items_without_min_support(item_freq, min_sup, transactions):
    for k, v in item_freq.items():
        if float(v) / len(transactions) < min_sup:
            del item_freq[k]


if __name__ == '__main__':
    content = load_data('data/census_mod.dat')
    one_item_freq = defaultdict(int)
    two_item_freq = defaultdict(int)
    transactions = []
    for line in content:
        transactions.append(frozenset(line.strip().split()))

    for transaction in transactions:
        for item in transaction:
            one_item_freq[item] += 1

    print len(one_item_freq.keys())
    remove_items_without_min_support(one_item_freq, 0.1, transactions)
    print len(one_item_freq.keys())

    for k, v in one_item_freq.iteritems():
        print k + ': ' + str(v)

    # second step
    two_item_combinations = combinations(one_item_freq.keys(), 2)
    for idx, combination in enumerate(two_item_combinations):
        for transaction in transactions:
            if set(combination).issubset(transaction):
                two_item_freq[frozenset(set(combination))] += 1
        print idx

    for k, v in two_item_freq.iteritems():
        print str(k) + ': ' + str(v)
