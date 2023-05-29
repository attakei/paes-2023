# attakei pages

https://attakei.net のソース（予定）です。

## 公開目的

主に以下の3点を目的としています。

* サイト内の実装周りをポートフォリオ兼ねて公開する。
* 本人が気づかないTypoの類に修正PRをもらう。

## ローカルビルド時

```console
cp .env.example .env
pipenv install --dev
pipenv run python -m tasks.get_font resources/fonts
pipenv run make local
```
