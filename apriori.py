# -*- coding: utf-8 -*-
from sys import exit, exc_info
from itertools import combinations
from collections import defaultdict
from time import clock
from optparse import OptionParser


def parse_arguments(parser):
    '''parse the arguments provided in the command line'''
    parser.add_option('-i', '--input', type='string', help='input file',
                      dest='input')
    parser.add_option('-s', '--support', type='float', help='minimum support',
                      dest='support')
    parser.add_option('-c', '--confidence', type='float',
                      help='minimum confidence', dest='confidence')
    parser.add_option('-a', '--atm', type='float', help='minimum at-metric',
                      dest='atm')
    (options, args) = parser.parse_args()
    if not options.input:
        parser.error('Input filename not given')
    if not options.support:
        parser.error('Support not given')
    if not options.confidence:
        parser.error('Confidence not given')
    return(options, args)


def get_transactions_from_file(file_name):
    '''returns the transactions from a given file, where the items must be
    separated by spaces.

    :returns transactions: a list of transactions, where each transaction is a
        frozenset containing items
    '''
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


def print_results(itemsets_list, rules, transactions):
    '''prints the results of the algorithm according to the standard specified
    in the documentation of the task. The confidence values are first rounded
    and then truncated
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


def remove_itemsets_without_min_support(itemsets, min_sup, transactions,
                                        min_atm):
    '''remove the itemsets that don't have the minimum support and, if given,
    the minimum value for atm
    '''
    for itemset, freq in itemsets.items():
        if float(freq) / len(transactions) < min_sup:
            if min_atm is not None and len(itemset) >= 2:
                mul = 1.0
                for item in itemset:
                    mul *= itemsets_list[0][frozenset([item])]
                atm = pow(freq, len(itemset)) / mul
                if atm < min_atm:
                    del itemsets[itemset]
            if min_atm is None:
                del itemsets[itemset]


def generate_itemsets(itemsets_list, min_sup, min_atm):
    '''given the trivial itemsets of length 1, this function generates the
    following itemsets using self joins, and then eliminating the itemsets
    without the minimum support

    :param itemsets_list: a list containing only one element which, at this
        stage, is the dictionary of itemsets of length 1
    '''
    try:
        next_candidate_item_sets = self_join(itemsets_list[0])
    except IndexError:
        return
    while(len(next_candidate_item_sets) != 0):
        itemsets_list.append(defaultdict(int))
        for idx, item_set in enumerate(next_candidate_item_sets):
            for transaction in transactions:
                if item_set.issubset(transaction):
                    itemsets_list[-1][item_set] += 1

        remove_itemsets_without_min_support(itemsets_list[-1], min_sup,
                                            transactions, min_atm)
        try:
            next_candidate_item_sets = self_join(itemsets_list[-1])
        except IndexError:
            break


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


def build_one_consequent_rules(itemset, freq, itemsets_list):
    '''builds one-consequent rules based on an itemset and its frequency, but
    most importantly, it also generates the accurate consequents that will be
    used to generate the two-consequent rules. In other words "if one or other
    of the single-consequent rules does not hold, there is no point in
    considering the double-consequent one" [Witten et. al., Data mining :
    practical machine learning tools and techniques]

    :param itemset: an itemset
    :param freq: frequency of the above mentioned itemset
    :param itemsets_list: dictionaries of itemsets of all lengths
    '''
    accurate_consequents = []
    rules = []
    for combination in combinations(itemset, 1):
        consequent = frozenset(combination)
        antecedent = itemset - consequent
        ant_len_itemsets = itemsets_list[len(antecedent) - 1]
        conf = float(freq) / ant_len_itemsets[antecedent]
        if conf >= min_conf:
            accurate_consequents.append(consequent)
            rules.append(((antecedent, consequent), conf))
    return accurate_consequents, rules


def build_n_plus_one_consequent_rules(itemset, freq, accurate_consequents,
                                      itemsets_list):
    '''similarly to the build_one_consequent_rules method, this one generates
    the n plus one consequent rules, the same way the former method does

    :param itemset: an itemset
    :param freq: frequency of the above mentioned itemset
    :param accurate_consequents: the accurate consequents generated in the
        former method
    :param itemsets_list: dictionaries of itemsets of all lengths
    '''
    rules = []
    consequent_length = 2
    while(len(accurate_consequents) != 0 and
          consequent_length < len(itemset)):
        new_accurate_consequents = []
        for combination in combinations(accurate_consequents, 2):
            consequent = frozenset.union(*combination)
            if len(consequent) != consequent_length:
                # combined itemsets must share n-1 common items
                continue
            antecedent = itemset - consequent
            ant_len_itemsets = itemsets_list[len(antecedent) - 1]
            conf = float(freq) / ant_len_itemsets[antecedent]
            if conf >= min_conf:
                new_accurate_consequents.append(consequent)
                rules.append(((antecedent, consequent), conf))
        accurate_consequents = new_accurate_consequents
        consequent_length += 1
    return rules


def generate_rules(itemsets, min_conf, itemsets_list):
    '''
    :param itemsets: itemsets of same lenght to be used for generating subsets
    :param min_conf: minimum confidence
    :param itemsets_list: dictionaries of itemsets of all lengths
    :returns rules: list of rules in the form of
        [((antecedent, consequent), confidence), ...]
    '''
    rules = []
    for itemset, freq in itemsets.iteritems():
        accurate_consequents, new_rules = \
            build_one_consequent_rules(itemset, freq, itemsets_list)
        rules += new_rules
        # 2-item-itemsets only produce 1-consequent rules,
        # no need to go further with those
        if len(itemset) <= 2:
            continue

        rules += build_n_plus_one_consequent_rules(itemset, freq,
                                                   accurate_consequents,
                                                   itemsets_list)
    return list(set(rules))


if __name__ == '__main__':
    usage_text = 'Usage: %prog -s minsup -c minconf [-a minatm]'
    parser = OptionParser(usage=usage_text)
    (options, args) = parse_arguments(parser)
    min_sup = options.support
    min_conf = options.confidence
    min_atm = options.atm
    t1 = clock()

    transactions = get_transactions_from_file(options.input)
    itemsets_list = [defaultdict(int)]

    # generate itemsets of length 1
    for transaction in transactions:
        for item in transaction:
            itemsets_list[0][frozenset([item])] += 1
    remove_itemsets_without_min_support(itemsets_list[0], min_sup,
                                        transactions, min_atm)

    # generate itemsets of length > 1
    generate_itemsets(itemsets_list, min_sup, min_atm)

    # generating rules
    rules = []
    for itemsets in list(reversed(itemsets_list))[:-1]:
        rules += generate_rules(itemsets, min_conf, itemsets_list)

    t2 = clock()
    print_results(itemsets_list, rules, transactions)
