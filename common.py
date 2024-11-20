import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from collections import Counter
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


def show_chart_score(ranking):
    scores = [item["score"] for item in ranking]
    max_score = max(scores) if scores else 100
    bins = list(range(0, int(max_score) + 5, 5))  # Tạo các khoảng cách 5 điểm

    fig_scores = plt.figure(figsize=(8, 6))
    plt.hist(scores, bins=bins, edgecolor="black")
    plt.title("Phổ điểm theo khoảng cách 5 điểm")
    plt.xlabel("Điểm số")
    plt.ylabel("Số lượng thí sinh")
    plt.grid(True, alpha=0.3)
    st.pyplot(fig_scores)
    plt.close()


def show_chart_spent_time(ranking):
    spent_times = [
        item["spent_time"] / 60 for item in ranking
    ]  # Chuyển đổi giây sang phút
    scores = [item["score"] for item in ranking]
    max_time = max(spent_times) if spent_times else 120
    time_bins = list(range(0, int(max_time) + 5, 5))  # Tạo các khoảng cách 5 phút

    fig_times, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    n, bins, patches = ax1.hist(spent_times, bins=time_bins, edgecolor="black")

    # Tính điểm trung bình cho mỗi khoảng thời gian
    avg_scores = []
    for i in range(len(bins) - 1):
        bin_scores = [
            score
            for time, score in zip(spent_times, scores)
            if bins[i] <= time < bins[i + 1]
        ]
        avg_scores.append(sum(bin_scores) / len(bin_scores) if bin_scores else 0)

    # Vẽ đường điểm trung bình
    ax2.plot(bins[:-1], avg_scores, color="red", marker="o")

    ax1.set_title("Phân bố thời gian làm bài và điểm trung bình")
    ax1.set_xlabel("Thời gian (phút)")
    ax1.set_ylabel("Số lượng thí sinh", color="blue")
    ax2.set_ylabel("Điểm trung bình", color="red")

    ax1.grid(True, alpha=0.3)

    # Thêm chú thích
    ax1.legend(["Số lượng thí sinh"], loc="upper left")
    ax2.legend(["Điểm trung bình"], loc="upper right")

    st.pyplot(fig_times)
    plt.close()


def show_chart_org(ranking):
    # Tạo biểu đồ phân bố tỉnh thành và điểm trung bình
    provinces = [item["org_name"] for item in ranking]
    scores = [item["score"] for item in ranking]
    province_counts = Counter(provinces)

    # Tính điểm trung bình cho mỗi tỉnh
    province_avg_scores = {}
    for province, count in province_counts.items():
        province_scores = [
            score
            for item, score in zip(ranking, scores)
            if item["org_name"] == province
        ]
        province_avg_scores[province] = sum(province_scores) / count

    # Sp xếp và lấy top 10 tỉnh thành có số lượng thí sinh nhiều nhất
    top_10_provinces = dict(
        sorted(province_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    )

    fig_provinces, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    bars = ax1.bar(top_10_provinces.keys(), top_10_provinces.values(), color="skyblue")
    line = ax2.plot(
        top_10_provinces.keys(),
        [province_avg_scores[province] for province in top_10_provinces.keys()],
        color="red",
        marker="o",
    )

    ax1.set_title("Top 10 tỉnh thành có nhiều thí sinh nhất và điểm trung bình")
    ax1.set_xlabel("Tỉnh thành")
    ax1.set_ylabel("Số lượng thí sinh", color="skyblue")
    ax1.set_xticklabels(top_10_provinces.keys(), rotation=90)
    ax2.set_ylabel("Điểm trung bình", color="red")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Thêm chú thích
    ax1.legend([bars], ["Số lượng thí sinh"], loc="upper left")
    ax2.legend([line[0]], ["Điểm trung bình"], loc="upper right")

    st.pyplot(fig_provinces)
    plt.close()


def show_chart_score_spent_time(ranking):
    # Tạo biểu đồ phân bố giữa score và spent_time_formated
    scores = [item["score"] for item in ranking]
    spent_times = [int(item["spent_time"]) / 60 for item in ranking]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(spent_times, scores, color="skyblue")
    ax.set_title("Phân bố giữa điểm và thời gian làm bài")
    ax.set_xlabel("Thời gian (phút)")
    ax.set_ylabel("Điểm")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close()


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
