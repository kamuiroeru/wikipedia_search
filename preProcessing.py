from collections import defaultdict, Counter
from glob import glob
from time import time
from math import sqrt
import json
import pickle
from multiprocessing import Pool

# dic = defaultdict(list)  # str(単語):list(含まれているドキュメント ex[0000, 0032, 0043, ...])
# dicdoc = defaultdict(dict)  # str(ドキュメント名):dict(str(ドキュメントに含まれている単語):float(wt))
# diclen = defaultdict(float)  # str(ドキュメント名):float(|wt|)

start = time()


def calcNorm(loop: str, dicW: dict) -> tuple:
    return loop, sqrt(sum([w ** 2 for w in dicW.values()]))


weightWithLoops = pickle.load(open('../wwl.pkl', 'rb'))
with Pool() as p:
    diclen = {loop: norm for loop, norm in p.starmap(calcNorm, weightWithLoops.items())}
dicdoc = {loop: dicWeight for loop, dicWeight in weightWithLoops.items()}
# for loop, dicWeight in pickle.load(open('../wwl-{}gram.pkl'.format(n), 'rb')):
#     i += 1
#     sqr = 0.0
#     for morph, weight in dicWeight.items():
#         dicdoc[loop][morph] = weight
#         sqr += weight ** 2  # 単語ごとのwtを2乗して足し合わせる
#     diclen[loop] = sqrt(sqr)  # 足し合わせたsqrを√して長さを取得
#     if (i % 1000 == 0):
#         print(str(int(i / 1000)))
print("読み込み時間{}[sec]".format(time() - start))
import pickle

start = time()
pickle.dump(dicdoc, open('dicdoc.pkl', 'wb'))
pickle.dump(diclen, open('diclen.pkl', 'wb'))
print("書き込み時間{}[sec]".format(time() - start))
