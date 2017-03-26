'''
Decision trees
'''
from math import log


def divideset(rows, column, value):
    '''
    Divides a set on a specific column.
    Can handle numeric or nominal values
    '''
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] >= value
    else:
        split_function = lambda row: row[column] == value

    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)


def uniquecounts(rows):
    '''
    Create counts of possible results
    (the last column of each row is the result)
    '''
    results = {}
    for row in rows:
        lastr = row[-1]
        results[lastr] = results.get(lastr, 0) + 1
    return results


def entropy(rows):
    '''
    Entropy is the sum of p(x)log(p(x)) across all
    the different possible results
    '''
    log2 = lambda x: log(x) / log(2)
    results = uniquecounts(rows)
    ent = 0.0
    for key in results:
        valp = float(results[key] / len(rows))
        ent = ent - valp * log2(valp)
    # print('entropia for rows %s results %s: %s' % (len(rows), results, ent))
    return ent


class Decisionnode:
    def __init__(self, col=-1, value=None, results=None, trueb=None, falseb=None):
        self.col = col
        self.value = value
        self.results = results
        self.trueb = trueb
        self.falseb = falseb


def buildtree(rows, scoref=entropy):
    '''
    rows is the set, either whole dataset or part of it in the recursive call,
    coref is the method to measure heterogeneity. By default it's entropy.
    '''
    if len(rows) == 0:
        return Decisionnode()
    current_score = scoref(rows)
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
        # print('Edo colval: %s' % column_values)
        for value in column_values:
            set1, set2 = divideset(rows, col, value)
            psize = float(len(set1)) / len(rows)
            gain = current_score - psize * scoref(set1) - (1 - psize) * scoref(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)
    if best_gain > 0:
        true_branch = buildtree(best_sets[0])
        false_branch = buildtree(best_sets[1])
        return Decisionnode(col=best_criteria[0],
                            value=best_criteria[1],
                            trueb=true_branch,
                            falseb=false_branch
                           )
    else:
        return Decisionnode(results=uniquecounts(rows))


def prn(tree):
    print(tree.col)
    print(tree.value)
    print(tree.results)
    print("")
    print(tree.tb.col)
    print(tree.tb.value)
    print(tree.tb.results)
    print("")
    print(tree.tb.tb.col)
    print(tree.tb.tb.value)
    print(tree.tb.tb.results)
    print("")
    print(tree.tb.fb.col)
    print(tree.tb.fb.value)
    print(tree.tb.fb.results)


def printtree(tree, indent=''):
    if tree.results != None:
        print(str(tree.results))
    else:
        #print(tree.col)
        print(str(tree.col) + ':' + str(tree.value) + '? ')
        # Print the branches
        print(indent + 'T->', end=" ")
        printtree(tree.trueb, indent + '  ')
        print(indent + 'F->', end=" ")
        printtree(tree.falseb, indent + '  ')


def classify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.trueb
            else:
                branch = tree.falseb
        else:
            if v == tree.value:
                branch = tree.trueb
            else:
                branch = tree.falseb
        return classify(observation, branch)


if __name__ == '__main__':
    TIT = ['Xora', 'Poli', 'Epaggelma', 'Fylo']
    ASET = [['Greece', 'athens', 'logistis', 'male'],
            ['Greece', 'athens', 'oikiaka', 'female'],
            ['Greece', 'athens', 'oikiaka', 'shemale'],
            ['Greece', 'patra', 'oikiaka', 'female'],
            ['France', 'paris', 'oikiaka', 'shemale'],
            ['Germany', 'krapa', 'programmer', 'male'],
            ['Italy', 'rome', 'prorammer', 'female']]
    #AS1, AS2 = divideset(ASET, 3, 20)
    #print(entropy(AS1), entropy(AS2))
    my_data = [ ['slashdot','USA','yes',18,'None'],
                ['google','France','yes',23,'Premium'],
                ['digg','USA','yes',24,'Basic'],
                ['kiwitobes','France','yes',23,'Basic'],
                ['google','UK','no',21,'Premium'],
                ['(direct)','New Zealand','no',12,'None'],
                ['(direct)','UK','no',21,'Basic'],
                ['google','USA','no',24,'Premium'],
                ['slashdot','France','yes',19,'None'],
                ['digg','USA','no',18,'None'],
                ['google','UK','no',18,'None'],
                ['kiwitobes','UK','no',19,'None'],
                ['digg','New Zealand','yes',12,'Basic'],
                ['slashdot','UK','no',21,'None'],
                ['google','UK','yes',18,'Basic'],
                ['kiwitobes','France','yes',19,'Basic']]
    tree = buildtree(my_data)
    printtree(tree)
    print(classify(['google', 'USA', 'yes', 46], tree))
