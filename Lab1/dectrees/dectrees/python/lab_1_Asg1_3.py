from dtree import *
from monkdata import monk1, monk2, monk3, attributes

entropy1 = entropy(monk1)
entropy2 = entropy(monk2)
entropy3 = entropy(monk3)

print("Entropy for 1 is "+str(entropy3))

gain_1 = [0]*6
info_gain = 0
for i in range(6):
    info_gain = averageGain(monk1, attributes[i])
    gain_1[i] = info_gain
print(gain_1)

gain_vals_list = [0]*len(list(attributes[4].values))
for num, val in enumerate(attributes[4].values):
    subset = select(monk1, attributes[4], val)
    info_gain = [averageGain(subset, attributes[j]) for j in range(6)]
    gain_vals_list[num] = info_gain

print(gain_vals_list)

#a5=2
gain_vals_list = [0]*len(list(attributes[3].values))
for num, val in enumerate(attributes[3].values):
    subset = select(select(monk1, attributes[4], 2), attributes[3], val)
    info_gain = [averageGain(subset, attributes[j]) for j in range(6)]
    gain_vals_list[num] = info_gain
print(gain_vals_list)
mcom_a52 = mostCommon(select(monk1, attributes[4], 2))

#a5=3
gain_vals_list = [0]*len(list(attributes[5].values))
for num, val in enumerate(attributes[5].values):
    subset = select(select(monk1, attributes[4], 3), attributes[5], val)
    info_gain = [averageGain(subset, attributes[j]) for j in range(6)]
    gain_vals_list[num] = info_gain
print(gain_vals_list)
mcom_a53 = select(monk1, attributes[4], 3)

#a5=4
gain_vals_list = [0]*len(list(attributes[0].values))
for num, val in enumerate(attributes[0].values):
    subset = select(select(monk1, attributes[4], 4), attributes[0], val)
    info_gain = [averageGain(subset, attributes[j]) for j in range(6)]
    gain_vals_list[num] = info_gain
print(gain_vals_list)
mcom_a54 = mostCommon(select(monk1, attributes[4], 4))

subset_a51 = select(monk1, attributes[4], 1)


