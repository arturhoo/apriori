# -*- coding: utf-8 -*-
from sys import exit, exc_info


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


if __name__ == '__main__':
    content = load_data('data/census_mod.dat')
