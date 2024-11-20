from lms import Lms
import streamlit as st
import pandas as pd

from common import (
    get_info,
    show_chart_score,
    show_chart_spent_time,
    show_chart_org,
    export_excel,
    show_chart_score_spent_time,
)
from input import show_prizes_config, show_round_selector, show_prize_filter

st.set_page_config(
    page_title="Bảng xếp hạng",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)

dmn = st.query_params["dmn"]
user_code = st.query_params.get("user_code", "")
user_code = user_code if user_code else dmn
contest_iid = st.query_params["contest"]

if not contest_iid:
    st.error("Thiếu tham số contest_iid trong URL")
    st.stop()
if not dmn:
    st.error("Thiếu tham số dmn trong URL")
    st.stop()


# @st.cache_resource
def get_admin():
    return Lms(dmn, user_code)


admin = get_admin()

list_round = admin.get_round(contest_iid=contest_iid)
col1, col2 = st.columns(2)

with col1:
    prizes = show_prizes_config()

with col2:
    selected_round = show_round_selector(list_round)
    prize_filter = show_prize_filter(prizes)

ranking = admin.get_rank(
    contest_iid=contest_iid, exam_round_iid=selected_round, items_per_page=-1
)
ranking = [get_info(item, prizes) for item in ranking]

# Lọc ranking theo giải đã chọn
if prize_filter:
    ranking = [item for item in ranking if item["prize_name"] in prize_filter]
label_ranking = [
    "STT",
    "Giải",
    "STT giải",
    "Họ và tên",
    "Mã",
    "Đơn vị",
    "Điểm",
    "Thời gian(s)",
    "Thời gian(hh:mm:ss)",
]
df_ranking = pd.DataFrame(ranking)
df_ranking.columns = label_ranking
df_ranking.set_index("STT", inplace=True)

st.dataframe(df_ranking, use_container_width=True)


if st.button("Xuất Excel"):
    export_excel(
        ranking,
        "Bảng xếp hạng",
        label_ranking,
    )

# Tạo phân tích phổ điểm và phân bố tỉnh thành
col1, col2, col3 = st.columns(3)

with col1:
    show_chart_score(ranking)
    show_chart_score_spent_time(ranking)
with col2:
    show_chart_spent_time(ranking)
with col3:
    show_chart_org(ranking)
