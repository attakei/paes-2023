:article:published_time: 2022-04-19
:article:modified_time: 2022-04-29

============
Sphinx拡張群
============

主に自身の需要のために作成した、単機能なSphinx拡張をまとめて紹介。

前提
====

PyPI上に公開しているとは限りません。
PyPI上にないものについては、GitHubリポジトリのREADME上で「 `--find-links` を使ったインストール」についての説明書きをしています。

紹介
====

sphinxcontrib-gtagjs
--------------------

:PyPI登録: 有

HTML生成時に、 ``gtag.js`` を利用したタグ埋め込みをするための拡張。

* https://pypi.org/project/sphinxcontrib-gtagjs
* https://github.com/attakei/sphinxcontrib-gtagjs

sphinxcontrib-oembed
--------------------

:PyPI登録: 無

``oembed`` というディレクティブを追加する拡張。
https://oembed.com/ 上で保存されているプロバイダー一覧をもとに、
指定したURLをもとにoembed向けのHTMLコンテンツを取得して、HTML生成時に出力します。

* https://github.com/attakei-lab/sphinxcontrib-oembed

sphinxcontrib-budoux
--------------------

:PyPI登録: 有

Googleが公開しているBudouXを利用した、Sphinx内タイトル向けに改行ポイントを挿入する拡張。
標準実装では `<wbr>` 要素+Styleを用いることで、実際の表示に対して適切なタイミイングで改行を実施します。

* https://pypi.org/project/sphinxcontrib-budoux
* https://github.com/attakei-lab/sphinxcontrib-budoux

sphinxcontrib-sass
------------------

:PyPI登録: 無

libsass-pythonを利用して、ビルダー実行タイミングでSASSをCSSにコンパイルする拡張。

* https://github.com/attakei-lab/sphinxcontrib-sass

sphinxcontrib-mixed-builder
---------------------------

:PyPI登録: 無

Sphinxの拡張ビルダー。
複数のHTML系ビルダーを協調させて、ドキュメントごとに生成するビルダーを振り分けられるようになります。

* https://github.com/attakei-lab/sphinxcontrib-mixed-builder
