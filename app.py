
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
# スマホ用CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
   画面全体
   ========================================================= */

html,
body {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    overflow-x: hidden !important;
}

[data-testid="stAppViewContainer"] {
    width: 100% !important;
    overflow-x: hidden !important;
}

[data-testid="stAppViewBlockContainer"] {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
}

.block-container {
    width: 100% !important;
    max-width: 100% !important;

    padding-top: 15px !important;
    padding-bottom: 30px !important;

    padding-left: 8px !important;
    padding-right: 8px !important;

    overflow-x: hidden !important;
}


/* =========================================================
   横並び
   ========================================================= */

div[data-testid="stHorizontalBlock"] {
    width: 100% !important;
    max-width: 100% !important;

    min-width: 0 !important;

    flex-wrap: nowrap !important;

    align-items: center !important;

    overflow: hidden !important;
}

div[data-testid="stHorizontalBlock"] > div {
    min-width: 0 !important;
}


/* =========================================================
   メモタイトル
   ========================================================= */

.memo-title-button {
    width: fit-content !important;
    max-width: 100% !important;

    margin: 0 !important;
    padding: 0 !important;
}

.memo-title-button button {
    width: auto !important;

    min-width: 90px !important;
    max-width: calc(100vw - 25px) !important;

    height: 38px !important;
    min-height: 38px !important;

    padding: 4px 12px !important;

    margin: 0 !important;

    white-space: nowrap !important;

    overflow: hidden !important;

    text-overflow: ellipsis !important;
}


/* =========================================================
   項目行
   ========================================================= */

.item-row {
    width: 100% !important;

    min-width: 0 !important;

    height: 48px !important;

    display: flex !important;

    align-items: center !important;

    overflow: hidden !important;
}


/* =========================================================
   ★ チェックボックス
   ========================================================= */

.item-check {
    width: 100% !important;

    min-width: 0 !important;

    height: 48px !important;

    margin: 0 !important;
    padding: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;
}


/*
   Streamlit checkbox 本体の位置をリセット
*/

.item-check div[data-testid="stCheckbox"] {
    width: 48px !important;

    min-width: 48px !important;

    height: 48px !important;

    margin: 0 !important;
    padding: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;
}


/*
   label全体
*/

.item-check div[data-testid="stCheckbox"] > label {
    width: 48px !important;

    min-width: 48px !important;

    height: 48px !important;

    margin: 0 !important;

    padding: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    cursor: pointer !important;
}


/*
   ★ チェックボックスを36pxに大型化
*/

.item-check input[type="checkbox"] {
    appearance: none !important;
    -webkit-appearance: none !important;

    width: 36px !important;
    height: 36px !important;

    min-width: 36px !important;
    min-height: 36px !important;

    max-width: 36px !important;
    max-height: 36px !important;

    margin: 0 !important;
    padding: 0 !important;

    border: 2px solid #777 !important;

    border-radius: 6px !important;

    background: white !important;

    cursor: pointer !important;

    position: relative !important;

    display: block !important;

    flex-shrink: 0 !important;
}


/*
   チェックされた状態
*/

.item-check input[type="checkbox"]:checked {
    background: #555 !important;

    border-color: #555 !important;
}


/*
   チェックマーク
*/

.item-check input[type="checkbox"]:checked::after {
    content: "✓" !important;

    position: absolute !important;

    left: 50% !important;
    top: 50% !important;

    transform: translate(-50%, -53%) !important;

    color: white !important;

    font-size: 25px !important;

    font-weight: bold !important;

    line-height: 1 !important;
}


/*
   チェックボックス周辺のStreamlit余白を削除
*/

.item-check div[data-testid="stCheckbox"] > label > div {
    margin: 0 !important;
    padding: 0 !important;
}


/* =========================================================
   項目名
   ========================================================= */

.memo-text {
    width: 100% !important;

    min-width: 0 !important;

    min-height: 48px !important;

    margin: 0 !important;

    padding: 5px 4px !important;

    font-size: 15px !important;

    line-height: 1.45 !important;

    display: flex !important;

    align-items: center !important;

    word-break: break-word !important;

    overflow-wrap: anywhere !important;

    white-space: normal !important;
}

.memo-text.completed {
    text-decoration: line-through !important;

    opacity: 0.45 !important;
}


/* =========================================================
   削除ボタン
   ========================================================= */

.item-delete {
    width: 100% !important;

    min-width: 0 !important;

    height: 48px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    margin: 0 !important;

    padding: 0 !important;
}

.item-delete button {
    width: 54px !important;

    min-width: 54px !important;

    max-width: 54px !important;

    height: 36px !important;

    min-height: 36px !important;

    max-height: 36px !important;

    margin: 0 !important;

    padding: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    text-align: center !important;

    line-height: 1 !important;

    white-space: nowrap !important;
}

.item-delete button > div {
    width: 100% !important;

    height: 100% !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    margin: 0 !important;

    padding: 0 !important;
}

.item-delete button p {
    width: 100% !important;

    height: 100% !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    margin: 0 !important;

    padding: 0 !important;

    line-height: 1 !important;

    text-align: center !important;
}


/* =========================================================
   項目追加
   ========================================================= */

.add-input {
    width: 100% !important;

    min-width: 0 !important;

    display: flex !important;

    align-items: center !important;
}

.add-input input {
    width: 100% !important;

    max-width: 100% !important;

    box-sizing: border-box !important;
}


/* =========================================================
   ＋ボタン
   ========================================================= */

.add-button {
    width: 100% !important;

    height: 100% !important;

    min-width: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    margin: 0 !important;

    padding: 0 !important;
}

.add-button button {
    width: 40px !important;

    min-width: 40px !important;

    max-width: 40px !important;

    height: 40px !important;

    min-height: 40px !important;

    max-height: 40px !important;

    margin: 0 !important;

    padding: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    text-align: center !important;

    line-height: 1 !important;
}


/* =========================================================
   スマホ
   ========================================================= */

@media (max-width: 600px) {

    .block-container {
        padding-left: 8px !important;
        padding-right: 8px !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 3px !important;
    }

    .memo-text {
        font-size: 15px !important;
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
# DB初期化
# =========================================================

def init_database():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memo_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memo_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)


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
# データ取得
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
# メモ関連
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
# 項目関連
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
# フリーメモ関連
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
# セッション
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
# 新しいメモ
# =========================================================

with st.expander(
    "➕ 新しいメモを作成",
    expanded=False
):

    with st.form(
        "create_memo_form",
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

            title_text = f"🔽 {memo['title']}"

        else:

            title_text = f"📝 {memo['title']}"


        st.markdown(
            '<div class="memo-title-button">',
            unsafe_allow_html=True
        )


        if st.button(
            title_text,
            key=f"memo_button_{memo['id']}"
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
            f"add_item_form_{selected_memo['id']}",
            clear_on_submit=True
        ):

            input_col, plus_col = st.columns(
                [8.5, 1],
                gap="small",
                vertical_alignment="center"
            )


            with input_col:

                st.markdown(
                    '<div class="add-input">',
                    unsafe_allow_html=True
                )

                new_item = st.text_input(
                    "項目",
                    placeholder="例：牛乳を買う",
                    label_visibility="collapsed",
                    key=f"new_item_{selected_memo['id']}"
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            with plus_col:

                st.markdown(
                    '<div class="add-button">',
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

                # =================================================
                # ★ 3列を横一列に固定
                #
                # チェック | 項目名 | 削除
                # =================================================

                check_col, text_col, delete_col = st.columns(
                    [1.25, 6.75, 1.5],
                    gap="small",
                    vertical_alignment="center"
                )


                # ---------------------------------------------
                # チェック
                # ---------------------------------------------

                with check_col:

                    st.markdown(
                        '<div class="item-check">',
                        unsafe_allow_html=True
                    )


                    checked = st.checkbox(
                        "完了",
                        value=bool(item["completed"]),
                        key=f"check_{item['id']}",
                        label_visibility="collapsed"
                    )


                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


                # ---------------------------------------------
                # 項目名
                # ---------------------------------------------

                with text_col:

                    safe_text = html.escape(
                        str(item["item"])
                    )


                    if item["completed"]:

                        st.markdown(
                            f"""
                            <div class="memo-text completed">
                                {safe_text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            f"""
                            <div class="memo-text">
                                {safe_text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                # ---------------------------------------------
                # 削除
                # ---------------------------------------------

                with delete_col:

                    st.markdown(
                        '<div class="item-delete">',
                        unsafe_allow_html=True
                    )


                    delete_button = st.button(
                        "削除",
                        key=f"delete_{item['id']}",
                        help="この項目を削除"
                    )


                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


                    if delete_button:

                        delete_memo_item(
                            item["id"]
                        )

                        st.rerun()


                # ---------------------------------------------
                # チェック状態更新
                # ---------------------------------------------

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
        "free_memo_form",
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

            with st.container(border=True):

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

st.caption("📝 かんたんメモ")
