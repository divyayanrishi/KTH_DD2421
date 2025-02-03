#!/usr/bin/env python

import monkdata as m
import dtree
import random
import matplotlib.pyplot as plt
import numpy as np
import gussie_plotfuncs as gplt
import drawtree_qt5

def partition(data, fraction):
    ldata = list(data)
    random.shuffle(ldata)
    breakPoint = int(len(ldata) * fraction)
    return ldata[:breakPoint], ldata[breakPoint:]

def ans1():
    print("Entropy monk-1: " + str(dtree.entropy(m.monk1)))
    print("Entropy monk-2: " + str(dtree.entropy(m.monk2)))
    print("Entropy monk-3: " + str(dtree.entropy(m.monk3)))

def ans3():  
    print("Entropy monk-1:")
    for i in range(6):
        print("a" + str(i) + ": " + str(dtree.averageGain(m.monk1, m.attributes[i])))
    
    print("Entropy monk-2:")
    for i in range(6):
        print("a" + str(i) + ": " + str(dtree.averageGain(m.monk2, m.attributes[i])))
    
    print("Entropy monk-3:")
    for i in range(6):
        print("a" + str(i) + ": " + str(dtree.averageGain(m.monk3, m.attributes[i])))


def ans5_pre():
    '''
    tree = ans5_buildtree(m.monk1, m.attributes, 2)
    print("Train error monk-1: " + str(dtree.check(tree, m.monk1)))
    print("Test error monk-1: " + str(dtree.check(tree, m.monk1test)))
    '''
    t1=dtree.buildTree(m.monk1, m.attributes, 2)
    drawtree_qt5.drawTree(t1)
    '''
    print("Train error monk-1: " + str(dtree.check(t1, m.monk1)))
    print("Test error monk-1: " + str(dtree.check(t1, m.monk1test)))
    '''

def ans5_buildtree(dataset, attr, depth):
    # Check for default and depth
    default = dtree.mostCommon(dataset)
    if depth < 1:
        return dtree.TreeLeaf(default)
    # pick the attribute which gets the highest information gain once known (max of average gain for all attributes)
    a = dtree.bestAttribute(dataset, m.attributes)
    # make a list with remaining attributes
    atts_left = []
    for at in attr:
        if at != a:
            atts_left.append(at)
    branches = []
    for val in a.values:
        branches.append((val, ans5_build_branch(dtree.select(dataset, a, val), atts_left, depth, default)))
    return dtree.TreeNode(a, dict(branches), default)
    

def ans5_build_branch(dataset, attr, depth, default):
    # first check if we have anything left in set
    if not dataset:
        return dtree.TreeLeaf(dtree.mostCommon(default))
    if dtree.allPositive(dataset):
        return dtree.TreeLeaf(True)
    if dtree.allNegative(dataset):
        return dtree.TreeLeaf(False)
    return ans5_buildtree(dataset, attr, depth - 1)
    

def ans5():
    t1=dtree.buildTree(m.monk1, m.attributes)
    print("Train error monk-1: " + str(dtree.check(t1, m.monk1)))
    print("Test error monk-1: " + str(dtree.check(t1, m.monk1test)))

    t2=dtree.buildTree(m.monk2, m.attributes)
    print("Train error monk-2: " + str(dtree.check(t2, m.monk2)))
    print("Test error monk-2: " + str(dtree.check(t2, m.monk2test)))

    t3=dtree.buildTree(m.monk3, m.attributes)
    print("Train error monk-3: " + str(dtree.check(t3, m.monk3)))
    print("Test error monk-3: " + str(dtree.check(t3, m.monk3test)))

def ans7():
    fractions = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    #ans7_calc_plot(fractions, m.monk1, m.monk1test, "monk-1")
    x = fractions
    y = []
    var = []

    y1, var1 = ans7_calc_data(fractions, m.monk1, m.monk1test, "monk-1")
    y2, var2 = ans7_calc_data(fractions, m.monk2, m.monk2test, "monk-2")
    y3, var3 = ans7_calc_data(fractions, m.monk3, m.monk3test, "monk-3")
    y = [y1, y2, y3]
    var = [var1, var2, var3]
    legend = ["monk-1", "monk-2", "monk-3"]
    gplt.make_plot_mult_series(x, y, 'Test error mean per fraction', 'Fraction', 'Test error mean', legend)
    gplt.make_plot_mult_series(x, var, 'Test error variance per fraction', 'Fraction', 'Test error variance', legend)
    plt.show()

    
      

def ans7_calc_data(fractions, monkdata, monktest, monkname):
    num_vals = 100
    ## x-axis, fractions
    x = fractions
    y = []
    var = []
    # Add all data points
    for frac in fractions:
        data = [] 
        for i in range(num_vals):
            data.append(make_pruned_calc(frac, monkdata, monktest))
        # Calculate mean and add to y-axis
        y.append(np.mean(data))
        # Calculate variance and add to variance
        var.append(np.var(data))
    return y, var

def make_pruned_calc(frac, data, testdata):
    # Do the partition
    monktrain, monkval = partition(data, frac)
    # Build the tree
    t=dtree.buildTree(monktrain, m.attributes)
    # Prune once
    final_tree, did_prune = prune_once(t, monkval)
    # Continue pruning as long as validation error does not increase
    while did_prune:
        final_tree, did_prune = prune_once(final_tree, monkval)
    # Calculate and return test error
    return dtree.check(final_tree, testdata)

def prune_once(tree, monkval):
    new_tree = tree
    new_val_check = dtree.check(tree, monkval)
    did_prune = False
    list_pruned = dtree.allPruned(tree)
    for pruned in list_pruned:
        pruned_val_check = dtree.check(pruned, monkval)
        # If pruned tree is not worse than old tree
        if(pruned_val_check > new_val_check):
            new_tree = pruned
            new_val_check = pruned_val_check
            did_prune = True
    return new_tree, did_prune


if __name__ == "__main__":
    ans5_pre()