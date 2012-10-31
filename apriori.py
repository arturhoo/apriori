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


def self_join(list_of_sets, l=2):
    '''generates itemsets efficiently'''
    assert(all(len(item_set) == l for item_set in list_of_sets))
    new_list_of_sets = []
    first_l_features = defaultdict(list)
    for item_set in list_of_sets:
        # small cheat to make a list a hashable type XD
        l_feature = ''.join(sorted(item_set)[:l - 1])
        first_l_features[l_feature].append(item_set)
    '''example dict generated so far:
    {'hours=overtime':
        [frozenset(['hours=overtime', 'sex=Male']),
         frozenset(['hours=overtime', 'salary<=50K']
    }
    '''
    for k, v in first_l_features.items():
        if len(v) < 2:
            del first_l_features[k]  # delete those that appear only once
        else:
            # generate the new itemsets
            for combination in combinations(v, 2):
                union = combination[0].union(combination[1])
                new_list_of_sets.append(union)
    return new_list_of_sets


if __name__ == '__main__':
    min_sup = 0.4
    content = load_data('data/census_mod.dat')
    item_freq_dicts = [defaultdict(int)]

    transactions = []
    for line in content:
        transactions.append(frozenset(line.strip().split()))

    # first step
    for transaction in transactions:
        for item in transaction:
            item_freq_dicts[0][item] += 1
    remove_items_without_min_support(item_freq_dicts[0], min_sup, transactions)

    # second step
    item_freq_dicts.append(defaultdict(int))
    two_item_combinations = combinations(item_freq_dicts[0].keys(), 2)
    for idx, combination in enumerate(two_item_combinations):
        for transaction in transactions:
            if set(combination).issubset(transaction):
                item_freq_dicts[1][frozenset(set(combination))] += 1
    remove_items_without_min_support(item_freq_dicts[1], min_sup, transactions)

    # next steps
    next_candidate_item_sets = self_join(item_freq_dicts[1].keys(),
                                         len(item_freq_dicts))
    while(len(next_candidate_item_sets) != 0):
        item_freq_dicts.append(defaultdict(int))
        for idx, item_set in enumerate(next_candidate_item_sets):
            for transaction in transactions:
                if item_set.issubset(transaction):
                    item_freq_dicts[-1][item_set] += 1

        remove_items_without_min_support(item_freq_dicts[-1], min_sup,
                                         transactions)
        next_candidate_item_sets = self_join(item_freq_dicts[-1].keys(),
                                             len(item_freq_dicts))
