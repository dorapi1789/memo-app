import streamlit as st
import sqlite3
from datetime import datetime


# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="かんたんメモアプリ",
    page_icon="📝",
    layout="wide"
)


# =========================================================
# データベース
# =========================================================

DB_NAME = "memo_app.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():

    conn = get_connection()
    cursor = conn.cursor()

    # メモ本体
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # メモの項目
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memo_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memo_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # フリーメモ
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS free_memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_database()


# =========================================================
# メモ取得
# =========================================================

def get_memos():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, created_at
        FROM memos
        ORDER BY id DESC
    """)

    result = cursor.fetchall()

    conn.close()

    return result


def get_memo_items(memo_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, memo_id, item, created_at
        FROM memo_items
        WHERE memo_id = ?
        ORDER BY id ASC
    """, (memo_id,))

    result = cursor.fetchall()

    conn.close()

    return result


def get_free_memos():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, content, created_at
        FROM free_memos
        ORDER BY id DESC
    """)

    result = cursor.fetchall()

    conn.close()

    return result


# =========================================================
# メモ作成
# =========================================================

def create_memo(title):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memos (
            title,
            created_at
        )
        VALUES (?, ?)
    """, (
        title,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    memo_id = cursor.lastrowid

    conn.close()

    return memo_id


# =========================================================
# メモ削除
# =========================================================

def delete_memo(memo_id):

    conn = get_connection()
    cursor = conn.cursor()

    # 先にメモに紐づいている項目を削除
    cursor.execute("""
        DELETE FROM memo_items
        WHERE memo_id = ?
    """, (memo_id,))

    # メモ本体を削除
    cursor.execute("""
        DELETE FROM memos
        WHERE id = ?
    """, (memo_id,))

    conn.commit()
    conn.close()


# =========================================================
# 項目追加
# =========================================================

def add_memo_item(memo_id, item):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memo_items (
            memo_id,
            item,
            created_at
        )
        VALUES (?, ?, ?)
    """, (
        memo_id,
        item,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# =========================================================
# 項目削除
# =========================================================

def delete_memo_item(item_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM memo_items
        WHERE id = ?
    """, (item_id,))

    conn.commit()
    conn.close()


# =========================================================
# フリーメモ保存
# =========================================================

def create_free_memo(content):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO free_memos (
            content,
            created_at
        )
        VALUES (?, ?)
    """, (
        content,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# =========================================================
# フリーメモ削除
# =========================================================

def delete_free_memo(memo_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM free_memos
        WHERE id = ?
    """, (memo_id,))

    conn.commit()
    conn.close()


# =========================================================
# 画面
# =========================================================

st.title("📝 かんたんメモアプリ")

st.write(
    "買い物リスト、ToDo、仕事のメモなどをまとめて管理できます。"
)


# =========================================================
# 新しいメモを作る
# =========================================================

st.header("➕ 新しいメモを作成")


with st.form(
    key="create_new_memo_form",
    clear_on_submit=True
):

    title = st.text_input(
        "メモのタイトル",
        placeholder="例：買い物リスト",
        key="new_memo_title"
    )

    create_button = st.form_submit_button(
        "＋ メモを作成",
        use_container_width=True
    )


if create_button:

    title = title.strip()

    if title:

        # 新しいメモをSQLiteに保存
        create_memo(title)

        st.success(
            f"「{title}」を作成しました！"
        )

        # フォームの内容は clear_on_submit=True
        # によって自動的にクリアされる
        st.rerun()

    else:

        st.warning(
            "メモのタイトルを入力してください。"
        )


st.divider()


# =========================================================
# 作成したメモ
# =========================================================

st.header("📋 作成したメモ")


memos = get_memos()


if not memos:

    st.info(
        "まだメモがありません。"
        "上のフォームからメモを作成してください。"
    )


else:

    for memo in memos:

        # =================================================
        # 1つのメモ
        # =================================================

        with st.container(border=True):

            title_col, delete_col = st.columns(
                [5, 1],
                vertical_alignment="center"
            )


            # -------------------------------------------------
            # メモタイトル
            # -------------------------------------------------

            with title_col:

                st.subheader(
                    f"📌 {memo['title']}"
                )


            # -------------------------------------------------
            # メモ削除
            # -------------------------------------------------

            with delete_col:

                if st.button(
                    "🗑️ メモ削除",
                    key=f"delete_memo_{memo['id']}",
                    use_container_width=True
                ):

                    delete_memo(
                        memo["id"]
                    )

                    st.rerun()


            # -------------------------------------------------
            # 項目追加
            # -------------------------------------------------

            st.write("**項目を追加**")


            with st.form(
                key=f"add_item_form_{memo['id']}",
                clear_on_submit=True
            ):

                item_col, add_col = st.columns(
                    [5, 1]
                )


                with item_col:

                    new_item = st.text_input(
                        "項目",
                        placeholder="例：牛乳",
                        label_visibility="collapsed",
                        key=f"item_input_{memo['id']}"
                    )


                with add_col:

                    add_button = st.form_submit_button(
                        "＋ 追加",
                        use_container_width=True
                    )


                if add_button:

                    new_item = new_item.strip()

                    if new_item:

                        add_memo_item(
                            memo["id"],
                            new_item
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "項目を入力してください。"
                        )


            # -------------------------------------------------
            # 項目一覧
            # -------------------------------------------------

            items = get_memo_items(
                memo["id"]
            )


            if items:

                st.write("**項目一覧**")


                for item in items:

                    item_col, button_col = st.columns(
                        [5, 1],
                        vertical_alignment="center"
                    )


                    with item_col:

                        st.write(
                            f"・{item['item']}"
                        )


                    with button_col:

                        if st.button(
                            "✅ 完了・削除",
                            key=f"delete_item_{item['id']}",
                            use_container_width=True
                        ):

                            delete_memo_item(
                                item["id"]
                            )

                            st.rerun()


            else:

                st.caption(
                    "まだ項目がありません。"
                )


st.divider()


# =========================================================
# フリーメモ
# =========================================================

st.header("✏️ フリーメモ")

st.write(
    "タイトルや項目に分けず、自由に文章を書いて保存できます。"
)


with st.form(
    key="free_memo_form",
    clear_on_submit=True
):

    free_text = st.text_area(
        "自由にメモ",
        placeholder=(
            "例：\n"
            "明日の会議で確認すること\n"
            "・資料を確認\n"
            "・○○さんに連絡\n"
            "・次回の予定を決める"
        ),
        height=180,
        label_visibility="collapsed",
        key="free_memo_input"
    )


    save_button = st.form_submit_button(
        "💾 フリーメモを保存",
        use_container_width=True
    )


    if save_button:

        if free_text.strip():

            create_free_memo(
                free_text.strip()
            )

            st.success(
                "フリーメモを保存しました！"
            )

            st.rerun()

        else:

            st.warning(
                "メモの内容を入力してください。"
            )


# =========================================================
# 保存済みフリーメモ
# =========================================================

st.subheader("📚 保存したフリーメモ")


free_memos = get_free_memos()


if not free_memos:

    st.caption(
        "保存したフリーメモはここに表示されます。"
    )


else:

    for free_memo in free_memos:

        with st.container(border=True):

            text_col, delete_col = st.columns(
                [5, 1],
                vertical_alignment="top"
            )


            with text_col:

                st.write(
                    free_memo["content"]
                )

                st.caption(
                    f"保存日時：{free_memo['created_at']}"
                )


            with delete_col:

                if st.button(
                    "🗑️ 削除",
                    key=f"delete_free_memo_{free_memo['id']}",
                    use_container_width=True
                ):

                    delete_free_memo(
                        free_memo["id"]
                    )

                    st.rerun()


# =========================================================
# フッター
# =========================================================

st.divider()

st.caption(
    "📝 かんたんメモアプリ ｜ SQLiteでデータを保存しています"
)