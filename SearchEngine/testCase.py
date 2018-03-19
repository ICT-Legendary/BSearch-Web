__author__ = 'admin'
import json
import random
basedir = '/home/polly/test/func_test_set' #'/home/polly/test/2017-01-06'
arr, dirarr = [], []
prefix = ['short', 'normal', 'exact', 'fuzzy', 'mix', 'boundry', 'except']
charset = ['0', '1', '.', '*', '%', '*', '#', '!', '~', '+', '-', '_', '+', '|', '`', 'a', 'b', 'c', 'd',
            'e', 'f', 'g', 'h', 'i', 'j','k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
            'x', 'y', 'z']
dirType = ['null', 'single', 'multi_brand', 'multi_deep', 'multi_mix', 'noexist']
null_dir = ['/test_null']
single_dir = ['/test_single']
mulitbrand_dir = ['/test_multi_brand', '/boundry', '/media', 'netpack']
multideep_dir = ['/test_multi_deep']
multimix_dir = ['/test_multi_mix']
noexist_dir = ['/exist']
AllDir = []
AllDir.append(null_dir)
AllDir.append(single_dir)
AllDir.append(mulitbrand_dir)
AllDir.append(multideep_dir)
AllDir.append(multimix_dir)
AllDir.append(noexist_dir)

for i in range(2,10):
    charset.append(str(i))
charlen = len(charset)
for pre in prefix:
    name = pre + "_string_set"
    dic = {}
    dic['set_name'] = name
    dic['set_return_code'] = 1
    if pre != 'except' and pre != 'fuzzy':
        dic['set_return_code'] = 0

    data_list = []
    if pre == 'short':
        data_list.append('..........')
        for i in range(0,10):
            l = random.randint(10,15)
            s = ""
            for j in range(0, l):
                idx = random.randint(0,2)
                s += charset[idx]
            data_list.append(s)
    elif pre == 'normal':
        for i in range(10):
            l = random.randint(100, 999)
            s = ''
            idx = random.randint(0,1)
            s += charset[idx]
            for j in range(0, l):
                idx = random.randint(0,2)
                s += charset[idx]
            data_list.append(s)
    elif pre == 'exact':
        for i in range(10):
            l = random.randint(10, 888)
            s = ''
            for j in range(0, l):
                idx = random.randint(0,1)
                s += charset[idx]
            data_list.append(s)
    elif pre == 'fuzzy':
          for i in range(10):
            l = random.randint(8, 555)
            s = ''
            for j in range(0, l):
                s += charset[2]
            data_list.append(s)
    elif pre == 'mix':
        for i in range(10):
            l = random.randint(10, 888)
            s = ''
            for j in range(0, l):
                idx = random.randint(0,5)
                s += charset[idx]
            data_list.append(s)
    elif pre == 'boundry':
         for i in range(5):
            l = random.randint(10, 888)
            s1 = ''
            for j in range(0, l):
                s1 += '0'
            data_list.append(s1)

            l = random.randint(10, 888)
            s2 = ''
            for j in range(0, l):
                s2 += '1'
            data_list.append(s2)
    elif pre == 'except':
        for i in range(10):
            l = random.randint(10, 150)
            s = ''
            for j in range(0, l):
                idx = random.randint(0, charlen-1)
                s += charset[idx]
            data_list.append(s)

    dic['set_data_list'] = data_list
    arr.append(dic)

strjson = json.dumps(arr)
print strjson
with open("search_string_list_set.json", "w+") as f:
    f.write(strjson)


typelen = len(dirType)
for i in range(0, typelen):
    l = len(AllDir[i])
    for j in range(0, l):
        dic = {}
        dic['directory_type'] = dirType[i]
        dic['directory_name'] = AllDir[i][j]
        dic['directory_return_code'] = 0
        if dirType[i] == 'noexist':
            dic['directory_return_code'] = 1
        dirarr.append(dic)
strjson = json.dumps(dirarr)
print len(dirarr), ' ',strjson




with open("directory_list.json", "w+") as f:
    f.write(strjson)