
import streamlit as st
import sqlite3
from datetime import datetime


# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="かんたんメモ",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# スマホ向けデザイン
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 800px;
}

h1 {
    font-size: 2rem !important;
}

h2 {
    font-size: 1.4rem !important;
}

h3 {
    font-size: 1.1rem !important;
}

/* ボタン */
.stButton button {
    min-height: 44px;
    border-radius: 10px;
}

/* スマホ */
@media (max-width: 600px) {

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    h1 {
        font-size: 1.7rem !important;
    }

    h2 {
        font-size: 1.3rem !important;
    }

    h3 {
        font-size: 1.1rem !important;
    }

    .stButton button {
        min-height: 46px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# データベース
# =========================================================

DB_NAME = "memo_app.db"


def get_connection():
    """
    SQLiteデータベースへ接続する
    """

    conn = sqlite3.connect(DB_NAME)

    # カラム名でデータを取得できるようにする
    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# データベース初期化
# =========================================================

def init_database():

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------------------------
    # メモ本体
    #
    # 今回はカテゴリーを完全に使わない
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # -----------------------------------------------------
    # メモ項目
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memo_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memo_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # -----------------------------------------------------
    # フリーメモ
    # -----------------------------------------------------

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
        SELECT
            id,
            title,
            created_at
        FROM memos
        ORDER BY id DESC
    """)

    result = cursor.fetchall()

    conn.close()

    return result


# =========================================================
# メモ項目取得
# =========================================================

def get_memo_items(memo_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            memo_id,
            item,
            created_at
        FROM memo_items
        WHERE memo_id = ?
        ORDER BY id ASC
    """, (memo_id,))

    result = cursor.fetchall()

    conn.close()

    return result


# =========================================================
# フリーメモ取得
# =========================================================

def get_free_memos():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            content,
            created_at
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

    # タイトルは入力された文字をそのまま保存
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

    # メモに紐づいている項目も削除
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

    # 項目も入力された文字をそのまま保存
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

    # 入力された文章をそのまま保存
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
# セッション状態
# =========================================================

# 現在開いているメモ
if "opened_memo_id" not in st.session_state:

    st.session_state.opened_memo_id = None


# =========================================================
# タイトル
# =========================================================

st.title("📝 かんたんメモ")

st.caption(
    "メモをタップすると項目を表示できます。"
)


# =========================================================
# 新しいメモを作成
# =========================================================

with st.expander(
    "➕ 新しいメモを作成",
    expanded=False
):

    with st.form(
        key="create_new_memo_form",
        clear_on_submit=True
    ):

        new_title = st.text_input(
            "メモのタイトル",
            placeholder="例：買い物リスト",
            key="new_memo_title"
        )

        create_button = st.form_submit_button(
            "＋ メモを作成",
            use_container_width=True
        )


    if create_button:

        # 入力された文字の前後にある
        # 不要な空白だけ削除
        title = new_title.strip()

        if title:

            create_memo(title)

            st.success(
                f"「{title}」を作成しました！"
            )

            st.rerun()

        else:

            st.warning(
                "メモのタイトルを入力してください。"
            )


# =========================================================
# 作成したメモ
# =========================================================

st.divider()

st.subheader("📋 作成したメモ")


memos = get_memos()


# =========================================================
# メモがない場合
# =========================================================

if not memos:

    st.info(
        "まだメモがありません。"
        "「新しいメモを作成」からメモを作ってください。"
    )


# =========================================================
# メモタイトルボタン
# =========================================================

else:

    # 2列で表示
    # スマホでもタイトルを見つけやすくする
    for i in range(
        0,
        len(memos),
        2
    ):

        row_memos = memos[
            i:i + 2
        ]

        cols = st.columns(2)


        for col, memo in zip(
            cols,
            row_memos
        ):

            with col:

                # -----------------------------------------
                # 現在開いているメモ
                # -----------------------------------------

                if (
                    st.session_state.opened_memo_id
                    == memo["id"]
                ):

                    button_text = (
                        f"🔽 {memo['title']}"
                    )

                else:

                    button_text = (
                        f"📝 {memo['title']}"
                    )


                # -----------------------------------------
                # タイトルボタン
                # -----------------------------------------

                if st.button(
                    button_text,
                    key=f"open_memo_{memo['id']}",
                    use_container_width=True
                ):

                    # すでに開いている場合
                    # → 閉じる
                    if (
                        st.session_state.opened_memo_id
                        == memo["id"]
                    ):

                        st.session_state.opened_memo_id = None

                    # 閉じている場合
                    # → 開く
                    else:

                        st.session_state.opened_memo_id = memo["id"]

                    st.rerun()


# =========================================================
# 選択したメモの中身
# =========================================================

if st.session_state.opened_memo_id is not None:

    # -----------------------------------------------------
    # 現在選択されているメモを取得
    # -----------------------------------------------------

    selected_memo = None


    for memo in get_memos():

        if (
            memo["id"]
            == st.session_state.opened_memo_id
        ):

            selected_memo = memo

            break


    # -----------------------------------------------------
    # メモが存在しない場合
    # -----------------------------------------------------

    if selected_memo is None:

        st.session_state.opened_memo_id = None

        st.rerun()


    else:

        st.divider()

        # =================================================
        # メモタイトル
        # =================================================

        st.subheader(
            f"📝 {selected_memo['title']}"
        )


        # =================================================
        # 項目追加
        # =================================================

        st.write("**項目を追加**")


        with st.form(
            key=f"add_item_form_{selected_memo['id']}",
            clear_on_submit=True
        ):

            item_col, add_col = st.columns(
                [5, 1]
            )


            # ---------------------------------------------
            # 項目入力
            # ---------------------------------------------

            with item_col:

                new_item = st.text_input(
                    "項目",
                    placeholder="例：牛乳",
                    label_visibility="collapsed",
                    key=f"item_input_{selected_memo['id']}"
                )


            # ---------------------------------------------
            # 追加ボタン
            # ---------------------------------------------

            with add_col:

                add_button = st.form_submit_button(
                    "＋",
                    use_container_width=True
                )


        # =================================================
        # 項目追加処理
        # =================================================

        if add_button:

            item = new_item.strip()

            if item:

                add_memo_item(
                    selected_memo["id"],
                    item
                )

                st.rerun()

            else:

                st.warning(
                    "項目を入力してください。"
                )


        # =================================================
        # 項目一覧
        # =================================================

        st.write("**項目一覧**")


        items = get_memo_items(
            selected_memo["id"]
        )


        if not items:

            st.caption(
                "まだ項目がありません。"
            )


        else:

            for item in items:

                item_col, delete_col = st.columns(
                    [5, 1],
                    vertical_alignment="center"
                )


                # -----------------------------------------
                # 項目
                # -----------------------------------------

                with item_col:

                    st.write(
                        f"・{item['item']}"
                    )


                # -----------------------------------------
                # 項目削除
                # -----------------------------------------

                with delete_col:

                    if st.button(
                        "✓",
                        key=f"delete_item_{item['id']}",
                        use_container_width=True
                    ):

                        delete_memo_item(
                            item["id"]
                        )

                        st.rerun()


        # =================================================
        # メモ削除
        # =================================================

        st.write("")


        if st.button(
            "🗑️ このメモを削除",
            key=f"delete_selected_memo_{selected_memo['id']}",
            use_container_width=True
        ):

            delete_memo(
                selected_memo["id"]
            )

            # 削除したメモを閉じる
            st.session_state.opened_memo_id = None

            st.rerun()


# =========================================================
# フリーメモ
# =========================================================

st.divider()


with st.expander(
    "✏️ フリーメモ",
    expanded=False
):

    st.caption(
        "タイトルや項目に分けず、自由に文章を保存できます。"
    )


    # =====================================================
    # フリーメモ入力
    # =====================================================

    with st.form(
        key="free_memo_form",
        clear_on_submit=True
    ):

        free_text = st.text_area(
            "自由にメモ",
            placeholder=(
                "ここに自由にメモできます。\n\n"
                "例：\n"
                "明日の会議で確認すること\n"
                "資料を確認する\n"
                "○○さんに連絡する"
            ),
            height=180,
            label_visibility="collapsed",
            key="free_memo_input"
        )


        save_button = st.form_submit_button(
            "💾 フリーメモを保存",
            use_container_width=True
        )


    # =====================================================
    # フリーメモ保存処理
    # =====================================================

    if save_button:

        content = free_text.strip()

        if content:

            create_free_memo(content)

            st.success(
                "フリーメモを保存しました！"
            )

            st.rerun()

        else:

            st.warning(
                "メモの内容を入力してください。"
            )


    # =====================================================
    # 保存済みフリーメモ
    # =====================================================

    free_memos = get_free_memos()


    if free_memos:

        st.write("**保存したフリーメモ**")


        for free_memo in free_memos:

            with st.container(
                border=True
            ):

                text_col, delete_col = st.columns(
                    [5, 1],
                    vertical_alignment="top"
                )


                # -----------------------------------------
                # フリーメモ内容
                # -----------------------------------------

                with text_col:

                    st.write(
                        free_memo["content"]
                    )

                    st.caption(
                        f"保存日時：{free_memo['created_at']}"
                    )


                # -----------------------------------------
                # フリーメモ削除
                # -----------------------------------------

                with delete_col:

                    if st.button(
                        "🗑️",
                        key=f"delete_free_{free_memo['id']}",
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
    "📝 かんたんメモ"
)

