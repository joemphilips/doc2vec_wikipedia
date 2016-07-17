#!usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# setup.py はpythonパッケージのメタデータ等を記述するpythonのスクリプトです。

setup(
    name='', # パッケージ名
    description='', # パッケージの１行での説明
    version='0.0.1',
    url='https://github.com/',
    author='',
    author_email='',
    license='MIT', # ライセンスの明記は大事
    classifiers=[
        'Development Status :: 3 - Alpha',

        # どのpythonのバージョンで動作するか
        'Programming Language :: Python :: 3.4',
         # 複数書く場合は、全バージョンでのテストを実行しておくこと
        'Programming Language :: Python :: 3.5',
    ],

    keywords='', # PYPIでの検索時に用いられるキーワード

    # PIPYパッケージに含まれるディレクトリ名を明示する。
    # 通常、実行に必要なものだけ含める。
    # `find_packages`を使用すると、自動で`__init__.py`を探し
    # 出してくれるので便利
    packages=find_packages(exclude=['dist', 'docs', 'tests*']),

    # dependencyを書く。PIPY上にあるパッケージに限る。
    # requirements.txtを読み込んでもよいが、余計なものを含めないように注意
    # (requirements.txtは`pip freeze`コマンドで作成する。)
    install_requires=[],

    # PYPI以外の場所にdependencyがある場合、ここにリンクを書く
    dependency_links=[],

    # `setup.py test`の実行に必要なパッケージ
    tests_require=["doctest2"]

    # サンプルデータを含める場合、ここに書く。
    # package_data={
    #     'sample': ['package_data.dat'],
    # },
)

