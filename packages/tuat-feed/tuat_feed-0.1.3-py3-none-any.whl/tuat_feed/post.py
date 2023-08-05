from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List


@dataclass(repr=True, eq=True)
class Attachment:
    """添付ファイルデータ"""

    name: str  # ファイル名
    url: str  # URL


@dataclass(repr=True)
class Post:
    """
    掲示板の投稿
    """

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

    @classmethod
    def parse_post(cls, post_raw: dict) -> Post:
        """取得された生データから投稿情報のクラスに変換します

        Parameters
        ----------
        post_raw : dict
            取得されたJSONのデータ

        Returns
        -------
        Post
            投稿情報
        """

        post_data_raw: dict[str, str] = post_raw["data"]

        # 投稿ID
        post_id = post_raw["id"]
        # タイトル
        title = post_data_raw.pop("タイトル")
        # 本文
        description = post_data_raw.pop("本文")
        # 最終更新日
        update_date_raw = post_data_raw.pop("最終更新日")
        update_date = datetime.strptime(update_date_raw[:-5], "%Y/%m/%d").date()
        # 公開期間
        show_date_raw = post_data_raw.pop("公開期間")
        show_date_start_raw, show_date_end_raw = show_date_raw.split(" 〜 ")
        show_date_start = datetime.strptime(show_date_start_raw[:-5], "%Y/%m/%d").date()
        show_date_end = datetime.strptime(show_date_end_raw[:-5], "%Y/%m/%d").date()
        # 担当者
        author = post_data_raw.pop("担当者")
        # 発信元
        origin = post_data_raw.pop("発信元")
        # カテゴリー
        category = post_data_raw.pop("カテゴリー")
        # 添付ファイル
        attachment_raw = (
            post_data_raw.pop("添付ファイル") if "添付ファイル" in post_data_raw else None
        )
        attachment = []
        if attachment_raw is not None:
            for s in attachment_raw.split("\n"):
                name, url = s[1:-1].split("](")
                attachment.append(Attachment(name=name, url=url))

        return Post(
            post_id=post_id,
            title=title,
            description=description,
            update_date=update_date,
            show_date_start=show_date_start,
            show_date_end=show_date_end,
            author=author,
            origin=origin,
            category=category,
            attachment=attachment,
            other=post_data_raw,
        )
