import streamlit as st
import datetime
import requests
import json
from openai import OpenAI

# Premium Mobile iOS Layout Configuration
st.set_page_config(
    page_title="Namma Health Pro",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Premium Luxury Theme Stylesheet
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp {
        background-color: #0b0f19 !important;
        font-family: 'SF Pro Display', -apple-system, sans-serif !important;
        color: #f3f4f6 !important;
    }
    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        font-size: 28px !important;
        padding-bottom: 5px !important;
    }
    h2, h3, h4, h5 {
        color: #9ca3af !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    div[data-form="true"] {
        background: linear-gradient(145deg, #111827, #1f2937) !important;
        border: 1px solid #374151 !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3) !important;
    }
    div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        height: 48px !important;
    }
    label p {
        color: #e5e7eb !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 6px !important;
    }
    button[kind="primaryFormSubmit"], button[data-testid="baseButton-secondary"], button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 14px !important;
        height: 50px !important;
        width: 100% !important;
        font-size: 16px !important;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.4) !important;
    }
    div[data-testid="stMetric"] {
        background: #111827 !important;
        border: 1px solid #374151 !important;
        padding: 16px !important;
        border-radius: 16px !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #3b82f6 !important;
        font-weight: 700 !important;
    }
    .plan-card {
        background: #111827; 
        border-radius: 14px; 
        padding: 18px; 
        border: 1px solid #2563eb; 
        margin-bottom: 15px;
    }
    
    .user-bubble { background-color: #2563eb; color: white; padding: 12px; border-radius: 14px 14px 0px 14px; margin-bottom: 10px; max-width: 85%; margin-left: auto; text-align: left; }
    .ai-bubble { background-color: #1f2937; color: #f3f4f6; padding: 12px; border-radius: 14px 14px 14px 0px; margin-bottom: 10px; max-width: 85%; border: 1px solid #374151; }
    </style>
""", unsafe_allow_html=True)

# Fetching Data Using Clean Requests Library instead of Urllib
@st.cache_data(ttl=3600)
def fetch_live_food_data(barcode, fallback_name, c_100, p_100, cb_100, f_100):
    try:
        url = f"https://openfoodfacts.org{barcode}.json"
        response = requests.get(url, headers={'User-Agent': 'NammaHealthPro - iOS - Version 6.0'}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                prod = data["product"]
                nutriments = prod.get("nutriments", {})
                return {
                    "name": prod.get("product_name", fallback_name),
                    "calories_100g": int(nutriments.get("energy-kcal_100g", c_100)),
                    "protein_100g": round(float(nutriments.get("proteins_100g", p_100)), 1),
                    "carbs_100g": round(float(nutriments.get("carbohydrates_100g", cb_100)), 1),
                    "fats_100g": round(float(nutriments.get("fat_100g", f_100)), 1)
                }
    except Exception:
        pass
    return {"name": fallback_name, "calories_100g": c_100, "protein_100g": p_100, "carbs_100g": cb_100, "fats_100g": f_100}

# Local Food Catalog Configuration
food_catalog = {
    "Carbohydrates": {
        "Rolled Oats": {"barcode": "7311150031206", "c": 389, "p": 16.9, "cb": 66.3, "f": 6.9},
        "Sona Masuri Brown Rice": {"barcode": "8901552011117", "c": 111, "p": 2.6, "cb": 23.0, "f": 0.9},
        "Whole Wheat Chapati": {"barcode": "8901725181210", "c": 264, "p": 9.1, "cb": 48.0, "f": 3.2},
        "Ragi Flour (Millet Base)": {"barcode": "8904014404751", "c": 328, "p": 7.3, "cb": 72.0, "f": 1.3}
    },
    "Proteins": {
        "Fresh Paneer": {"barcode": "8901262140411", "c": 265, "p": 18.3, "cb": 1.2, "f": 20.8},
        "Lean Chicken Breast": {"barcode": "8906046960039", "c": 165, "p": 31.0, "cb": 0.0, "f": 3.6},
        "Whole Eggs": {"barcode": "8908007539034", "c": 155, "p": 13.0, "cb": 1.1, "f": 11.0},
        "Organic Tofu": {"barcode": "8906013340116", "c": 144, "p": 14.0, "cb": 2.5, "f": 8.0},
        "Thick Yellow Dal / Sambhar": {"barcode": "8901552000302", "c": 343, "p": 22.0, "cb": 60.0, "f": 1.5}
    },
    "Snacks": {
        "Roasted Almonds & Cashews": {"barcode": "8906105632228", "c": 579, "p": 21.0, "cb": 22.0, "f": 49.0},
        "Roasted Chana (Chickpeas)": {"barcode": "8906014401156", "c": 364, "p": 19.0, "cb": 58.0, "f": 5.0}
    }
}

st.title("🩺 Namma Health Pro Studio")
st.markdown("##### Interactive Engine & AI Health Coach")

with st.form("interactive_health_form"):
    st.markdown("### 👤 Step 1: Core Metrics")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (Years)", min_value=1, max_value=120, value=40)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        height_cm = st.number_input("Height (cm)", min_value=50, max_value=250, value=175)
        weight_kg = st.number_input("Weight (kg)", min_value=10, max_value=300, value=62)
        
    st.markdown("---")
    st.markdown("### 🗺️ Step 2: Location Profile")
    location = st.selectbox("Geographic Hub", ["Bengaluru, India (ORR / Whitefield IT Belt)", "Other Global Locations"])

    submit_btn = st.form_submit_button("CALIBRATE APP ENGINE")

if submit_btn or 'interactive_calculated' in st.session_state:
    st.session_state['interactive_calculated'] = True
    
    if gender == "Female":
        bmr = int(447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age))
    else:
        bmr = int(88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age))
        
    tdee = int(bmr * 1.375)  
    caloric_target = tdee + 350
    
    protein_target_g = int((caloric_target * 0.30) / 4)
    carb_target_g = int((caloric_target * 0.45) / 4)
    fat_target_g = int((caloric_target * 0.25) / 9)

    st.markdown("---")
    st.markdown("### 📊 Energy Blueprint Results")
    m_col1, m_col2 = st.columns(2)
    with m_col1: st.metric(label="Basal Energy (BMR)", value=f"{bmr} kcal")
    with m_col2: st.metric(label="Clean Gain Target", value=f"{caloric_target} kcal")

    # Step 3: Interactive Food Exchanges (All 4 meal selectors included)
    st.markdown("---")
    st.markdown("### 🥞 Step 3: Interactive Food Exchanges")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        bf_carb_choice = st.selectbox("Breakfast Carb Source", list(food_catalog["Carbohydrates"].keys()), index=0)
        bf_prot_choice = st.selectbox("Breakfast Protein Source", list(food_catalog["Proteins"].keys()), index=2)
        lunch_carb_choice = st.selectbox("Lunch Carb Source", list(food_catalog["Carbohydrates"].keys()), index=1)
        lunch_prot_choice = st.selectbox("Lunch Protein Source", list(food_catalog["Proteins"].keys()), index=1)
    with col_sel2:
        snack_choice = st.selectbox("Desk Drawer Snack Choice", list(food_catalog["Snacks"].keys()), index=0)
        dinner_carb_choice = st.selectbox("Dinner Carb Source", list(food_catalog["Carbohydrates"].keys()), index=2)
        dinner_prot_choice = st.selectbox("Dinner Protein Source", list(food_catalog["Proteins"].keys()), index=0)

    # API Queries for selected data strings
    c_bf_meta = food_catalog["Carbohydrates"][bf_carb_choice]
    p_bf_meta = food_catalog["Proteins"][bf_prot_choice]
    bf_carb_api = fetch_live_food_data(c_bf_meta["barcode"], bf_carb_choice, c_bf_meta["c"], c_bf_meta["p"], c_bf_meta["cb"], c_bf_meta["f"])
    bf_prot_api = fetch_live_food_data(p_bf_meta["barcode"], bf_prot_choice, p_bf_meta["c"], p_bf_meta["p"], p_bf_meta["cb"], p_bf_meta["f"])

    c_ln_meta = food_catalog["Carbohydrates"][lunch_carb_choice]
    p_ln_meta = food_catalog["Proteins"][lunch_prot_choice]
    ln_carb_api = fetch_live_food_data(c_ln_meta["barcode"], lunch_carb_choice, c_ln_meta["c"], c_ln_meta["p"], c_ln_meta["cb"], c_ln_meta["f"])
    ln_prot_api = fetch_live_food_data(p_ln_meta["barcode"], lunch_prot_choice, p_ln_meta["c"], p_ln_meta["p"], p_ln_meta["cb"], p_ln_meta["f"])

    snk_meta = food_catalog["Snacks"][snack_choice]
    snack_api = fetch_live_food_data(snk_meta["barcode"], snack_choice, snk_meta["c"], snk_meta["p"], snk_meta["cb"], snk_meta["f"])

    c_dn_meta = food_catalog["Carbohydrates"][dinner_carb_choice]
    p_dn_meta = food_catalog["Proteins"][dinner_prot_choice]
    dn_carb_api = fetch_live_food_data(c_dn_meta["barcode"], dinner_carb_choice, c_dn_meta["c"], c_dn_meta["p"], c_dn_meta["cb"], c_dn_meta["f"])
    dn_prot_api = fetch_live_food_data(p_dn_meta["barcode"], dinner_prot_choice, p_dn_meta["c"], p_dn_meta["p"], p_dn_meta["cb"], p_dn_meta["f"])

    # Gram Portion Weight Math (Calorie distribution split: 25% BF, 35% Lunch, 15% Snack, 25% Dinner)
    calc_bf_carb_g = int((carb_target_g * 0.25) / (max(bf_carb_api["carbs_100g"], 1) / 100))
    calc_bf_prot_g = int((protein_target_g * 0.25) / (max(bf_prot_api["protein_100g"], 1) / 100))
    
    calc_ln_carb_g = int((carb_target_g * 0.35) / (max(ln_carb_api["carbs_100g"], 1) / 100))
    calc_ln_prot_g = int((protein_target_g * 0.35) / (max(ln_prot_api["protein_100g"], 1) / 100))
    
    calc_snack_g = int((caloric_target * 0.15) / (max(snack_api["calories_100g"], 1) / 100))
    
    calc_dn_carb_g = int((carb_target_g * 0.25) / (max(dn_carb_api["carbs_100g"], 1) / 100))
    calc_dn_prot_g = int((protein_target_g * 0.25) / (max(dn_prot_api["protein_100g"], 1) / 100))

    # Complete 4-Meal Plan Output Cards Render Block
    st.markdown("### 📋 Your Balanced Meal Portions")
    st.markdown(f"""
    <div class="plan-card">
        <h4 style="color: #3b82f6; margin-top: 0;">🌅 Morning Breakfast Target</h4>
        <p style="color: #e5e7eb; margin-bottom: 0;">• Consume <b>{calc_bf_carb_g}g</b> of {bf_carb_api['name']} paired with <b>{calc_bf_prot_g}g</b> of {bf_prot_api['name']}.</p>
    </div>
    <div class="plan-card">
        <h4 style="color: #3b82f6; margin-top: 0;">🍱 Office Lunch Target</h4>
        <p style="color: #e5e7eb; margin-bottom: 0;">• Consume <b>{calc_ln_carb_g}g</b> of {ln_carb_api['name']} paired with <b>{calc_ln_prot_g}g</b> of {ln_prot_api['name']}. Add 1.5 tbsp Ghee to rice grains.</p>
    </div>
    <div class="plan-card">
        <h4 style="color: #3b82f6; margin-top: 0;">🥜 Tech-Park Desk Snack</h4>
        <p style="color: #e5e7eb; margin-bottom: 0;">• Keep at desk and measure out <b>{calc_snack_g}g</b> of {snack_api['name']} during afternoon operational calls.</p>
    </div>
    <div class="plan-card">
        <h4 style="color: #3b82f6; margin-top: 0;">🍽️ Balanced Evening Dinner Target</h4>
        <p style="color: #e5e7eb; margin-bottom: 0;">• Consume <b>{calc_dn_carb_g}g</b> of {dn_carb_api['name']} balanced with <b>{calc_dn_prot_g}g</b> of {dn_prot_api['name']} to maintain structural amino recovery.</p>
    </div>
    """, unsafe_allow_html=True)

    # Restored Home Workout Module Block
    st.markdown("---")
    st.markdown("### 🏠 45-Min Postural & Home Workout Log")
    st.caption("Target tracking variables to activate dead glutes, adjust desk slouching, and protect joints.")
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        st.markdown("##### 🦵 Lower Body (Spinal Safety Target)")
        st.number_input("Leg Press / Dumbbell Goblet Squats (kg)", min_value=5, value=25, key="h_ex1")
        st.caption("_3 Sets × 10 Reps (Protects lumbar vertebrae from keyboard-sitting posture strain)_")
        st.number_input("Dumbbell Romanian Deadlifts (kg)", min_value=5, value=16, key="h_ex2")
        st.caption("_3 Sets × 12 Reps (Awakens posterior chains and hip flexibility metrics)_")
    with w_col2:
        st.markdown("##### 💪 Upper Body (Postural Alignment Correction)")
        st.number_input("Dumbbell Floor / Chest Press (kg per hand)", min_value=4, value=12, key="h_ex3")
        st.caption("_3 Sets × 10 Reps (Safe shoulder glenohumeral motion parameters)_")
        st.number_input("Seated Rows / Banded Lat Pull-Downs (kg)", min_value=10, value=30, key="h_ex4")
        st.caption("_3 Sets × 12 Reps (Directly counteracts tech-desk rounded shoulders)_")

    if location == "Bengaluru, India (ORR / Whitefield IT Belt)":
        st.markdown("---")
        st.markdown("""
        <div style="background-color: #1e1b4b; border-left: 5px solid #818cf8; padding: 18px; border-radius: 12px;">
            <p style="color: #c7d2fe; font-size: 14px; line-height: 1.6; margin-bottom: 0;">
                ⚠️ <b>IT Hub Epidemiological Warning</b>: Clinical audits track that <b>77% of Bengaluru tech professionals</b> experience active Vitamin D3 reductions due to indoor shifts. Balance this by taking walking meetings or using short standing-break intervals during long computer shifts.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Section 4: Live GPT Chat Core Interface System
    st.markdown("---")
    st.markdown("### 💬 Chat with Your AI Hypertrophy Coach")
    st.caption("Discuss your calculations, target meal portions, or posture exercises.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": f"Hello! I am your custom Health Coach. I see you are {age} years old, weigh {weight_kg}kg, live in {location.split(',')}, and want to achieve a target of {caloric_target} kcal/day. How can I assist you with your diet or exercises today?"}
        ]

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble">🤖 {message["content"]}</div>', unsafe_allow_html=True)

    user_query = st.chat_input("Type your question here...")

    if user_query:
        st.markdown(f'<div class="user-bubble">{user_query}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        api_key = st.secrets.get("OPENAI_API_KEY", "")

        if not api_key:
            ai_response = "⚠️ App Configuration Note: Please add your `OPENAI_API_KEY` inside your Streamlit Cloud Secrets dashboard."
        else:
            try:
                client = OpenAI(api_key=api_key.strip())
                system_prompt = f"You are an expert sports nutritionist and strength coach assisting a {age}-year-old male user. Weight: {weight_kg}kg, Height: {height_cm}cm, Location: {location}. Target Calories: {caloric_target}kcal, Target Protein: {protein_target_g}g. Provide actionable, concise health guidance. Keep answers short and optimal for reading on an iPhone mobile screen."
                
                messages_payload = [{"role": "system", "content": system_prompt}]
                for h in st.session_state.chat_history[-5:]:
                    messages_payload.append({"role": h["role"], "content": h["content"]})

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages_payload,
                    temperature=0.7
                )
                ai_response = response.choices.message.content
                    
            except Exception as e:
                ai_response = f"Official Gateway Connection Error: {str(e)}"

        st.markdown(f'<div class="ai-bubble">🤖 {ai_response}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
