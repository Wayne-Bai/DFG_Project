import numpy as np
import re

def code2str(line,flag):
    code_list = []
    smb_list = ['{','}',';',',']
    error_list = ['exit', 'abort', 'cleanupandexit']
    value_list = ['=','+=','-=','/=','%=','<<=','>>=','&=','^=','/=']

    # return or goto
    if 'return' in line or 'goto' in line:
        line_list = line.split()
        if len(line_list) < 3:
            for i in line_list:
                code_list.append(i.strip(';'))

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

            elif '*' in sl:
                code_list.append('*')
                for i in sl.split('*'):
                    line_list3_cp.append(i.strip('\t\n; '))

            elif '+' in sl:
                code_list.append('+')
                for i in sl.split('+'):
                    line_list3_cp.append(i.strip('\t\n; '))
            elif '-' in sl:
                code_list.append('-')
                for i in sl.split('-'):
                    line_list3_cp.append(i.strip('\t\n; '))

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
                    code_list.append(slice2.strip('\t\n; ()'))
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
    if '++' in line:
        code_list.append('++')
        code_list.append(line.strip('\t').strip('\n').strip('++').strip(';'))
    elif '--' in line:
        code_list.append('--')
        code_list.append(line.strip('\t').strip('\n').strip('--').strip(';'))

    # get the element based on some rules
    for slice1 in line_list:
        if '(' not in slice1 and slice1 not in smb_list and ')' not in slice1:
            if slice1 != ':':
                code_list.append(slice1.strip(':').strip(';').strip(','))
            else:
                code_list.append(':')
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
                code_list.append(slice1.strip(')').strip('!').strip(','))
            else:
                code_list.append(slice1.strip(')').strip(','))

    code_list = handle_special(code_list)

    return code_list,flag

def handle_special(code_list):
    # special situation: ['.','*','&']
    temp_code_list = code_list.copy()
    for p in code_list:
        p = p.strip()
        if p != '' and '.' in p and len(p) > 1 and '0' not in p:
            p_list = p.split('.')
            for i in p_list:
                temp_code_list.append(i.strip())
        if p != '' and p[0] == '*' and len(p) > 1:
            temp_code_list.append('*')
            temp_code_list.append(p.strip('*').strip())
        if p != '' and p[0] == '&' and len(p) > 1:
            temp_code_list.append('&')
            temp_code_list.append(p.strip('&').strip())
        if '[' in p:
            p_list = p.split('[')
            temp_code_list.append(p_list[0].strip('&').strip('*').strip())
    return temp_code_list



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
    cnt = 0
    for line in f.readlines():
        if flag <1000:
            if line != '----------------------------------------------------------------------------------\n':
                code_list,cnt = code2str(line,cnt)
                print('{} {}'.format(flag+1,code_list))
            flag +=1
    f.close()

