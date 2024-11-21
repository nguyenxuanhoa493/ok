import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter
import streamlit as st
from common import format_time


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


def show_metric(ranking):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        exam_count = len(ranking)
        st.metric("Số bài thi", exam_count)
    with col2:
        org_count = len(set([item["org_name"] for item in ranking]))
        st.metric("Số đơn vị tham gia", org_count)
    with col3:
        max_score = max([item["score"] for item in ranking])
        st.metric("Điểm cao nhất", max_score)

    with col4:
        avg_score = sum([item["score"] for item in ranking]) / len(ranking)
        st.metric("Điểm trung bình", round(avg_score, 2))

    with col5:
        avg_spent_time = sum([item["spent_time"] for item in ranking]) / len(ranking)
        st.metric("Thời gian làm bài trung bình(phút)", round(avg_spent_time / 60))
