import streamlit as st
import platform

st.set_page_config(page_title="", layout="centered")

# Hide title and extra spacing
st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { padding-top: 0rem; }
    .keypad-row { display: flex; justify-content: center; margin-bottom: 10px; }
    .key-button { width: 70px; height: 70px; font-size: 24px; margin: 5px; font-family: 'Myriad Pro', sans-serif; }
    .input-display { font-family: 'Myriad Pro', sans-serif; text-transform: uppercase; font-weight: bold; font-size: 32px; text-align: center; margin: 20px auto; border: 1px solid #ccc; padding: 10px; width: 220px; }
    .results { font-family: 'Myriad Pro', sans-serif; text-transform: uppercase; font-weight: bold; font-size: 22px; text-align: center; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# Detect if mobile
is_mobile = platform.system() == "Linux" and "android" in platform.platform().lower()

# State variables
if "age_input" not in st.session_state:
    st.session_state.age_input = ""
if "selected_gender" not in st.session_state:
    st.session_state.selected_gender = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Pricing data
male_ia_prices = {**{a: 21 for a in range(18, 41)}, **{a: 25 for a in range(41, 46)}}
female_ia_prices = {**{a: 20 for a in range(18, 41)}, **{a: 22 for a in range(41, 46)}}
male_tl_prices = {46: 25, 47: 27, 48: 28, 49: 30, 50: 31, 51: 33, 52: 35, 53: 37, 54: 39, 55: 41, 56: 45, 57: 49, 58: 53, 59: 58, 60: 62, 61: 70, 62: 77, 63: 84, 64: 93}
female_tl_prices = {46: 25, 47: 25, 48: 26, 49: 27, 50: 27, 51: 29, 52: 30, 53: 32, 54: 34, 55: 35, 56: 38, 57: 40, 58: 43, 59: 46, 60: 49, 61: 54, 62: 58, 63: 62, 64: 67}
male_sh_prices = {**{a: 9 for a in range(18, 41)}, **{41: 14, 42: 14, 43: 15, 44: 15, 45: 16}, 46: 17, 47: 18, 48: 19, 49: 20, 50: 21, 51: 26, 52: 26, 53: 28, 54: 29, 55: 30, 56: 32, 57: 33, 58: 35, 59: 37, 60: 38, 61: 50, 62: 53, 63: 58, 64: 67}
female_sh_prices = {18: 14, 19: 14, 20: 14, 21: 14, 22: 15, 23: 15, 24: 15, 25: 16, 26: 16, 27: 17, 28: 17, 29: 18, 30: 19, 31: 19, 32: 20, 33: 20, 34: 21, 35: 21, 36: 21, 37: 22, 38: 22, 39: 23, 40: 23, 41: 23, 42: 24, 43: 24, 44: 25, 45: 25, 46: 27, 47: 28, 48: 29, 49: 32, 50: 37, 51: 39, 52: 41, 53: 42, 54: 44, 55: 44, 56: 45, 57: 46, 58: 47, 59: 49, 60: 50, 61: 53, 62: 56, 63: 59, 64: 62}
final_expense_prices = {age: {"Male": male, "Female": female} for age, male, female in [(65, 80, 64), (66, 85, 68), (67, 89, 72), (68, 94, 76), (69, 99, 80), (70, 103, 84), (71, 110, 89), (72, 116, 95), (73, 123, 101), (74, 129, 107), (75, 136, 112), (76, 144, 120), (77, 152, 128), (78, 160, 137), (79, 168, 145), (80, 176, 153)]}

# Input display
suffix = ""
if st.session_state.selected_gender == "Male":
    suffix = " M"
elif st.session_state.selected_gender == "Female":
    suffix = " F"
st.markdown(f'<div class="input-display">{st.session_state.age_input}{suffix}</div>', unsafe_allow_html=True)

# Only show keypad if not submitted
if not st.session_state.submitted:
    def add_digit(d):
        if len(st.session_state.age_input) < 2:
            st.session_state.age_input += str(d)

    def select_gender(g):
        st.session_state.selected_gender = g
        st.session_state.submitted = True

    rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for row in rows:
        cols = st.columns(3)
        for i, digit in enumerate(row):
            disabled = False
            if st.session_state.age_input == "9" and digit != 0:
                disabled = True
            if st.session_state.age_input == "8" and digit != 0:
                disabled = True
            if st.session_state.age_input == "1" and digit not in [8, 9]:
                disabled = True
            if st.session_state.age_input and int(st.session_state.age_input + str(digit)) > 80:
                disabled = True
            if cols[i].button(str(digit), key=f"btn{digit}", disabled=disabled):
                add_digit(digit)

    colM, col0, colF = st.columns(3)
    if colM.button("MALE", key="male_btn"):
        select_gender("Male")
    if col0.button("0", key="btn0"):
        add_digit(0)
    if colF.button("FEMALE", key="female_btn"):
        select_gender("Female")

# Reset button
if st.button("RESET"):
    st.session_state.age_input = ""
    st.session_state.selected_gender = None
    st.session_state.submitted = False

# Display result
if st.session_state.submitted and st.session_state.age_input.isdigit():
    age = int(st.session_state.age_input)
    gender = st.session_state.selected_gender
    if age >= 65:
        fe_price = final_expense_prices[age][gender]
        st.markdown(f"<div class='results'>FE${fe_price}</div>", unsafe_allow_html=True)
    else:
        if age <= 45:
            plan = "IA"
            tl_price = male_ia_prices[age] if gender == "Male" else female_ia_prices[age]
        else:
            plan = "TL"
            tl_price = male_tl_prices[age] if gender == "Male" else female_tl_prices[age]
        sh_price = male_sh_prices[age] if gender == "Male" else female_sh_prices[age]
        bundle = tl_price + sh_price
        st.markdown(f"<div class='results'>{plan}${tl_price}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='results'>SH${sh_price}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='results'>BUNDLE${bundle}</div>", unsafe_allow_html=True)
