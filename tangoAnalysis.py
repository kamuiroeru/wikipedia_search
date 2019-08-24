# ecoding:utf-8

import json
from multiprocessing import Process
from collections import defaultdict, Counter
from glob import glob
from time import time
from os import mkdir
from MeCab import Tagger
import MeCab

t = MeCab.Tagger("-F%f[6]\\t%m\\n -E\ ")
try:
    mkdir("outputTango")
except FileExistsError:
    pass

start_prog = time()
files = [f_list.strip(".txt") for f_list in glob("*.txt")]
doc_total = len(files)


def get_words(s):
    s = s.split("\t")
    if len(s) < 2:
        return ""
    return s[0] or s[1]


from math import log2

wwl = defaultdict(dict)
morphToDocument = {}  # 単語: 単語を含むドキュメントの集合
for n in range(1, 4):
    start_MeCab = time()


    def calculateTF(loop: str) -> dict:
        sentence = ""
        with open(loop + ".txt", encoding="utf-8") as a_file:
            lines = [list(filter(lambda str2: str2, [get_words(str2) for str2 in t.parse(line).split("\n")])) for line
                     in a_file]

        word_total = 0
        dic_eachTF = defaultdict(int)
        for str2 in lines:
            word_total += max(0, len(str2) - n + 1)
            for i in range(0, len(str2) - n + 1):
                dic_eachTF["".join(str2[i:i + n])] += 1

        TFcheck = 0.0
        dicTF = defaultdict(float)
        for k, v in dic_eachTF.items():
            dicTF[k] = v / word_total
            TFcheck += v / word_total

        return dict(dicTF)


    from multiprocessing import Pool

    with Pool() as p:
        dicTFs = p.map(calculateTF, files)

    dicDocuments = {}
    for file, dicTF in zip(files, dicTFs):
        dicDocuments[file] = dicTF

    dicIndex = defaultdict(set)  # keyはngram、valueはそのngramが含まれている文書の集合
    for loop, loopDicTF in dicDocuments.items():
        for k in loopDicTF:
            dicIndex[k].add(loop)

    morphToDocument.update({k: v for k, v in dicIndex.items() if not '!' in k})


    # d = {k: list(sorted(v) for k, v in dicIndex.items() if not '!' in k}
    # json.dump(d, open("outputTango/mt_index_" + str(n) + ".json", "w", encoding="utf-8"), ensure_ascii=False)


    def calculateWeight(loop: str, dicTF: dict) -> tuple:
        retDic = {}
        for morph, tf in sorted(dicTF.items()):
            l = len(set(dicIndex[morph]))
            w = tf * (log2(doc_total / l) + 1)
            retDic[morph] = w
        return loop, retDic


    with Pool() as p:
        weightsWithLoops = p.starmap(calculateWeight, sorted(dicDocuments.items()))

    for loop, dicWT in weightsWithLoops:
        wwl[loop].update(dicWT)

    print(str(n) + "-gram処理時間" + "{}[min]".format((time() - start_MeCab) / 60))

start = time()

import pickle

pickle.dump(wwl, open('./outputTango/wwl.pkl', 'wb'))
pickle.dump(morphToDocument, open('./outputTango/morphToDoc.pkl', 'wb'))
print("ファイル書き出し時間" + "{}[min]".format((time() - start) / 60))
print("〜完了〜 全処理時間" + "{}[min]".format((time() - start_prog) / 60))
