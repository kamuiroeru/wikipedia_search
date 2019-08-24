# coding:utf-8
from time import time
from collections import defaultdict, Counter
from multiprocessing import Process
from os import mkdir
from glob import glob

try:
    mkdir("outputMoji")
except FileExistsError:
    pass

start_prog = time()
files = [f_list.strip(".txt") for f_list in glob("*.txt")]
doc_total = len(files)


def write_gram(dicDocuments, dicIndex, n):
    from math import log2
    print(str(n) + "-gram export")
    for loop, dicTF in dicDocuments.items():
        with open("outputMoji/" + str(loop) + "." + str(n) + "-gram", "w", encoding="utf-8") as f:
            for morph, tf in sorted(dicTF.items()):
                l = len(dicIndex[morph])
                w = tf * (log2(doc_total / l) + 1)
                f.write(u"{}\t{}\n".format(morph, w))


def write_index(dicIndex, n):
    with open("outputMoji/mt_index_." + str(n) + "-gram", "w", encoding="utf-8") as f1:
        for i, j in sorted(dicIndex.items()):
            f1.write(i + "\t:" + str(", ".join(sorted(j))) + "\n")


for n in range(1, 6):
    start_MeCab = time()

    # 0000.txtの '0000'を引数に与えると、TFを計算して、 k:v = 形態素: TF値 の dictを返す
    def calculateTF(loop: str) -> dict:
        with open(loop + ".txt", encoding="utf-8") as a_file:
            lists = [arg1.strip() for arg1 in a_file]

        word_total = 0
        dic_eachTF = defaultdict(int)
        for str2 in lists:
            word_total += max(0, len(str2) - n + 1)
            for i in range(0, len(str2) - n + 1):
                dic_eachTF[str2[i:i + n]] += 1

        # for k in dic_eachTF:
        #     dicIndex[k].add(loop)

        TFcheck = 0.0
        dicTF = defaultdict(float)
        for k, v in dic_eachTF.items():
            dicTF[k] = v / word_total
            TFcheck += v / word_total

        return dicTF

    from multiprocessing import Pool
    with Pool() as p:
        dicTFs = p.map(calculateTF, files)

    dicDocuments = {}
    for file, dicTF in zip(files, dicTFs):
        dicDocuments[file] = dicTF
    #       print(str(loop) + ".txt" + str(n) + "TF count= " + str(len(dicTF)) + " :" + str(TFcheck))
    print(str(n) + "-gram{}[sec]".format((time() - start_MeCab)))

    dicIndex = defaultdict(set)  # keyはngram、valueはそのngramが含まれている文書の集合
    for loop, loopDicTF in dicDocuments.items():
        for k in loopDicTF:
            dicIndex[k].add(loop)

    import pickle
    pickle.dump(dicIndex, open("outputMoji/mt_index_." + str(n) + "-gram", "wb"))

    start = time()
    process = [Process(target=write_gram, args=(dicDocuments, dicIndex, n)),
               Process(target=write_index, args=(dicIndex, n))]
    for p in process:
        p.start()
    print(str(n) + "-gram_index{0}[sec]".format((time() - start)))
for p in process:
    p.join()
print("END ALL{}[sec]".format((time() - start_prog)))
