import numpy as np
import re
import pandas as pd
import csv

def code2str(line,flag):
    code_list = []
    smb_list = ['{','}',';',',']
    error_list = ['exit', 'abort', 'cleanupandexit']
    value_list = ['=','+=','-=','/=','%=','<<=','>>=','&=','^=','/=']

    # return or goto
    if 'return' in line or 'goto' in line:
        line_list = line.split()
        # if len(line_list) < 3:
        #     for i in line_list:
        #         code_list.append(i.strip(';'))

        # return code_list, flag

    # get rid of comment
    if '/*' in line or '*/' in line or '//' in line:
        return code_list, flag

    # printf in 2 lines
    if 'printf' not in line and flag == 0:
        line_list = line.split()
    elif 'printf' in line:
        for i in line:
            if i == '(':
                flag += 1
            elif i == ')':
                flag -= 1
        line_list = line.split('(', 1)
        line_list[0] = line_list[0].strip('\t').strip('\n')
        line_list[1] = 'message'
    elif 'printf' not in line and flag !=0:
        for i in line:
            if i == '(':
                flag += 1
            elif i == ')':
                flag -= 1
        line_list = []

    # assign value
    sign = []
    idx = []
    for i in value_list:
        if i in line_list:
            sign.append(i)
            idx.append(line_list.index(i))
    if idx != [] and idx[0] == 1:
        line_list3 = line.split(sign[0],1)
        code_list.append(sign[0])

        # handle polynomial
        line_list3_cp = line_list3.copy()
        for sl in line_list3:
            if '/' in sl:
                code_list.append('/')
                for i in sl.split('/'):
                    if '+' in i:
                        code_list.append('+')
                        for j in i.split('+'):
                            line_list3_cp.append(j.strip('\t\n; ()'))
                    elif '-' in i:
                        code_list.append('-')
                        for j in i.split('-'):
                            line_list3_cp.append(j.strip('\t\n; ()'))
                    else:
                        line_list3_cp.append(i.strip('\t\n; '))

            elif '*' in sl and '-' not in sl and '+' not in sl:
                code_list.append('*')
                for i in sl.split('*'):
                    line_list3_cp.append(i.strip('\t\n; '))

            elif '+' in sl :
                code_list.append('+')
                for i in sl.split('+'):
                    line_list3_cp.append(i.strip('\t\n; '))
                    if '*' in i:
                        code_list.append('*')
                        for j in i.split('*'):
                            line_list3_cp.append(j.strip('\t\n; '))
            elif '-' in sl:
                code_list.append('-')
                for i in sl.split('-'):
                    line_list3_cp.append(i.strip('\t\n; '))
                    if '*' in i:
                        code_list.append('*')
                        for j in i.split('*'):
                            line_list3_cp.append(j.strip('\t\n; '))

            elif '&' in sl:
                code_list.append('&')
                for i in sl.split('&'):
                    line_list3_cp.append(i.strip('\t\n; '))

        for slice2 in line_list3_cp:
            if '(' not in slice2:
                if '?' in slice2:
                    code_list.append('?')
                code_list.append(slice2.strip('\t\n; ()?'))

            elif '(' in slice2 and '+' not in slice2 and '-' not in slice2 and '*' not in slice2 and '&' not in slice2:
                left = 0
                right = 0
                for i in slice2:
                    if i == '(':
                        left += 1
                    elif i == ')':
                        right += 1
                if left == right:
                    code_list.append(slice2.strip(' \t\n;'))
                    for i in slice2.split('('):
                        if slice2.index(i) != 0:
                            code_list.append(i.strip('\t\n; ()'))
                if slice2[0] != '(':
                    code_piece = slice2.split('(')
                    if '?' in code_piece[0]:
                        code_list.append('?')
                    code_list.append(code_piece[0].strip('\t\n; ()?'))
                else:
                    code_list.append(slice2.strip('\t\n; ()?'))


        code_list = handle_special(code_list)

        return code_list,flag


    # operate value
    if '++' in line and line.strip('\t\n ')[0] == '+':
        code_list.append('++')
        code_list.append(line.strip('\t').strip('\n').strip('++').strip(';'))

        code_list = handle_special(code_list)
        return code_list, flag
    elif '--' in line and line[0] == '-':
        code_list.append('--')
        code_list.append(line.strip('\t').strip('\n').strip('--').strip(';'))

        code_list = handle_special(code_list)
        return code_list, flag

    # get the element based on some rules
    for slice1 in line_list:
        if '(' not in slice1 and slice1 not in smb_list and ')' not in slice1:
            if slice1 != ':':
                code_list.append(slice1.strip(':').strip(';').strip(','))
            else:
                code_list.append(':')
        elif '(' in slice1 and ')' in slice1 and slice1[0] != '(' and slice1.split('(')[0] not in error_list:
            left = 0
            right = 0
            for i in slice1:
                if i == '(':
                    left += 1
                elif i == ')':
                    right += 1
            tmp = rreplace(slice1,')',' ',right - left)
            code_list.append(tmp.strip(';}\t\n '))
            line_list1 = slice1.split('(')
            for i in line_list1:
                code_list.append(i.strip(';}\t\n() '))
        elif '(' in slice1:
            line_list2 = slice1.split('(')

            # get special exit code
            if line_list2[0] in error_list:
                code_list.append(slice1.strip(';').strip('}').strip(','))
            else:
                for i in line_list2:
                    if '!' in i:
                        code_list.append('!')
                        code_list.append(i.strip(')').strip('!').strip(','))
                    elif i != '' and '!' not in i:
                        code_list.append(i.strip(')').strip(','))
        elif ')' in slice1:
            if '!' in slice1:
                code_list.append('!')
                code_list.append(slice1.strip(')!; '))
            else:
                code_list.append(slice1.strip('); '))

    code_list = handle_special(code_list)

    return code_list,flag

def handle_special(code_list):
    # special situation: ['.','*','&']
    temp_code_list = code_list.copy()
    for p in code_list:
        p = p.strip()
        if p != '' and '.' in p and len(p) > 1 and '0' not in p and '-' not in p and '(' not in p and ')' not in p:
            p_list = p.split('.')
            for i in p_list:
                temp_code_list.append(i.strip())
        if p != '' and p[0] == '*' and len(p) > 1:
            temp_code_list.append('*')
            temp_code_list.append(p.strip('*').strip())
        if p != '' and p[0] == '&' and p != '&&' and len(p) > 1:
            temp_code_list.append('&')
            temp_code_list.append(p.strip('&').strip())
        if '[' in p:
            p_list = p.split('[')
            temp_code_list.append(p_list[0].strip('&').strip('*').strip())
        if '->' in p:
            p_list = p.split('->')
            temp_code_list.append('->')
            for i in p_list:
                temp_code_list.append(i.strip(' '))
        if ',' in p and '(' not in p:
            p_list = p.split(',')
            for i in p_list:
                temp_code_list.append(i.strip(' '))
    return temp_code_list

def rreplace(self, old, new, *max):
    count = len(self)
    if max and str(max[0]).isdigit():
        count = max[0]
    while count:
        index = self.rfind(old)
        if index >= 0:
            chunk = self.rpartition(old)
            self = chunk[0] + new + chunk[2]
        count -= 1
    return self




def getCodeList(list1,list2):
    for i in list2:
        if i != '' and i != ';' and i not in list1:
            list1.append(i)
    return list1


# Step 1: Tokenize a sentence
def word_extraction(sentence):
    # 提取句子中的词们
    words = sentence.split()
    stop_words = ['{','}','(',')']
    cleaned_text = [w.lower() for w in words if not w in stop_words]
    return cleaned_text


# Step 2：Apply tokenization to all sentences
def tokenize(sentences):
    # 对所有句子做 step1,生成词表
    words = []
    for sentence in sentences:
        w = word_extraction(sentence)
        words.extend(w)
    words = sorted(list(set(words)))
    return words


# Step 3: Build vocabulary and generate vectors
def generate_bow(allsentences):
    vocab = tokenize(allsentences)
    print("Word List for Document \n{0} \n".format(vocab))
    for sentence in allsentences:
        words = word_extraction(sentence)
        bag_vector = np.zeros(len(vocab))
        for w in words:
            for i, word in enumerate(vocab):
                if word == w:
                    bag_vector[i] += 1

        print("{0}\n{1}\n".format(sentence, np.array(bag_vector)))

if __name__ == "__main__":
    f = open('conStatement_code.txt', 'r')
    flag = 0
    code_list = []
    whole_code_list = []
    whole_code_dict = {}
    cnt = 0

    for line in f.readlines():
        if flag <1000:
            if line != '----------------------------------------------------------------------------------\n':
                code_list,cnt = code2str(line,cnt)
                # print('{} {}'.format(flag+1,code_list))

                whole_code_list = getCodeList(whole_code_list,code_list)
            flag +=1
    print(len(whole_code_list))
    print(whole_code_list)
    f.close()

    for i in whole_code_list:
        whole_code_dict[i] = 0

    temp_dict = whole_code_dict.copy()
    # print(whole_code_dict)

    key_list = []
    for i in whole_code_dict.keys():
        key_list.append(i)
    # with open("test.csv", "w") as csvfile:
    #     writer = csv.writer(csvfile)
    #
    #     writer.writerow(key_list)

    flag1 = 0
    flag2 = 0

    csv_list = [key_list]
    line_list = []

    f = open('conStatement_code.txt', 'r')
    for line in f.readlines():
        if flag1 < 100000:
            if line != '----------------------------------------------------------------------------------\n':
                code_list, cnt = code2str(line, cnt)
                for i in code_list:
                    if i in whole_code_dict.keys():
                        whole_code_dict[i] += 1
                flag2 += 1
            else:
                print('{} - {}: {}'.format(flag1-flag2, flag1, whole_code_dict))
                value_list = []
                for i in whole_code_dict.keys():
                    value_list.append(whole_code_dict[i])

                line_list.append('{} - {}'.format(flag1-flag2+1, flag1-1))

                csv_list.append(value_list)
                # with open("test.csv", "w") as csvfile:
                #     writer = csv.writer(csvfile)
                #     writer.writerow(value_list)

                for i in whole_code_list:
                    whole_code_dict[i] = 0
                flag2 = 0

            flag1 += 1

    with open("code2vec.csv", "w") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerows(csv_list)

    with open("vec2line", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['line number'])
        for i in line_list:
            writer.writerow([i])

    # print(len(whole_code_list))
    # print(whole_code_list)
    # w.close()
    f.close()

