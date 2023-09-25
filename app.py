import streamlit as st
import datetime
import time
from PIL import Image
from backend import send_request


def main():
    high_bp1, low_bp1, high_bp2, low_bp2, meal = None, None, None, None, None

    # セッション状態の初期化
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None

    # cookie_manager = get_manager()
    # モバイル用の縦長のレイアウトを設定
    # st.set_page_config(layout="wide")
    st.title("血圧行動記録アプリ")
    submit_mes = st.header("")


    # 1行目: UIDと送信ボタン
    uid_textinput_col, send_button_col = st.columns(2)
    # uid_value = get_cookie("uid")
    uid_value = None
    uid_textinput_col.text_input("Email", value=uid_value)


    # 2行目: 1秒ごとに更新される時刻
    time_placeholder = st.empty()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_placeholder.write(f"現在時刻: {current_time}")

    # 3行目: 最高血圧と最低血圧のinput text
    st.header("血圧")
    high_bp1_col, low_bp1_col = st.columns(2)
    high_bp1 = high_bp1_col.number_input("最高血圧1(mmHg)", min_value=0, max_value=300, value=120, step=1)
    low_bp1 = low_bp1_col.number_input("最低血圧1(mmHg)", min_value=0, max_value=300, value=80, step=1)

    # 4行目: 最高血圧と最低血圧のinput text
    high_bp2_col, low_bp2_col = st.columns(2)
    high_bp2 = high_bp2_col.number_input("最高血圧2(mmHg)", min_value=0, max_value=300, value=120, step=1)
    low_bp2 = low_bp2_col.number_input("最低血圧2(mmHg)", min_value=0, max_value=300, value=80, step=1)

    # 5行目: 食事のinput textと画像参照ボタン
    st.header("食事")
    meal_col, image_ref_button_col = st.columns(2)
    meal = meal_col.text_input("食事")

    uploaded_file = image_ref_button_col.file_uploader("食事画像", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロードされた画像", width=100)  # widthを200pxに設定
    
    is_camera = image_ref_button_col.checkbox("カメラ")
    if is_camera:
        picture = st.camera_input("カメラ")

    # # 6行目: 飲酒のinput text
    # drink_col = st.text_input("飲酒")

    # # 7行目: タバコのinput text
    # smoke_col = st.text_input("タバコ")

    # 8行目: ジョギングとヨガのボタン
    # カテゴリとサブカテゴリのデータ
    # CSSを使用してボタンのサイズを変更
    # CSSを使用してボタンのサイズと列の最小幅を変更
    st.markdown("""
        <style>
            .stButton > button {
                width: 150px;
                height: 50px;
                font-size: 20px;
            }
            @media (max-width: 768px) {
                .stApp .stColumns .stColumn {
                    flex: 0 0 33.33% !important;
                    max-width: 33.33% !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)
    st.header("カテゴリとサブカテゴリ")
    categories = {
        "ワークライフ": ["仕事", "オフィス", "リモートワーク", "現場", "出張", "休憩", "休暇", "その他"],
        "運動": ["ウォーキング", "ジョギング", "サイクリング", "スポーツ", "ヨガ", "筋トレ", "瞑想", "その他"],
        "温冷浴": ["お風呂", "シャワー", "サウナ", "その他"],
        "カフェイン": ["コーヒー", "紅茶", "緑茶", "その他"],
        "アルコール": ["ビール", "日本酒", "焼酎", "ワイン", "ウィスキー", "カクテル", "その他"],
        "ニコチン": ["紙巻タバコ", "加熱式タバコ", "電子タバコ", "その他"],
        "体調": ["元気", "疲労", "不調", "リラックス", "ストレス", "その他"],
        "感情": ["怒り", "不安", "幸福", "興奮", "悲しみ", "その他"],
        "痛み": ["頭痛", "腹痛", "腰痛", "胸痛", "背痛", "筋肉痛", "生理痛", "その他"]
    }
    # セッション状態の初期化
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
        
    # ボタンと対応するサブカテゴリの選択
    category_list = list(categories.keys())
    for i in range(0, len(category_list), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(category_list[i], key=f"btn_{i}"):
                st.session_state.selected_category = category_list[i]
        with col2:
            if i+1 < len(category_list) and st.button(category_list[i+1], key=f"btn_{i+1}"):
                st.session_state.selected_category = category_list[i+1]
        with col3:
            if i+2 < len(category_list) and st.button(category_list[i+2], key=f"btn_{i+2}"):
                st.session_state.selected_category = category_list[i+2]

    # 選択されたカテゴリに基づいてサブカテゴリを表示
    if st.session_state.selected_category:
        selected_subcategory = st.selectbox("サブカテゴリを選択してください", categories[st.session_state.selected_category])
        st.write(f"選択されたカテゴリ: {st.session_state.selected_category}")
        st.write(f"選択されたサブカテゴリ: {selected_subcategory}")

    if send_button_col.button("送信"):
        data = make_data(uid_value, high_bp1, low_bp1, high_bp2, low_bp2, meal)
        response_data, error_text = send_request(data)  # 外部ファイルの関数を呼び出す
        #set_cookie("uid", uid_value)
        #cookie_manager.set_cookie("uid", uid_value)

        if error_text:
            st.write(f"失敗: {error_text}")
            submit_mes.header("送信失敗")
        else:
            st.write(f"成功: {response_data}")
            submit_mes.header("送信成功")


    # 無限ループで時刻を更新（注意: 他の操作をブロックする可能性があります）
    while True:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_placeholder.write(f"現在時刻: {current_time}")
        time.sleep(1)


def make_data(uid_value, high_bp1, low_bp1, high_bp2, low_bp2, meal):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "uid": uid_value,
        "time": current_time,
    }
    if high_bp1 not in ["", None]:
        data["high_bp1"] = high_bp1
    if low_bp1 not in ["", None]:
        data["low_bp1"] = low_bp1
    if high_bp2 not in ["", None]:
        data["high_bp2"] = high_bp2
    if low_bp2 not in ["", None]:
        data["low_bp2"] = low_bp2
    if meal not in ["", None]:
        data["meal"] = meal
    return data

if __name__ == "__main__":
    main()