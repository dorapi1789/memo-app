
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
# CSS
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


/* =====================================================
   メモタイトルボタン
   ===================================================== */

.stButton button {
    min-height: 44px;
    border-radius: 10px;
}


/* =====================================================
   項目行
   ===================================================== */

.item-row {
    display: flex;
    align-items: center;
    width: 100%;
    min-height: 44px;
    margin-bottom: 6px;
}


/* =====================================================
   スマホ
   ===================================================== */

@media (max-width: 600px) {

    .block-container {
        padding-left: 10px;
        padding-right: 10px;
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
        min-height: 44px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# データベース
# =========================================================

DB_NAME = "memo_app.db"


def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# データベース初期化
# =========================================================

def init_database():

    conn = get_connection()
    cursor = conn.cursor()


    # -----------------------------------------------------
    # メモ
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
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)


    # -----------------------------------------------------
    # 既存データに completed がない場合
    # -----------------------------------------------------

    cursor.execute("""
        PRAGMA table_info(memo_items)
    """)

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]


    if "completed" not in columns:

        cursor.execute("""
            ALTER TABLE memo_items
            ADD COLUMN completed INTEGER NOT NULL DEFAULT 0
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
# 項目取得
# =========================================================

def get_memo_items(memo_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            memo_id,
            item,
            completed,
            created_at
        FROM memo_items
        WHERE memo_id = ?
        ORDER BY completed ASC, id ASC
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


    # メモの項目を削除
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
            completed,
            created_at
        )
        VALUES (?, ?, 0, ?)
    """, (
        memo_id,
        item,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# =========================================================
# 項目の完了状態変更
# =========================================================

def update_item_completed(item_id, completed):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE memo_items
        SET completed = ?
        WHERE id = ?
    """, (
        1 if completed else 0,
        item_id
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
# セッション状態
# =========================================================

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
# 新しいメモ作成
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


                if st.button(
                    button_text,
                    key=f"open_memo_{memo['id']}",
                    use_container_width=True
                ):

                    if (
                        st.session_state.opened_memo_id
                        == memo["id"]
                    ):

                        st.session_state.opened_memo_id = None

                    else:

                        st.session_state.opened_memo_id = memo["id"]

                    st.rerun()


# =========================================================
# 選択したメモ
# =========================================================

if st.session_state.opened_memo_id is not None:

    selected_memo = None


    for memo in get_memos():

        if (
            memo["id"]
            == st.session_state.opened_memo_id
        ):

            selected_memo = memo

            break


    # -----------------------------------------------------
    # メモが削除されている場合
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


            with item_col:

                new_item = st.text_input(
                    "項目",
                    placeholder="例：牛乳",
                    label_visibility="collapsed",
                    key=f"item_input_{selected_memo['id']}"
                )


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

            # -------------------------------------------------
            # 項目を1つずつ表示
            # -------------------------------------------------

            for item in items:

                # =================================================
                # ここが重要
                #
                # チェック
                # ↓
                # 項目名
                # ↓
                # 削除
                #
                # を必ず横1列にする
                # =================================================

                check_col, text_col, delete_col = st.columns(
                    [0.8, 7.2, 1],
                    vertical_alignment="center"
                )


                # -------------------------------------------------
                # 左：チェックボックス
                # -------------------------------------------------

                with check_col:

                    checked = st.checkbox(
                        "完了",
                        value=bool(item["completed"]),
                        key=f"completed_{item['id']}",
                        label_visibility="collapsed"
                    )


                # -------------------------------------------------
                # チェック状態が変わった場合
                # -------------------------------------------------

                if checked != bool(item["completed"]):

                    update_item_completed(
                        item["id"],
                        checked
                    )

                    st.rerun()


                # -------------------------------------------------
                # 中央：項目名
                # -------------------------------------------------

                with text_col:

                    if item["completed"]:

                        st.markdown(
                            f"<div style='padding-top:8px; "
                            f"text-decoration:line-through; "
                            f"opacity:0.55;'>"
                            f"{item['item']}"
                            f"</div>",
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            f"<div style='padding-top:8px;'>"
                            f"{item['item']}"
                            f"</div>",
                            unsafe_allow_html=True
                        )


                # -------------------------------------------------
                # 右：削除ボタン
                # -------------------------------------------------

                with delete_col:

                    if st.button(
                        "🗑",
                        key=f"delete_item_{item['id']}",
                        help="この項目を削除"
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
    # フリーメモ保存
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


                with text_col:

                    st.write(
                        free_memo["content"]
                    )

                    st.caption(
                        f"保存日時：{free_memo['created_at']}"
                    )


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

