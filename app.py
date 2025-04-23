import streamlit as st
import platform

st.set_page_config(page_title="Quote Tool", layout="centered")

# Detect if on mobile
is_mobile = platform.system() == "Linux" and "android" in platform.platform().lower()

# Password protection
PASSWORD = "kittenpoodle"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "pw_attempt" not in st.session_state:
    st.session_state.pw_attempt = False
if not st.session_state.authenticated:
    st.title("🔒 Enter Password")
    pw = st.text_input("Password", type="password")
    if st.button("Submit"):
        st.session_state.pw_attempt = True
        if pw == PASSWORD:
            st.session_state.authenticated = True
    if st.session_state.pw_attempt and not st.session_state.authenticated:
        st.error("Incorrect password")
    st.stop()

# Styling
st.markdown("""
    <style>
        .stButton>button {
            height: 3em;
            width: 6em;
            margin: 5px;
            font-size: 1.1rem;
            background-color: #222;
            color: white;
            border-radius: 10px;
        }
        .stButton>button:hover {
            background-color: #444;
            color: #00f;
        }
        .dim {
            opacity: 0.4;
        }
        .highlight {
            border: 2px solid #0af;
            color: #0af !important;
        }
        .input-display {
            border: 1px solid white;
            padding: 0.5em;
            margin: 10px 0;
            font-size: 1.2em;
            width: 100%;
            text-align: center;
        }
        .character-row {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
        }
        .character-box {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .character-img {
            height: 60px;
        }
    </style>
""", unsafe_allow_html=True)

# State tracking
if "age_input" not in st.session_state:
    st.session_state.age_input = ""
if "selected_gender" not in st.session_state:
    st.session_state.selected_gender = None

# Constants
male_ia_prices = {**{a: 21 for a in range(18, 41)}, **{a: 25 for a in range(41, 46)}}
female_ia_prices = {**{a: 20 for a in range(18, 41)}, **{a: 22 for a in range(41, 46)}}
male_tl_prices = {46: 25, 47: 27, 48: 28, 49: 30, 50: 31, 51: 33, 52: 35, 53: 37, 54: 39, 55: 41, 56: 45, 57: 49, 58: 53, 59: 58, 60: 62, 61: 70, 62: 77, 63: 84, 64: 93}
female_tl_prices = {46: 25, 47: 25, 48: 26, 49: 27, 50: 27, 51: 29, 52: 30, 53: 32, 54: 34, 55: 35, 56: 38, 57: 40, 58: 43, 59: 46, 60: 49, 61: 54, 62: 58, 63: 62, 64: 67}
male_sh_prices = {**{a: 9 for a in range(18, 41)}, **{41: 14, 42: 14, 43: 15, 44: 15, 45: 16}, 46: 17, 47: 18, 48: 19, 49: 20, 50: 21, 51: 26, 52: 26, 53: 28, 54: 29, 55: 30, 56: 32, 57: 33, 58: 35, 59: 37, 60: 38, 61: 50, 62: 53, 63: 58, 64: 67}
female_sh_prices = {18: 14, 19: 14, 20: 14, 21: 14, 22: 15, 23: 15, 24: 15, 25: 16, 26: 16, 27: 17, 28: 17, 29: 18, 30: 19, 31: 19, 32: 20, 33: 20, 34: 21, 35: 21, 36: 21, 37: 22, 38: 22, 39: 23, 40: 23, 41: 23, 42: 24, 43: 24, 44: 25, 45: 25, 46: 27, 47: 28, 48: 29, 49: 32, 50: 37, 51: 39, 52: 41, 53: 42, 54: 44, 55: 44, 56: 45, 57: 46, 58: 47, 59: 49, 60: 50, 61: 53, 62: 56, 63: 59, 64: 62}
final_expense_prices = {age: {"Male": male, "Female": female} for age, male, female in [(65, 80, 64), (66, 85, 68), (67, 89, 72), (68, 94, 76), (69, 99, 80), (70, 103, 84), (71, 110, 89), (72, 116, 95), (73, 123, 101), (74, 129, 107), (75, 136, 112), (76, 144, 120), (77, 152, 128), (78, 160, 137), (79, 168, 145), (80, 176, 153)]}

# Age input display
st.markdown(f'<div class="input-display">{st.session_state.age_input}</div>', unsafe_allow_html=True)

# Number pad
if is_mobile:
    for row in [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0]]:
        cols = st.columns(len(row))
        for i, num in enumerate(row):
            if st.session_state.age_input == "9" and num != 0:
                continue
            if st.session_state.age_input == "8" and num != 0:
                continue
            if cols[i].button(str(num)):
                if len(st.session_state.age_input) < 2:
                    st.session_state.age_input += str(num)

# PC typing allowed
if not is_mobile:
    st.session_state.age_input = st.text_input("Enter Age", st.session_state.age_input, max_chars=2)

# Validate age
if st.session_state.age_input and (not st.session_state.age_input.isdigit() or int(st.session_state.age_input) > 80):
    st.session_state.age_input = ""

# Gender selection
colM, colF = st.columns(2)
if colM.button("Male"):
    st.session_state.selected_gender = "Male"
if colF.button("Female"):
    st.session_state.selected_gender = "Female"

# Reset button
if st.button("Reset"):
    st.session_state.age_input = ""
    st.session_state.selected_gender = None

# Results
if st.session_state.age_input.isdigit() and st.session_state.selected_gender:
    age = int(st.session_state.age_input)
    gender = st.session_state.selected_gender
    if 18 <= age <= 45:
        plan = "IA"
        price = male_ia_prices[age] if gender == "Male" else female_ia_prices[age]
        sh = male_sh_prices[age] if gender == "Male" else female_sh_prices[age]
        bundle = price + sh
        st.markdown(f"**{plan}${price} | SH${sh}<br>BUNDLE${bundle}**", unsafe_allow_html=True)
    elif 46 <= age <= 64:
        plan = "TL"
        price = male_tl_prices[age] if gender == "Male" else female_tl_prices[age]
        sh = male_sh_prices[age] if gender == "Male" else female_sh_prices[age]
        bundle = price + sh
        st.markdown(f"**{plan}${price} | SH${sh}<br>BUNDLE${bundle}**", unsafe_allow_html=True)
    elif 65 <= age <= 80:
        fe_price = final_expense_prices[age][gender]
        st.markdown(f"**FE${fe_price}**", unsafe_allow_html=True)

# Character selection visuals
st.markdown("""
<div class="character-row">
  <div class="character-box">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Toiletsign_male.svg/1200px-Toiletsign_male.svg.png" class="character-img">
    <div><input type="text" placeholder="Quote" style="width:80px; border:1px solid #00f; background:#111; color:white; text-align:center;"></div>
  </div>
  <div class="character-box">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Toiletsign_female.svg/1200px-Toiletsign_female.svg.png" class="character-img">
    <div><input type="text" placeholder="Quote" style="width:80px; border:1px solid #f0f; background:#111; color:white; text-align:center;"></div>
  </div>
</div>
""", unsafe_allow_html=True)
