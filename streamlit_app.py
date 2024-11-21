from lms import Lms
import streamlit as st
import pandas as pd

from common import get_info, export_excel
from chart import (
    show_chart_score,
    show_chart_spent_time,
    show_chart_org,
    show_chart_score_spent_time,
    show_metric,
)
from input import (
    show_prizes_config,
    show_round_selector,
    show_prize_filter,
    show_org_filter,
    show_score_filter,
)

st.set_page_config(
    page_title="Bảng xếp hạng cuộc thi",
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
    org_filter = show_org_filter(ranking)
    score_range = show_score_filter(ranking)


# Lọc ranking theo các điều kiện
if prize_filter and len(prize_filter) > 0:
    ranking = [item for item in ranking if item["prize_name"] in prize_filter]
if org_filter:
    ranking = [item for item in ranking if item["org_name"] in org_filter]
if score_range:
    ranking = [
        item for item in ranking if score_range[0] <= item["score"] <= score_range[1]
    ]

show_metric(ranking)
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

# Tạo phân tích phổ điểm và phân bố tỉnh thành
col1, col2, col3, col4 = st.columns(4)

with col1:
    show_chart_score(ranking)
with col2:
    show_chart_spent_time(ranking)
with col3:
    show_chart_org(ranking)
with col4:
    show_chart_score_spent_time(ranking)

st.dataframe(df_ranking, use_container_width=True)
if st.button("Xuất Excel"):
    export_excel(
        ranking,
        "Bảng xếp hạng",
        label_ranking,
    )
