#!usr/bin/env python
# -*- coding: utf-8 -*-
from Fetcher.functions import *
"""main entry point for Fetcher

`__main__.py`を書くとすると、パッケージを(import用のモジュールではなく)
巨大なスクリプトとして実行した場合の挙動を定義することができます。

`python Fetcher`を実行してみましょう。

モジュール内のそれぞれのファイルで`if __name__ == '__main__'`を定義すると
それぞれのファイルをスクリプトとして用いることができますが、テスト以外にこれ
を用いることはアンチパターンです。
"""

if __name__ == '__main__':
    crowl("https://ja.wikipedia.org/wiki/Pok%C3%A9mon_GO", degree=2)
    with open("result.csv", "w") as fh:
        for info in INFOS:
            fh.write(",".join([info.url, str(info.degree), info.body, "\n"]))
