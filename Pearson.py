import numpy as np
from scipy.stats import pearsonr
import csv
# n = 100
# x1 = np.random.random_integers(0,10,8000)
# print(x1)
# x2 = np.random.random_integers(0,10,8000)
# p12 = pearsonr(x1,x2)

vec_list = []

with open("code2vec.csv","r") as csvfile:
    reader = csv.reader(csvfile)
    #这里不需要readlines
    # flag = 0
    # for line in reader:
    #     line_new = []
    #     if flag < 100000 and flag > 0:
    #         for i in line:
    #             line_new.append(int(i))
    #         vec_list.append(line_new)
    #         print(line_new)
    #     flag += 1
    for line in reader:
        if 'switch' not in line:
            line_new = []
            for i in line:
                line_new.append(int(i))
            vec_list.append(line_new)
        # print(line_new)
print(len(vec_list))
final_list = []
csvfile = open("valuedic.csv", "w")
writer = csv.writer(csvfile)
writer.writerow(['line number'])
for i in range(len(vec_list)):
    if i+1 < len(vec_list):
        for j in range(i+1,len(vec_list)):
            value_dic = {}
            x1 = np.array(vec_list[i])
            x2 = np.array(vec_list[j])
            value_dic['1st vec'] = i + 1
            value_dic['2nd vec'] = j + 1
            p = pearsonr(x1, x2)
            value_dic['co'] = p[0]
            value_dic['p-value'] = p[1]
            for key,value in value_dic.items():
                writer.writerow([key,value])
