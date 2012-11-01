# -*- coding: utf-8 -*-
from sys import exit, exc_info
from itertools import combinations
from collections import defaultdict
from time import clock


def load_data(file_name):
    try:
        with open(file_name) as f:
            content = f.readlines()
            f.close()
    except IOError as e:
        print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
        exit()
    except:
        print 'Unexpected error: ', exc_info()[0]
        exit()
    return content


def format_output(item_freq_dicts, rules, transactions):
    '''first round the values, then truncate
    '''
    for idx, item_freq in enumerate(item_freq_dicts):
        if len(item_freq) == 0:
            continue
        print 'Itemsets of size', idx + 1
        formatted_item_freq = []
        for item, v in item_freq.iteritems():
            support = float(v) / len(transactions)
            if item.__class__ == str:
                formatted_item_freq.append((item, round(support, 3)))
            elif item.__class__ == frozenset:
                formatted_item_freq.append((','.join(sorted(map(str, item))),
                                            round(support, 3)))
        sorted_item_freq = sorted(formatted_item_freq,
                                  key=lambda tup: (-tup[1], tup[0]))
        for item, sup in sorted_item_freq:
            print item, '{0:.3f}'.format(sup)

        print

    print 'RULES'
    formatted_rules = [(','.join(sorted(map(str, rule[0]))) + ' -> ' +
                        ','.join(sorted(map(str, rule[1]))),
                       round(acc, 3))
                       for rule, acc in rules]
    sorted_rules = sorted(formatted_rules, key=lambda tup: (-tup[1], tup[0]))
    for rule, acc in sorted_rules:
        print rule, '{0:.3f}'.format(acc)


def remove_items_without_min_support(item_freq, min_sup, transactions):
    for k, v in item_freq.items():
        if float(v) / len(transactions) < min_sup:
            del item_freq[k]


def self_join(list_of_sets, l):
    '''generates itemsets efficiently'''
    assert(all(len(item_set) == l for item_set in list_of_sets))
    new_list_of_sets = []
    first_l_features = defaultdict(list)
    for item_set in list_of_sets:
        # small cheat to make a list a hashable type XD
        l_feature = ''.join(sorted(item_set)[:l - 1])
        first_l_features[l_feature].append(item_set)
    '''example dict generated so far:
    {'hours=overtime': item
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


def gen_subsets_and_rules(item_freq, min_acc, item_freq_dicts):
    '''
    :param item_freq: itemsets of same lenght to be used for generating subsets
    :param min_acc: minimum accuracy
    :param item_freq_dicts: dictionaries of item_sets of all lengths
    '''
    rules = []
    for k, v in item_freq.iteritems():
        # building 1-consequent rule
        accurate_consequents = []
        for combination in combinations(k, 1):
            consequent = frozenset(combination)
            antecedent = k - consequent
            ant_len_item_freq = item_freq_dicts[len(antecedent) - 1]
            if len(antecedent) == 1:
                # the itemset of length one stores its keys as strings
                # rather than frozensets
                acc = float(v) / ant_len_item_freq[list(antecedent)[0]]
            else:
                acc = float(v) / ant_len_item_freq[antecedent]
            if acc >= min_acc:
                accurate_consequents.append(consequent)
                rules.append(((antecedent, consequent), acc))

        # two-item-itemsets, only produce 1-consequent rules
        if len(k) <= 2:
            continue

        # building (n+1)-consequent rules
        consequent_length = 2
        while(len(accurate_consequents) != 0 and consequent_length < len(k)):
            new_accurate_consequents = []
            for combination in combinations(accurate_consequents, 2):
                consequent = frozenset.union(*combination)
                if len(consequent) != consequent_length:
                    # combined itemsets must share n-1 common items
                    continue
                antecedent = k - consequent
                ant_len_item_freq = item_freq_dicts[len(antecedent) - 1]
                if len(antecedent) == 1:
                    # the itemset of length one stores its keys as strings
                    # rather than frozensets
                    acc = float(v) / ant_len_item_freq[list(antecedent)[0]]
                else:
                    acc = float(v) / ant_len_item_freq[antecedent]
                if acc >= min_acc:
                    new_accurate_consequents.append(consequent)
                    rules.append(((antecedent, consequent), acc))
            accurate_consequents = new_accurate_consequents
            consequent_length += 1

    return list(set(rules))


if __name__ == '__main__':
    min_sup = 0.3
    min_acc = 0.7
    t1 = clock()
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

    # generating rules
    rules = []
    for item_freq in list(reversed(item_freq_dicts))[:-1]:
        rules += gen_subsets_and_rules(item_freq, min_acc, item_freq_dicts)

    t2 = clock()
    print 'Time spent: ', round(t2 - t1, 3)
    format_output(item_freq_dicts, rules, transactions)
