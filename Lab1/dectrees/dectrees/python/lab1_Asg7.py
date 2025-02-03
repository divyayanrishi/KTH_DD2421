import dtree as d
import monkdata as m
import random
import matplotlib.pyplot as plt

#6,7
def partition(data, fraction):
    '''
    Method to return train and test dataset splitted by fraction value
    data -> Dataset to be used
    fraction -> partition float value
    '''
    ldata = list(data)
    random.shuffle(ldata)
    training_set_limit = int(len(ldata)*fraction)
    return ldata[:training_set_limit], ldata[training_set_limit:]

def eval_pruning(dataset, test_data, data_attributes, partitions=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8], iters=100):
    '''
    Method to evalute accuracy of pruned trees and return the best one
    dataset -> Dataset to be used for building and pruning DT
    test_data -> Test dataset to be used to measuring accuracy
    data_attributes -> Features of the dataset to decide splits in DT
    partitions -> Train/Validation split fractions
    '''
    # for the sake of computational complexity, we will run
    # 100 iterations on each paritiion
    acc_list = [[0]*len(partitions)]*2
    for idx, partition_val in enumerate(partitions):
        avg_error_1 = avg_error_2 = 0
        for _ in range(iters):
            dataset_train, dataset_val = partition(dataset, partition_val)
            dataset_tree = d.buildTree(dataset_train, data_attributes)
            pruned_trees = d.allPruned(dataset_tree)
            optimal_tree = dataset_tree
            optimal_accuracy = d.check(dataset_tree, dataset_val)
            for pruned_tree in pruned_trees:
                tree_accuracy = d.check(pruned_tree, dataset_val)
                if tree_accuracy > optimal_accuracy:
                    optimal_accuracy = tree_accuracy
                    optimal_tree = pruned_tree
            optimal_tree_test_accuracy = d.check(optimal_tree, test_data)
            original_tree_test_accuracy = d.check(dataset_tree, test_data)
            avg_error_1 += (1-optimal_tree_test_accuracy)
            avg_error_2 += (1-original_tree_test_accuracy)
        acc_list[0][idx] = avg_error_1/iters
        acc_list[1][idx] = avg_error_2/iters
    return acc_list

if __name__ == '__main__':
    partitions = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    monk1_tree = d.buildTree(m.monk1, m.attributes)
    pruned_acc_m1, original_acc_m1 = eval_pruning(m.monk1, m.monk1test, m.attributes, partitions=partitions)[0], \
        eval_pruning(m.monk1, m.monk1test, m.attributes)[1]

    monk3_tree = d.buildTree(m.monk3, m.attributes)
    pruned_acc_m3, original_acc_m3 = eval_pruning(m.monk3, m.monk3test, m.attributes, partitions=partitions)[0], \
        eval_pruning(m.monk3, m.monk3test, m.attributes)[1]
    
    plt.plot(partitions, pruned_acc_m1, label="MONK1 on Pruned tree")
    plt.plot(partitions, original_acc_m1, label="MONK1 on Original tree")
    # Use the same lines 48-49 to plot the error curve for MONK3
    plt.xlabel('partition fraction')
    plt.ylabel('error fraction')
    plt.legend(loc='upper right')
    plt.show()
