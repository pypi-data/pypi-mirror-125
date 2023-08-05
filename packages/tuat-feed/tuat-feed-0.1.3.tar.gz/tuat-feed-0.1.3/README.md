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

`Post`の定義は