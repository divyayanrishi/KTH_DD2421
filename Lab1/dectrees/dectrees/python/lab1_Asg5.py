import dtree as d
import monkdata as m
import drawtree_qt5 as drwt5

# Assignment 5 prep questions
def q5_buildTree(dataset, attributes, maxdepth=1000000):
    "Recursively build a decision tree"
    default = d.mostCommon(dataset)
    if maxdepth < 1:
        return d.TreeLeaf(default)
    a = d.bestAttribute(dataset, attributes)
    attributesLeft = [x for x in attributes if x != a]
    branches = [(v, q5_buildBranch(d.select(dataset, a, v), default, attributesLeft, maxdepth))
                for v in a.values]
    return d.TreeNode(a, dict(branches), default)

def q5_buildBranch(dataset, default, attributes, maxdepth):
    "Add branches/leaf nodes"
    if not dataset:
        return d.TreeLeaf(d.mostCommon(default))
    if d.allPositive(dataset):
        return d.TreeLeaf(True)
    if d.allNegative(dataset):
        return d.TreeLeaf(False)
    return q5_buildTree(dataset, attributes, maxdepth-1)

lvl2_tree = q5_buildTree(m.monk1, m.attributes, 2) # Build 2-level DT
id3_tree = d.buildTree(m.monk1, m.attributes, 2) # Build ID3 routine DT 
drwt5.drawTree(lvl2_tree)

# Assignment 5
monk1_tree = d.buildTree(m.monk1, m.attributes)
print("MONK1, "+str(d.check(monk1_tree, m.monk1test)))
print("MONK1 TRAINSET, "+str(d.check(monk1_tree, m.monk1)))

monk2_tree = d.buildTree(m.monk2, m.attributes)
print("MONK2, "+str(d.check(monk2_tree, m.monk2test)))
print("MONK2 TRAINSET, "+str(d.check(monk2_tree, m.monk2)))

monk3_tree = d.buildTree(m.monk3, m.attributes)
print("MONK3, "+str(d.check(monk3_tree, m.monk3test)))
print("MONK3 TRAINSET, "+str(d.check(monk3_tree, m.monk3)))
