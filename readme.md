# jawiki検索エンジン

# requirements
- python3（3.5 >）
- [MeCab](https://taku910.github.io/mecab/)
- mecab-python3

## How to use
### 1
`tangoAnalysis.py` と `mojiAnalysis.py` をドキュメントのあるディレクトリで実行。
結果は新たなディレクトリ`outputTango/`と`outputMojiに/`格納される。
tangoは20分程度、mojiは２時間半程度？

### 2
前処理として`outputTango/`に `preProcessing.py` をコピーし実行。
検索エンジンを起動するために必要なdicts.jsonが作成される。
2分程度。

### 3
`outputTango/`ディレクトリ上で必要に応じて
TF/IDFの重み付けによる検索 `search_engine_tfidf.py` と
類似度による検索 `search_engine_vector.py` を使う。
毎回起動に30秒近くかかる。
起動が完了するまで待ち、検索したいワードを入力した後Enterで検索開始
AND検索したい場合は、「半角スペース(重要)」で区切って行う。

※1, 2の作業は一度のみやれば良い
