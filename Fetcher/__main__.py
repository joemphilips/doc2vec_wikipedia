#!usr/bin/env python
# -*- coding: utf-8 -*-
from Fetcher.functions import *
import multiprocessing as mp
"""main entry point for Fetcher

`__main__.py`を書くとすると、パッケージを(import用のモジュールではなく)
巨大なスクリプトとして実行した場合の挙動を定義することができます。

`python Fetcher`を実行してみましょう。

モジュール内のそれぞれのファイルで`if __name__ == '__main__'`を定義すると
それぞれのファイルをスクリプトとして用いることができますが、テスト以外にこれ
を用いることはアンチパターンです。
"""


def write_to_file(outputdir, resultfilename, q):
    """
    Args:
        q: ``mp.queue``, which yields ``pageinfo`` object
    """
    with open(outputdir + resultfilename, "w") as fh:
        while True:
            info = q.get(timeout = 20)
            processed_text = extract_text(info.html)
            fh.write(",".join([info.url, str(info.degree), processed_text, "\n"]))

            # write raw html
            htmlfilepath = outputdir + info.url.split("/")[-1]
            with open(htmlfilepath + ".html", "w") as htmlfh:
                htmlfh.write(info.html)

if __name__ == '__main__':
    q = mp.Queue()
    p = mp.Process(target=write_to_file,
                   args=("/mnt/ebs/english/", "result2.csv", q))
    p.start()
    crowl("https://ja.wikipedia.org/wiki/Pok%C3%A9mon_GO",
          q,
          degree=2,
          lang="en")
    p.join()
