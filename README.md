# python1
tutorial for python level 1


# ファイルの説明
* `setup.py` ... インストール、テストなどの要件を定義するファイル。どのファイルを配布物に含めたいか、より詳細に指定する場合は`MANIFEST.in`という独自DSLで記述することになるが、はじめは必要ない。
* `.gitignore` ... はじめは[github推奨のもの](https://github.com/github/gitignore/blob/master/Python.gitignore)を使っておく。pythonにかぎらない。
* `LICENSE.txt` ... ライセンスの全文。今回は[MITライセンス](http://choosealicense.com/licenses/mit/)
* `Fetcher` ... スクリプト本体のディレクトリ。
 * `Fetcher/__init__.py` ... 中身


## 注意点

`mecab`は

```
sudo rpm -ivh http://packages.groonga.org/centos/groonga-release-1.1.0-1.noarch.rpm
sudo yum install mecab mecab-ipadic mecab-devel -y
```

で`mecab`コマンドを予めインストールしておく(上はcentosの場合)

[日本語wikiのdump](https://dumps.wikimedia.org/jawiki/latest/)
