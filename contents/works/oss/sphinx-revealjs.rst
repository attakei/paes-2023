:article:published_time: 2022-04-15
:article:modified_time: 2022-04-19

===============
sphinx-revealjs
===============

Sphinx拡張の一つで、reStructuredTextベースのSphinxドキュメントから
Reveal.js形式のプレゼンテーションを生成するビルダー。

動き
====

.. figure:: https://sphinx-revealjs.readthedocs.io/en/latest/_images/screenshot-sphinx.png

この形式のreSTファイルが、以下のようなプレゼンテーション形式として生成されます。

.. figure:: https://sphinx-revealjs.readthedocs.io/en/latest/_images/screenshot-revealjs.png


特徴
====

reStructuredTextの標準的な記法をそのまま変換可能
------------------------------------------------

``====`` などで表現するセクション構造をそのままReveal.jsのスタイルへ変換できるようになっています。
イメージとしては、Reveal.js同梱のMarkdownプラグインによるMarkdownファイルからの変換と同等の感覚です。

Pythonistaが親しんでいるreStructuredTextでかいたドキュメントをそのままプレゼンテーションにすることも出来ます。

HTML生成系のSphinx拡張をそのまま表現可能
----------------------------------------

``figure`` , ``code-block`` といったSphinx/docutils同梱のディレクティブだけでなく、
``sphinxcontrib.blockdiag`` などのような、追加ディレクティブによる記述も、
HTMLを出力するものであればそのまま出力可能です。

そのため、Sphinxが持つ総合的な表現力をプレゼンテーションへ活かせるようになっています。

外部リンク
==========

* `PyPI パッケージ <https://pypi.org/project/sphinx-revealjs/>`_
* `ドキュメント <https://sphinx-revealjs.readthedocs.io/>`_
* `デモプレゼンテーション <https://attakei.github.io/sphinx-revealjs/>`_
* `GitHub リポジトリ <https://github.com/attakei/sphinx-revealjs/>`_
