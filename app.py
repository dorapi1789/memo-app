
import streamlit as st
import sqlite3
from datetime import datetime
import html


# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="かんたんメモ",
    page_icon="📝",
    layout="centered"
)


# =========================================================
# スマホ専用CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
   基本設定
   ========================================================= */

html,
body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
}


* {
    box-sizing: border-box !important;
}


.block-container {
    width: 100% !important;
    max-width: 100% !important;

    padding-top: 15px !important;
    padding-bottom: 30px !important;

    padding-left: 10px !important;
    padding-right: 10px !important;

    margin: 0 !important;

    overflow-x: hidden !important;
}


/* =========================================================
   タイトル
   ========================================================= */

h1 {
    font-size: 1.7rem !important;
    margin-bottom: 5px !important;
}

h2 {
    font-size: 1.3rem !important;
}

h3 {
    font-size: 1.1rem !important;
}


/* =========================================================
   全ての横方向コンテナ
   ========================================================= */

div[data-testid="stHorizontalBlock"] {

    width: 100% !important;
    max-width: 100% !important;

    min-width: 0 !important;

    overflow: hidden !important;

    flex-wrap: nowrap !important;

    gap: 6px !important;
}


/* =========================================================
   横方向コンテナの子要素
   ========================================================= */

div[data-testid="stHorizontalBlock"] > div {

    min-width: 0 !important;

    overflow: hidden !important;
}


/* =========================================================
   メモタイトルボタン
   ========================================================= */

.memo-button-wrapper {

    width: fit-content !important;

    max-width: 100% !important;

    margin: 0 !important;

    padding: 0 !important;

    overflow: hidden !important;
}


.memo-button-wrapper + div {

    margin-top: 0 !important;
}


.memo-button-wrapper button {

    width: auto !important;

    max-width: calc(100vw - 30px) !important;

    min-width: 90px !important;

    height: 38px !important;

    min-height: 38px !important;

    padding: 3px 12px !important;

    margin: 0 !important;

    border-radius: 8px !important;

    font-size: 0.9rem !important;

    white-space: nowrap !important;

    overflow: hidden !important;

    text-overflow: ellipsis !important;
}


/* =========================================================
   メモ一覧のボタン間隔
   ========================================================= */

div[data-testid="element-container"]:has(
    .memo-button-wrapper
) {

    margin-top: 0 !important;

    margin-bottom: 1px !important;

    padding: 0 !important;
}


/* =========================================================
   項目追加エリア
   ========================================================= */

.add-item-area {

    width: 100% !important;

    max-width: 100% !important;

    overflow: hidden !important;
}


/* =========================================================
   項目入力欄
   ========================================================= */

.add-item-input {

    width: 100% !important;

    min-width: 0 !important;

    overflow: hidden !important;
}


.add-item-input input {

    width: 100% !important;

    max-width: 100% !important;

    height: 42px !important;

    box-sizing: border-box !important;
}


/* =========================================================
   ＋ボタン
   ========================================================= */

.add-item-button {

    width: 42px !important;

    min-width: 42px !important;

    max-width: 42px !important;

    flex: 0 0 42px !important;

    overflow: hidden !important;
}


.add-item-button button {

    width: 42px !important;

    min-width: 42px !important;

    max-width: 42px !important;

    height: 42px !important;

    min-height: 42px !important;

    padding: 0 !important;

    margin: 0 !important;
}


/* =========================================================
   項目行
   ========================================================= */

.memo-item-row {

    width: 100% !important;

    max-width: 100% !important;

    min-width: 0 !important;

    overflow: hidden !important;
}


/* =========================================================
   チェックボックス部分
   ========================================================= */

.memo-check {

    width: 32px !important;

    min-width: 32px !important;

    max-width: 32px !important;

    flex: 0 0 32px !important;

    overflow: hidden !important;
}


.memo-check div[data-testid="stCheckbox"] {

    width: 32px !important;

    min-width: 32px !important;

    max-width: 32px !important;

    margin: 0 !important;

    padding: 0 !important;
}


/* =========================================================
   項目名
   ========================================================= */

.memo-item-name {

    flex: 1 1 auto !important;

    width: auto !important;

    min-width: 0 !important;

    max-width: none !important;

    overflow: hidden !important;

    padding: 5px 2px !important;

    font-size: 1rem !important;

    line-height: 1.4 !important;

    white-space: normal !important;

    overflow-wrap: anywhere !important;

    word-break: break-word !important;
}


.memo-item-name p {

    margin: 0 !important;

    padding: 0 !important;
}


/* =========================================================
   完了した項目
   ========================================================= */

.memo-item-name.completed {

    text-decoration: line-through !important;

    opacity: 0.45 !important;
}


/* =========================================================
   削除ボタン
   ========================================================= */

.memo-delete {

    width: 38px !important;

    min-width: 38px !important;

    max-width: 38px !important;

    flex: 0 0 38px !important;

    overflow: hidden !important;
}


.memo-delete button {

    width: 36px !important;

    min-width: 36px !important;

    max-width: 36px !important;

    height: 36px !important;

    min-height: 36px !important;

    padding: 0 !important;

    margin: 0 !important;

    font-size: 0.9rem !important;
}


/* =========================================================
   項目行の余白
   ========================================================= */

div[data-testid="element-container"]:has(
    .memo-item-row
) {

    width: 100% !important;

    max-width: 100% !important;

    margin-top: 0 !important;

    margin-bottom: 2px !important;

    padding: 0 !important;

    overflow: hidden !important;
}


/* =========================================================
   フォーム
   ========================================================= */

.stForm {

    width: 100% !important;

    max-width: 100% !important;

    overflow: hidden !important;
}


/* =========================================================
   テキスト入力
   ========================================================= */

.stTextInput {

    width: 100% !important;

    max-width: 100% !important;
}


.stTextInput input {

    width: 100% !important;

    max-width: 100% !important;

    box-sizing: border-box !important;
}


/* =========================================================
   フリーメモ
   ========================================================= */

.stTextArea {

    width: 100% !important;

    max-width: 100% !important;
}


.stTextArea textarea {

    width: 100% !important;

    max-width: 100% !important;

    box-sizing: border-box !important;
}


/* =========================================================
   ボタン
   ========================================================= */

.stButton button {

    border-radius: 8px !important;
}


/* =========================================================
   スマホ幅での最終調整
   ========================================================= */

@media (max-width: 600px) {

    .block-container {

        padding-left: 8px !important;

        padding-right: 8px !important;

        width: 100vw !important;

        max-width: 100vw !important;
    }


    /* 項目行 */

    .memo-item-row {

        width: 100% !important;

        max-width: 100% !important;
    }


    /* 項目名をできる限り広くする */

    .memo-item-name {

        flex: 1 1 0% !important;

        min-width: 0 !important;

        width: 0 !important;

        max-width: none !important;

        white-space: normal !important;

        overflow-wrap: anywhere !important;

        word-break: break-word !important;

        font-size: 0.95rem !important;
    }


    /* チェック */

    .memo-check {

        flex: 0 0 30px !important;

        width: 30px !important;

        min-width: 30px !important;

        max-width: 30px !important;
    }


    /* 削除 */

    .memo-delete {

        flex: 0 0 36px !important;

        width: 36px !important;

        min-width: 36px !important;

        max-width: 36px !important;
    }


    .memo-delete button {

        width: 34px !important;

        min-width: 34px !important;

        max-width: 34px !important;

        height: 34px !important;

        min-height: 34px !important;
    }


    /* ＋ボタン */

    .add-item-button {

        flex: 0 0 40px !important;

        width: 40px !important;

        min-width: 40px !important;

        max-width: 40px !important;
    }


    .add-item-button button {

        width: 40px !important;

        min-width: 40px !important;

        max-width: 40px !important;

        height: 40px !important;

        min-height: 40px !important;
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


    # メモ
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)


    # メモ項目
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memo_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memo_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)


    # completed列がない古いDBへの対応
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

    conn.close()


# =========================================================
# メモ削除
# =========================================================

def delete_memo(memo_id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        DELETE FROM memo_items
        WHERE memo_id = ?
    """, (memo_id,))


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
# 項目チェック変更
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
        key="create_memo_form",
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


if not memos:

    st.info(
        "まだメモがありません。"
        "「新しいメモを作成」からメモを作ってください。"
    )


else:

    for memo in memos:

        if (
            st.session_state.opened_memo_id
            == memo["id"]
        ):

            button_text = f"🔽 {memo['title']}"

        else:

            button_text = f"📝 {memo['title']}"


        st.markdown(
            '<div class="memo-button-wrapper">',
            unsafe_allow_html=True
        )


        if st.button(
            button_text,
            key=f"open_memo_{memo['id']}"
        ):

            if (
                st.session_state.opened_memo_id
                == memo["id"]
            ):

                st.session_state.opened_memo_id = None

            else:

                st.session_state.opened_memo_id = memo["id"]


            st.rerun()


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# 選択中のメモ
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


    if selected_memo is None:

        st.session_state.opened_memo_id = None

        st.rerun()


    else:

        st.divider()


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
                [1, 0.11],
                gap="small"
            )


            with item_col:

                st.markdown(
                    '<div class="add-item-input">',
                    unsafe_allow_html=True
                )


                new_item = st.text_input(
                    "項目",
                    placeholder="例：牛乳を買う",
                    label_visibility="collapsed",
                    key=f"item_input_{selected_memo['id']}"
                )


                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            with add_col:

                st.markdown(
                    '<div class="add-item-button">',
                    unsafe_allow_html=True
                )


                add_button = st.form_submit_button(
                    "＋"
                )


                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


        if add_button:

            item_text = new_item.strip()


            if item_text:

                add_memo_item(
                    selected_memo["id"],
                    item_text
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

                # -----------------------------------------
                # 1行の項目
                # -----------------------------------------

                item_cols = st.columns(
                    [0.55, 8.0, 0.7],
                    gap="small"
                )


                # -----------------------------------------
                # チェックボックス
                # -----------------------------------------

                with item_cols[0]:

                    st.markdown(
                        '<div class="memo-check">',
                        unsafe_allow_html=True
                    )


                    checked = st.checkbox(
                        "完了",
                        value=bool(item["completed"]),
                        key=f"completed_{item['id']}",
                        label_visibility="collapsed"
                    )


                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


                # -----------------------------------------
                # 項目名
                # -----------------------------------------

                with item_cols[1]:

                    safe_item = html.escape(
                        str(item["item"])
                    )


                    if item["completed"]:

                        st.markdown(
                            f"""
                            <div class="memo-item-name completed">
                                {safe_item}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            f"""
                            <div class="memo-item-name">
                                {safe_item}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                # -----------------------------------------
                # 削除ボタン
                # -----------------------------------------

                with item_cols[2]:

                    st.markdown(
                        '<div class="memo-delete">',
                        unsafe_allow_html=True
                    )


                    if st.button(
                        "🗑",
                        key=f"delete_item_{item['id']}",
                        help="この項目を削除"
                    ):

                        delete_memo_item(
                            item["id"]
                        )

                        st.rerun()


                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


                # -----------------------------------------
                # チェック状態変更
                # -----------------------------------------

                if checked != bool(item["completed"]):

                    update_item_completed(
                        item["id"],
                        checked
                    )

                    st.rerun()


        # =================================================
        # メモ削除
        # =================================================

        st.write("")


        if st.button(
            "🗑️ このメモを削除",
            key=f"delete_memo_{selected_memo['id']}",
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

                st.write(
                    free_memo["content"]
                )


                st.caption(
                    f"保存日時：{free_memo['created_at']}"
                )


                if st.button(
                    "🗑️ このフリーメモを削除",
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

