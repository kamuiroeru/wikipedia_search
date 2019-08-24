from collections import defaultdict, Counter
from time import time
import pickle

start = time()
print("ファイル読込中")
dic = pickle.load(open('morphToDoc.pkl', 'rb'))
dicdoc = pickle.load(open('dicdoc.pkl', 'rb'))
diclen = pickle.load(open('diclen.pkl', 'rb'))
print("読み込み時間{}[sec]".format(time() - start))


def search_engine(string):
    words = string
    if not (len(words) > 0):
        print("\n検索したい文字列を入力してください\n>>>", end="")
        words = input().split(" ")
        words = sorted(set(words))  # 半角スペース区切りでリストに
    else:
        words = string.split(" ")
    searchtime = time()
    dicwt = defaultdict(float)  # str(ドキュメントhas単語):float(そのドキュメントでの単語のwt)
    dicCostheta = defaultdict(float)  # str(ドキュメントhas単語):float(そのドキュメントと基準ドキュメントとの内積)
    tokens = []  # AND検索するときに検索ワードをlistに格納
    if len(words) == 1:  # 単体検索
        print("through single")
        tokens = [words[0]]  # 結果出力のため
        print(words[0])
        if dic.setdefault(words[0], []):  # 検索ワードが転置indexに含まれている(返り値が[]ではない)時True
            lines = dic[words[0]]
            for index in lines:
                dicwt[index] = dicdoc[index][words[0]]
        else:
            if words[0] != "":
                print(words[0] + "を含むものはありません")
            return 0
    else:
        documents = []
        index_list = []
        for s in words:
            if dic.setdefault(s, []):
                documents += dic[s]
                tokens.append(s)
            else:
                if s == "":
                    continue
                print(s + "を含むものはありません")
        for k, v in Counter(documents).items():
            if v > (len(tokens) - 1):
                index_list.append(k)
        for index in index_list:
            for t in tokens:
                dicwt[index] += dicdoc[index][t]
        if len(index_list) == 0:
            if len(tokens) != 0:
                print("と".join(tokens) + "を両方含むドキュメントは見つかりませんでした。\n個別に検索します。")
                for token in tokens:
                    search_engine(str(token))
            return 0
    doclines = list(sorted(dicwt.items(), key=lambda x: x[1], reverse=True))
    print(" ".join(tokens) + "は" + str([s[0] for s in doclines]).replace("'", "") + ".txtに含まれています。\n" + str(
        len(doclines)) + "個のドキュメント" + "\n検索時間{}[sec]".format(time() - searchtime))
    return 0


while True:
    search_engine("")
