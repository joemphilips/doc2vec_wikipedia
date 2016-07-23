#!usr/bin/env python
# -*- coding: utf-8 -*-
"""main entry point for Fetcher

`__main__.py`を書くとすると、パッケージを(import用のモジュールではなく)
巨大なスクリプトとして実行した場合の挙動を定義することができます。

`python Fetcher`を実行してみましょう。

モジュール内のそれぞれのファイルで`if __name__ == '__main__'`を定義すると
それぞれのファイルをスクリプトとして用いることができますが、テスト以外にこれ
を用いることはアンチパターンです。
"""

if __name__ == '__main__':
    print("hoge")
