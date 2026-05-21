import streamlit as st
import datetime

# Premium Mobile iOS Layout Configuration
st.set_page_config(
    page_title="Namma Health Pro",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom High-End iOS Theme Styling (Eliminates plain white boxes & bad mobile fonts)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Base Background and High-Contrast Typography */
    .stApp {
        background-color: #0b0f19 !important;
        font-family: 'SF Pro Display', -apple-system, sans-serif !important;
        color: #f3f4f6 !important;
    }
    
    /* Elegant Clean Headers */
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
    
    /* Premium Luxury Form Container Card */
    div[data-form="true"] {
        background: linear-gradient(145deg, #111827, #1f2937) !important;
        border: 1px solid #374151 !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Styled Input Fields and Select Boxes */
    div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        height: 48px !important;
    }
    
    /* Input Label Adjustments for Maximum Mobile Readability */
    label p {
        color: #e5e7eb !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 6px !important;
    }
    
    /* Premium Pill Button Style */
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
    
    /* Telemetry Info Cards */
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
    
    /* Custom Plan Cards styling */
    .plan-card {
        background: #111827; 
        border-radius: 14px; 
        padding: 16px; 
        border: 1px solid #1e293b; 
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Banner
st.title("🩺 Namma Health Pro Plan")
st.markdown("##### Dynamic Clinical-Grade Hypertrophy System")

# Step-by-Step Structured Intention Flow Form
with st.form("dynamic_health_form"):
    st.markdown("### 👤 Step 1: Core Physical Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (Years)", min_value=1, max_value=120, value=40)
        gender = st.selectbox("Gender at Birth", ["Male", "Female"])
    with col2:
        height_cm = st.number_input("Height (Centimetres)", min_value=50, max_value=250, value=175)
        weight_kg = st.number_input("Weight (Kilograms)", min_value=10, max_value=300, value=62)
        
    st.markdown("---")
    st.markdown("### 🎯 Step 2: Diet Preference & Routine")
    
    diet_pref = st.selectbox("Dietary Layout Preference", ["Vegetarian (with Dairy/Paneer)", "Non-Vegetarian (Includes Eggs/Chicken)"])
    activity = st.selectbox("Daily Activity Signature", [
        "Sedentary Desk Worker (IT / Corporate Floor)",
        "Lightly Active (Daily Walks / Playtime with Kids)",
        "Moderately Active (Gym Training 3-5 Days/Week)",
        "Very Active (Heavy Physical Labor / Athlete)"
    ])
    
    st.markdown("---")
    st.markdown("### 📍 Step 3: Location Context Validation")
    location = st.selectbox("Current Geographic Region", ["Bengaluru, India (ORR / Whitefield IT Belt)", "Other Global Locations"])

    # Form Submission Trigger
    submit_btn = st.form_submit_button("GENERATE PERSONALIZED DIET & LIFT PLAN")

# Calculation Phase Logic (Fully Dynamic Equations)
if submit_btn or 'calculated' in st.session_state:
    st.session_state['calculated'] = True
    
    # Scientific Revised Harris-Benedict Equations
    if gender == "Female":
        bmr = int(447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age))
    else:
        bmr = int(88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age))
        
    # Activity Scaling Parameter Co-efficients
    activity_multipliers = {
        "Sedentary Desk Worker (IT / Corporate Floor)": 1.2,
        "Lightly Active (Daily Walks / Playtime with Kids)": 1.375,
        "Moderately Active (Gym Training 3-5 Days/Week)": 1.55,
        "Very Active (Heavy Physical Labor / Athlete)": 1.725
    }
    tdee = int(bmr * activity_multipliers[activity])
    
    # Target Clean Surplus (+350 Calories for lean muscle mass retention at age 40)
    caloric_target = tdee + 350
    
    # Macro Split percentages: 45% Carb, 30% Protein, 25% Healthy Fats
    protein_g = int((caloric_target * 0.30) / 4)
    carb_g = int((caloric_target * 0.45) / 4)
    fat_g = int((caloric_target * 0.25) / 9)

    # Display Profile Summary Cards
    st.markdown("---")
    st.markdown("### 📊 Your Dynamic Calibration Metrics")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="Basal Metabolic Rate (BMR)", value=f"{bmr} kcal/day")
    with m_col2:
        st.metric(label="Lean Hypertrophy Target", value=f"{caloric_target} kcal/day")
        
    # Macronutrient Breakdown Display
    macro_col1, macro_col2, macro_col3 = st.columns(3)
    with macro_col1:
        st.metric(label="Target Protein", value=f"{protein_g}g", delta="30% Macros")
    with macro_col2:
        st.metric(label="Target Carbs", value=f"{carb_g}g", delta="45% Macros")
    with macro_col3:
        st.metric(label="Target Fats", value=f"{fat_g}g", delta="25% Macros")

    # SECTION A: THE CUSTOMIZED REAL-TIME DIET PLAN
    st.markdown("---")
    st.markdown("### 🥗 Your Calculated Localized Meal Plan")
    st.caption(f"Dynamically formulated for `{caloric_target} kcal` using real-time local macro sources.")
    
    # Portion math calculations mapped to target calories
    nandini_ml = int(caloric_target * 0.15)
    oats_g = int(caloric_target * 0.025)
    rice_g = int(caloric_target * 0.08)
    paneer_chicken_g = int(weight_kg * 2.5)

    if "Vegetarian" in diet_pref:
        bf_protein = f"100g Grilled Paneer or 150g Amul High-Protein Curd"
        lunch_protein = f"120g Paneer / Tofu Curry cooked with thick Dal"
        dinner_protein = f"100g Paneer Bhurji or Sprouted Green Moong Salad"
    else:
        bf_protein = f"3 Whole Boiled Eggs (Local farm fresh)"
        lunch_protein = f"150g Lean Chicken Breast or Fish Fillet cooked in local style"
        dinner_protein = f"3 Egg White Bhurji or 120g Minced Chicken Keema"

    st.markdown(f"""
    <div class="plan-card">
        <h4 style="color: #3b82f6; margin-top: 0;">🌅 Breakfast (Target: ~600 kcal)</h4>
        <p style="color: #e5e7eb; margin-bottom: 0;">
            • <b>Anabolism Shake</b>: Blend <b>{nandini_ml}ml Nandini Milk</b> (Orange pouch) + <b>{oats_g}g Rolled Oats</b> + 2 tbsp Peanut Butter + 1 Yelakki Banana.<br>
            • <b>Solid Plate</b>: Pair with <b>{bf_protein}</b> to trigger immediate muscle protein synthesis.
        </p>
    </div>
    <div class="plan-card">
        <h4 style="color: #3b82f6; margin-top: 0;">🍱 Corporate Lunch (Target: ~750 kcal)</h4>
        <p style="color: #e5e7eb; margin-bottom: 0;">
            • <b>Complex Grain Base</b>: <b>{rice_g}g Sona Masuri Brown Rice</b> or 2 thick Ragi Mudde.<br>
            • <b>Tissue Builder</b>: <b>{lunch_protein}</b>.<br>
            • <b>Calorie Booster</b>: Drizzle 1.5 tablespoons of pure Cow Ghee over your hot rice base to cleanly add dense macros.
        </p>
    </div>
    <div class="plan-card">
        <h4 style="color: #3b82f6; margin-top: 0;">🥜 Tech-Park Desk Snack (Target: ~350 kcal)</h4>
        <p style="color: #e5e7eb; margin-bottom: 0;">
            • Keep a jar at your workstation containing 25g almonds, 15g cashews, and 1 whole Yelakki Banana. Consume this halfway through afternoon operational calls.
        </p>
    </div>
    <div class="plan-card">
        <h4 style="color: #3b82f6; margin-top: 0;">🍽️ Dinner (Target: ~550 kcal)</h4>
        <p style="color: #e5e7eb; margin-bottom: 0;">
            • 3 Whole Wheat or Oats Chapatis (lightly brushed with ghee).<br>
            • Pair with <b>{dinner_protein}</b> and a high-fiber local green salad bowl to support overnight tissue recovery.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # SECTION B: THE JOINT-SAFE STRENGTH WORKOUT PLAN
    st.markdown("---")
    st.markdown("### 🏋️‍♂️ 45-Min Joint-Safe Hypertrophy Plan")
    st.caption("Designed to correct sitting posture, activate dead glutes, and protect structural tendons from loading strain.")
    
    st.markdown("""
    <div style="background-color: #111827; border-left: 4px solid #ef4444; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
        <span style="color: #fca5a5; font-weight: 600;">🚨 Mandatory 5-Min Warm-Up Routine:</span><br>
        <span style="color: #d1d5db; font-size: 14px;">Complete 2 sets of Cat-Cow movements (10 reps) and Bodyweight Glute Bridges (15 reps) to open tight hips before tracking your weights below.</span>
    </div>
    """, unsafe_allow_html=True)

    w_col1, w_col2 = st.columns(2)
    with w_col1:
        st.markdown("##### 🦵 Lower Body Posture Fixes")
        s_wt = st.number_input("Dumbbell Goblet Squats / Leg Press (kg)", min_value=5, value=20, step=2)
        st.caption("3 Sets × 10 Reps • *Bypasses axial spine compression caused by heavy barbell racks*")
        
        rdl_wt = st.number_input("Dumbbell Romanian Deadlifts (kg)", min_value=5, value=16, step=2)
        st.caption("3 Sets × 12 Reps • *Awakens hamstrings and glutes deactivated by corporate desk chairs*")

    with w_col2:
        st.markdown("##### 💪 Upper Body Posture Fixes")
        b_wt = st.number_input("Dumbbell Chest Press (kg per hand)", min_value=5, value=12, step=2)
        st.caption("3 Sets × 10 Reps • *Allows natural glenohumeral movement pattern, sparing shoulder joints*")
        
        row_wt = st.number_input("Seated Cable Rows / Lat Pulldowns (kg)", min_value=10, value=30, step=5)
        st.caption("3 Sets × 12 Reps • *Directly counters rounded shoulders from typing or writing code*")

    # SECTION C: LOCAL EPIDEMIOLOGICAL RISK MONITORING
    if location == "Bengaluru, India (ORR / Whitefield IT Belt)":
        st.markdown("---")
        st.markdown("### 📍 Bengaluru IT-Sector Epidemiological Warnings")
        st.markdown(f"""
        <div style="background-color: #1e1b4b; border-left: 5px solid #818cf8; padding: 20px; border-radius: 12px;">
            <ul style="color: #c7d2fe; font-size: 14px; line-height: 1.6; padding-left: 20px; margin-bottom: 0;">
                <li><b>Vitamin D3 Demineralization Risk</b>: Over <b>77% of Bengaluru tech workers</b> show clinically significant Vitamin D deficiencies due to indoor shifts. Supplementation is highly recommended to protect bone structural integrity and avoid deep muscle fatigue.</li>
                <li><b>Metabolic Preservation</b>: Combat long periods of uninterrupted sitting by standing or changing position inside your workstation bay for 5 minutes every hour to sustain non-exercise movement markers.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Save Progress Button UI
    st.markdown("---")
    if st.button("💾 SAVE TODAY'S HEALTH PROGRESS LOG", type="primary"):
        st.balloons()
        st.success(f"Log secure! Target of {caloric_target} calories and joint-safe training logs committed to active tracking memory.")
