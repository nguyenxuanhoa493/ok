import streamlit as st
import pandas as pd
from io import BytesIO


def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def get_prize_info(rank, prizes):
    current_pos = 1
    for prize_name, count in prizes.items():
        if rank <= current_pos + count - 1:
            return {"prize_name": prize_name, "prize_order": rank - current_pos + 1}
        current_pos += count
    return {"prize_name": None, "prize_order": None}


def get_info(item, prizes):
    prize_info = get_prize_info(item["ranking"], prizes)
    org_name = item["__expand"]["orgs"][0].get("short_name", "")
    if org_name == "":
        org_name = item["__expand"]["orgs"][0].get("name", "")
    return {
        "ranking": item["ranking"],
        "prize_name": prize_info["prize_name"],
        "prize_order": prize_info["prize_order"],
        "user_name": item["__expand"]["user"]["name"],
        "user_code": item["__expand"]["user"]["code"],
        # "avatar": item["__expand"]["user"]["avatar"],
        "org_name": org_name,
        "score": item["score"],
        "spent_time": item["spent_time"],
        "spent_time_formarted": format_time(item["spent_time"]),
    }


def export_excel(data, file_name, label: list = []):
    df = pd.DataFrame(data)
    if label:
        df.columns = label

    with BytesIO() as buffer:
        df.to_excel(buffer, index=False)
        st.download_button(
            label="Lưu file excel về máy",
            data=buffer.getvalue(),
            file_name=f"{file_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
