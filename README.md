# Apriori Algorithm

Artur Oliveira Rodrigues ; artur [at] dcc.ufmg.br

The documentation (in Portuguese) is located in the `doc` directory, and the
reference file is `doc/tp1.pdf`.


## Implementation

The algorithm was implemented in Python and its code can be found at
`apriori.py`.

The way the Apriori algorithm was implemeted allows the tuning of multiple
parameters, as follows:

    positional arguments:
      -i, --input         transactions file
      -s, --support       minimum support value [0, 1]
      -c, --confidence    minimum confidence value [0, 1]

    optional arguments:
      -a, --atm           minimum value for the atm metric [0, 1]
      -h, --help          show this help message and exit

Here is a sample parameters configuration:

    $ python apriori.py -i data/census_mod.dat -s 0.5 -c 0.7 -a 0.3

and here is the sample output (simplified for clarity):

    Itemsets of size 1
    country=United-States 0.897
    (...)
    workclass=Without-pay 0.000

    Itemsets of size 2
    country=United-States,race=White 0.788
    (...)
    edu_num=1,education=Preschool 0.002

    Itemsets of size 3
    country=United-States,race=White,salary<=50K 0.584
    (...)
    marital=Married-civ-spouse,race=White,relationship=Husband 0.365

    RULES
    edu_num=1 -> education=Preschool 1.000
    (...)
    country=United-States,workclass=Private -> race=White 0.880
    (...)
    age=middle-aged -> sex=Male 0.702
