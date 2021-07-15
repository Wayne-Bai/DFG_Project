import numpy as np
import re

def code2str(line,flag):
    code_list = []
    smb_list = ['{','}',':',';',',']
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
    else:
        line_list = ['message']

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
        for slice2 in line_list3:
            if '(' not in slice2:
                code_list.append(slice2.strip('\t').strip('\n').strip(';'))
            else:
                code_piece = slice2.split('(')
                code_list.append(code_piece[0].strip('\t').strip('\n').strip(';'))
        return code_list,flag

    # get the element based on some rules
    for slice1 in line_list:
        if '(' not in slice1 and slice1 not in smb_list and ')' not in slice1:
            code_list.append(slice1.strip(':').strip(';'))
        elif '(' in slice1:
            line_list2 = slice1.split('(')

            # get special exit code
            if line_list2[0] in error_list:
                code_list.append(slice1.strip(';').strip('}'))
            else:
                for i in line_list2:
                    if '!' in i:
                        code_list.append('!')
                        code_list.append(i.strip(')').strip('!'))
                    elif i != '' and '!' not in i:
                        code_list.append(i.strip(')'))
        elif ')' in slice1:
            if '!' in slice1:
                code_list.append('!')
                code_list.append(slice1.strip(')').strip('!'))
            else:
                code_list.append(slice1.strip(')'))







    return code_list,flag

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
        if flag <20:
            if line != '----------------------------------------------------------------------------------\n':
                code_list,cnt = code2str(line,cnt)
                print(code_list)
            flag +=1
    f.close()

