# make trie of root
# Input word
# check if input is root
# check possible prefix matches if contains prefixes
# check possible suffix matches if contains suffixes
# case for both
import json
import pandas as pd

exceptions = [
    "हसाँइ",
    "जँड्याहा",
    ""
]


def merge_roots():
    file = '/data/root'
    file2 = '/Users/deepakpaudel/mycodes/NepaliNLP/Lemmatization/data/raw/my-roots.txt'
    with open(file, 'r') as infile:
        data = infile.readlines()
    with open(file2, 'r') as infile1:
        data2 = infile1.readlines()


    data_1 = dict()
    for d in data:
        dd = d.strip().split('|')
        if len(dd) > 1:
            data_1.update({dd[0]: dd[1].split(',')})
        else:
            data_1.update({dd[0]: []})

    for d in data2:
        dd = d.strip().split('|')
        if dd[0] in data_1:
            if len(dd) > 1:
                data_1.update({dd[0]: list(set(data_1.get(dd[0])+dd[1].split(",")))})
        else:
            if len(dd) > 1:
                data_1.update({dd[0]: dd[1].split(',')})
            else:
                data_1.update({dd[0]: []})
    return data_1
    for k, v in data_1.items():
        value = ','.join(v)
        if value:
            line = f'{k}|{value}\n'
        else:
            line = f'{k}\n'
        outfile.write(line)
    outfile.close()


def merge_dict_rules_root(data_merged):
    file = '/merged__root.txt'
    diction = '/Users/deepakpaudel/mycodes/NepaliNLP/ne_NP_dict/ne_NP_original.dic'
    with open(diction, 'r') as infiled:
        dictions = infiled.readlines()
    with open(file, 'r') as infile:
        data = infile.readlines()
    # dictions = [d.strip() for d in dictions]
    new_data = []
    n_data = dict()
    for d in dictions:
        d1 = d.strip().split('/')
        if len(d1) > 1 and d1[0] in data_merged:
            new_data.append(dict(word=d1[0], pos=data_merged.get(d1[0]), rules=d1[1]))
            n_data.update({d1[0]: d1[1]})
    print(len(new_data))
    print(len(n_data.keys()))
    new_data = list()
    for w, p in data_merged.items():
        d = dict(word=w, pos=','.join(p), rules=n_data.get(w, ''))
        new_data.append(d)
    print(len(new_data))
    df = pd.DataFrame(new_data)
    df.to_csv("./root_pos_rules.csv", encoding='utf-8', index=None)


def get_common_roots():
    file = '/data/root'
    file2 = '/Users/deepakpaudel/mycodes/NepaliNLP/my-roots.txt'
    diction = '/Users/deepakpaudel/mycodes/NepaliNLP/ne_NP_dict/ne_NP_original.dic'
    with open(diction, 'r') as infiled:
        dictions = infiled.readlines()
    with open(file, 'r') as infile:
        data = infile.readlines()
    with open(file2, 'r') as infile1:
        data2 = infile1.readlines()
    # pn = {d.strip() for d in data2 if len(d.strip().split('|'))>1 and "PN" in d.strip().split('|')[1]}
    # print(pn)
    # pn = {d.strip() for d in data if len(d.strip().split('|'))>1 and "PN" in d.strip().split('|')[1]}
    # print(pn)
    data_ = list()
    for d in data:
        if len(d.strip().split('|')) > 1:
            data_.extend(d.strip().split("|")[1].split(','))
    print(list(set(data_)))
    data_1 = {d.strip().split("|")[0] for d in data}
    data_d = {d.strip().split('/')[0] for d in dictions}
    data_2 = {d.strip().split("|")[0] for d in data2}
    common = data_1.intersection(data_2)
    # print(len(common))
    # print(common)
    common = data_1.intersection(data_d)
    common2 = data_2.intersection(data_d)
    print(len(common), len(common2))
# get_common_roots()
merge_dict_rules_root(merge_roots())