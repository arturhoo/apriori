# -*- coding: utf-8 -*-
from sys import exit, exc_info
from itertools import combinations
from collections import defaultdict
from pprint import pprint


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
    one_item_freq = defaultdict(int)
    two_item_freq = defaultdict(int)
    three_item_freq = defaultdict(int)
    four_item_freq = defaultdict(int)

    transactions = []
    for line in content:
        transactions.append(frozenset(line.strip().split()))

    for transaction in transactions:
        for item in transaction:
            one_item_freq[item] += 1

    print len(one_item_freq.keys())
    remove_items_without_min_support(one_item_freq, min_sup, transactions)
    print len(one_item_freq.keys())

    # second step
    two_item_combinations = combinations(one_item_freq.keys(), 2)
    for idx, combination in enumerate(two_item_combinations):
        for transaction in transactions:
            if set(combination).issubset(transaction):
                two_item_freq[frozenset(set(combination))] += 1

    print len(two_item_freq.keys())
    remove_items_without_min_support(two_item_freq, min_sup, transactions)
    print len(two_item_freq.keys())

    candidate_three_item_sets = self_join(two_item_freq.keys())

    # third step
    for idx, item_set in enumerate(candidate_three_item_sets):
        for transaction in transactions:
            if item_set.issubset(transaction):
                three_item_freq[item_set] += 1

    print len(three_item_freq.keys())
    remove_items_without_min_support(three_item_freq, min_sup, transactions)
    print len(three_item_freq.keys())

    candidate_four_item_sets = self_join(three_item_freq.keys(), 3)

    # third step
    for idx, item_set in enumerate(candidate_four_item_sets):
        for transaction in transactions:
            if item_set.issubset(transaction):
                four_item_freq[item_set] += 1

    print len(four_item_freq.keys())
    remove_items_without_min_support(four_item_freq, min_sup, transactions)
    print len(four_item_freq.keys())
