import os

image_path = 'jasper-2.0.14'

def get_filelist(dir, Filelist):
    newDir = dir
    if os.path.isfile(dir):
        Filelist.append(dir)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_filelist(newDir, Filelist)
    return Filelist

def get_c_file(dir, Clist):
    for i in dir:
        if os.path.splitext(i)[-1] == '.c':
            Clist.append(i)

    return Clist

def get_conStatement_point(dir):
    for i in range(len(dir)):
        w = open('conStatement_point.txt', 'a')
        if i == 0:
            f = open(dir[i], 'r')
            flag = 1
            lines = f.readlines()
            for line in lines:
                line_list = line.split()
                if 'if' in line_list or 'switch' in line_list:
                    w.write(str(i))
                    w.write('\t')
                    w.write(dir[i])
                    w.write('\t')
                    w.write(str(flag))
                    w.write('\n')
                flag += 1

            f.close()
            w.close()

        else:
            f = open(dir[i], 'r')
            w = open('conStatement_point.txt', 'a')
            w.write('\n')
            flag = 1
            lines = f.readlines()
            for line in lines:
                line_list = line.split()
                if 'if' in line_list or 'switch' in line_list:
                    w.write(str(i))
                    w.write('\t')
                    w.write(dir[i])
                    w.write('\t')
                    w.write(str(flag))
                    w.write('\n')
                flag += 1

            f.close()
            w.close()

def get_conStatement_code(dir):
    for i in range(len(dir)):
        w = open('conStatement_code.txt', 'a')
        if i >= 0:
            f = open(dir[i], 'r')
            lines = f.readlines()
            smb = 0
            space = []
            for line in lines:
                line_list = line.split()
                if smb == 0:
                    if 'if' in line_list and '*/' not in line_list:
                        smb = 1
                        line_space1 = line.split('if')
                        space.append(line_space1[0])
                        w.write(line)
                    elif 'switch' in line_list and '*/' not in line_list:
                        smb = 1
                        line_space1 = line.split('switch')
                        space.append(line_space1[0])
                        w.write(line)
                else:
                    w.write(line)
                    if '}' in line_list and len(line_list) == 1:
                        line_space2 = line.split('}')
                        if space[0] == line_space2[0]:
                            w.write('\n')
                            w.write('----------------------------------------------------------------------------------')
                            w.write('\n')
                            smb = 0
                            space = []

            f.close()
            w.close()

if __name__ == '__main__':
    list = get_filelist(image_path, [])
    # print(len(list))
    # for e in list:
    #     print(e)

    c_list = get_c_file(list, [])


    # print(len(c_list))
    # for e in c_list:
    #     print(e)

    # get_conStatement_point(c_list)
    get_conStatement_code(c_list)