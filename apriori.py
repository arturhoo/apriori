# -*- coding: utf-8 -*-
from sys import exit, exc_info
from itertools import combinations
from collections import defaultdict
from time import clock
from optparse import OptionParser


def prepare_arguments(parser):
    '''prepares the argumets for the script to run'''
    parser.add_option('-i', '--input', type='string', help='input file',
                      dest='input')
    parser.add_option('-s', '--support', type='float', help='minimum support',
                      dest='support')
    parser.add_option('-c', '--confidence', type='float',
                      help='minimum confidence', dest='confidence')
    (options, args) = parser.parse_args()
    if not options.input:   # if input is not given
        parser.error('Input filename not given')
    if not options.support:   # if support is not given
        parser.error('Support not given')
    if not options.confidence:   # if confidence is not given
        parser.error('Confidence not given')
    return(options, args)


def get_transactions_from_file(file_name):
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
    transactions = []
    for line in content:
        transactions.append(frozenset(line.strip().split()))
    return transactions


def format_output(itemsets_list, rules, transactions):
    '''first round the values, then truncate
    '''
    for idx, itemsets in enumerate(itemsets_list):
        if len(itemsets) == 0:
            continue
        print 'Itemsets of size', idx + 1
        formatted_itemsets = []
        for itemset, freq in itemsets.iteritems():
            support = float(freq) / len(transactions)
            formatted_itemsets.append((','.join(sorted(map(str, itemset))),
                                       round(support, 3)))
        sorted_itemsets = sorted(formatted_itemsets,
                                 key=lambda tup: (-tup[1], tup[0]))
        for itemset, support in sorted_itemsets:
            print itemset, '{0:.3f}'.format(support)

        print

    print 'RULES'
    formatted_rules = [(','.join(sorted(map(str, rule[0]))) + ' -> ' +
                        ','.join(sorted(map(str, rule[1]))),
                       round(acc, 3))
                       for rule, acc in rules]
    sorted_rules = sorted(formatted_rules, key=lambda tup: (-tup[1], tup[0]))
    for rule, acc in sorted_rules:
        print rule, '{0:.3f}'.format(acc)


def remove_items_without_min_support(itemsets, min_sup, transactions):
    for itemset, freq in itemsets.items():
        if float(freq) / len(transactions) < min_sup:
            del itemsets[itemset]


def generate_itemsets(itemsets_list):
    '''given the trivial itemsets of length 1, this function generates the
    following itemsets using self joins, and then eliminating the itemsets
    without the minimum support

    :param itemsets_list: a list containing only one element which is the
        dictionary of itemsets of length 1
    '''
    next_candidate_item_sets = self_join(itemsets_list[0])
    while(len(next_candidate_item_sets) != 0):
        itemsets_list.append(defaultdict(int))
        for idx, item_set in enumerate(next_candidate_item_sets):
            for transaction in transactions:
                if item_set.issubset(transaction):
                    itemsets_list[-1][item_set] += 1

        remove_items_without_min_support(itemsets_list[-1], min_sup,
                                         transactions)
        next_candidate_item_sets = self_join(itemsets_list[-1])


def self_join(itemsets):
    '''generates itemsets efficiently by selfjoining the itemsets

    :param itemsets: list of itemsets
    :returns new_itemsets: list of itemsets containing l+1 members
    '''
    itemsets = itemsets.keys()  # we are only interested on the itemsets
                                # themselves, not the frequencies
    k = len(itemsets[0])  # length of the itemsets
    # making sure all the itemsets have the same length
    assert(all(len(itemset) == k for itemset in itemsets))
    kmomo = build_k_minus_one_members_and_their_occurrences(itemsets, k)
    return generate_itemsets_from_kmomo(kmomo)


def build_k_minus_one_members_and_their_occurrences(itemsets, k):
    '''in order to self join the itemsets, they must be sorted in lexical
    order. Then, all the unique sets of k-1 members must be idenfified and
    and the itemsets of length k in which they appear, associated

    :param itemsets: list of itemsets
    :param k: length of the itemsets
    :returns k_minus_one_members_and_occurrences: dictionary where keys are
        k-1 members, and values are itemsets of length k, where the members in
        its key appear
    '''
    k_minus_one_members_and_occurrences = defaultdict(list)
    for itemset in itemsets:
        # small cheat to make a list a hashable type
        k_minus_one_members = ''.join(sorted(itemset)[:k - 1])
        k_minus_one_members_and_occurrences[k_minus_one_members].\
            append(itemset)
    return k_minus_one_members_and_occurrences


def generate_itemsets_from_kmomo(kmomo):
    '''here we identify pairs with the same first k-1 members and produce a new
    itemset of length k+1. Given the kmomo dictionary, this task is easy as we
    simply generate the combinations of size 2 of the associated itemsets where
    they appear

    :param kmomo: dictionary where keys are k-1 members, and values are
        itemsets of length k, where the members in its key appear
    :returns new_itemsets: list of itemsets containing k+1 members
    '''
    new_itemsets = []
    for k_minus_one_members, occurrences in kmomo.items():
        if len(occurrences) < 2:
            # delete those k_minus_one_members that have only one occurrence
            del kmomo[k_minus_one_members]
        else:  # generate the new itemsets
            for combination in combinations(occurrences, 2):
                union = combination[0].union(combination[1])
                new_itemsets.append(union)
    return new_itemsets


def gen_subsets_and_rules(itemsets, min_conf, itemsets_list):
    '''
    :param itemsets: itemsets of same lenght to be used for generating subsets
    :param min_conf: minimum confidence
    :param itemsets_list: dictionaries of item_sets of all lengths
    '''
    rules = []
    for k, v in itemsets.iteritems():
        # building 1-consequent rule
        accurate_consequents = []
        for combination in combinations(k, 1):
            consequent = frozenset(combination)
            antecedent = k - consequent
            ant_len_itemsets = itemsets_list[len(antecedent) - 1]
            acc = float(v) / ant_len_itemsets[antecedent]

            if acc >= min_conf:
                accurate_consequents.append(consequent)
                rules.append(((antecedent, consequent), acc))

        # 2-item-itemsets only produce 1-consequent rules,
        # no need to go further
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
                ant_len_itemsets = itemsets_list[len(antecedent) - 1]
                acc = float(v) / ant_len_itemsets[antecedent]
                if acc >= min_conf:
                    new_accurate_consequents.append(consequent)
                    rules.append(((antecedent, consequent), acc))
            accurate_consequents = new_accurate_consequents
            consequent_length += 1

    return list(set(rules))


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options]')
    (options, args) = prepare_arguments(parser)
    min_sup = options.support
    min_conf = options.confidence
    t1 = clock()

    transactions = get_transactions_from_file(options.input)
    itemsets_list = [defaultdict(int)]

    # generate itemsets of length 1
    for transaction in transactions:
        for item in transaction:
            itemsets_list[0][frozenset([item])] += 1
    remove_items_without_min_support(itemsets_list[0], min_sup, transactions)

    # generate itemsets of length > 1
    generate_itemsets(itemsets_list)

    # generating rules
    rules = []
    for itemsets in list(reversed(itemsets_list))[:-1]:
        rules += gen_subsets_and_rules(itemsets, min_conf, itemsets_list)

    t2 = clock()
    # print 'Time spent: ', round(t2 - t1, 3)
    format_output(itemsets_list, rules, transactions)
