import streamlit as st

def init_prizes_config():
    if "prize_count" not in st.session_state:
        st.session_state.prizes_data = [
            {"name": "Giải Siêu Sao", "quantity": 1},
            {"name": "Giải Đặc Biệt", "quantity": 2},
            {"name": "Giải Nhất", "quantity": 5},
            {"name": "Giải Nhì", "quantity": 10},
            {"name": "Giải Ba", "quantity": 50},
        ]
        st.session_state.prize_count = len(st.session_state.prizes_data)

def update_prizes():
    prizes = {}
    for i in range(st.session_state.prize_count):
        name = st.session_state.get(f"prize_name_{i}")
        quantity = st.session_state.get(f"prize_quantity_{i}")
        if name and quantity:
            prizes[name] = quantity
    return prizes

def show_prizes_config():
    st.subheader("Cấu hình giải thưởng")
    prizes_container = st.container()
    
    init_prizes_config()

    with prizes_container:
        for i in range(st.session_state.prize_count):
            col_name, col_quantity, col_delete = st.columns([2, 1, 0.5])
            with col_name:
                default_name = (
                    st.session_state.prizes_data[i]["name"]
                    if i < len(st.session_state.prizes_data)
                    else f"Giải {i+1}"
                )
                st.text_input(
                    "Tên giải",
                    key=f"prize_name_{i}",
                    value=default_name,
                    label_visibility="collapsed",
                )
            with col_quantity:
                default_quantity = (
                    st.session_state.prizes_data[i]["quantity"]
                    if i < len(st.session_state.prizes_data)
                    else 1
                )
                st.number_input(
                    "Số lượng",
                    min_value=1,
                    key=f"prize_quantity_{i}",
                    value=default_quantity,
                    label_visibility="collapsed",
                )
            with col_delete:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.prize_count -= 1
                    st.rerun()

    col_add, col_space = st.columns([1, 3])
    with col_add:
        if st.button("➕ Thêm giải", use_container_width=True):
            st.session_state.prize_count += 1
            st.rerun()

    return update_prizes()

def show_round_selector(list_round):
    selected_round = st.selectbox(
        "Chọn vòng thi:",
        options=[round["value"] for round in list_round],
        format_func=lambda x: next(
            (r["primaryText"] for r in list_round if r["value"] == x), ""
        ),
    )
    return selected_round

def show_prize_filter(prizes):
    prize_filter = st.multiselect(
        "Lọc theo giải:",
        options=list(prizes.keys()),
        default=list(prizes.keys()),
        help="Chọn các giải muốn hiển thị",
    )
    return prize_filter 