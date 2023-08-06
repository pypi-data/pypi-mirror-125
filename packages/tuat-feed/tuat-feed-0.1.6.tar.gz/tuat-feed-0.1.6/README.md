# (非公式)TUAT掲示板ライブラリ

## インストール
* `python` >= 3.7

```sh
$ pip install tuat-feed
```

## 使い方

```python
>>> import tuat_feed
>>> feed = tuat_feed.fetch()
>>> len(feed)
40
>>> feed[0]
Post(...)
```

### fetch
`fetch()`を使って投稿情報をダウンロードします。結果は`Post`の配列になっています。
### Post

`Post`の定義はかんたんに書くと次のようになっています。

```python
class Post:
    post_id: int  # 投稿ID（内部処理用）
    title: str  # タイトル
    description: str  # 本文
    update_date: date  # 最終更新日
    show_date_start: date  # 公開期間（開始）
    show_date_end: date  # 公開期間（終了）
    author: str  # 担当者
    origin: str  # 発信元
    category: str  # カテゴリー
    attachment: List[Attachment]  # 添付ファイル
    other: Dict[str, str]  # その他のフィールド
```

### Attachment

`Attachment`の定義はかんたんに書くと次のようになっています。

```python
class Attachment:
    name: str  # ファイル名
    url: str  # URL
```