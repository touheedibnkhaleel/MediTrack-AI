import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

from geopy.geocoders import Nominatim

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MediTrack AI",
    page_icon="🏥",
    layout="wide"
)

# ---------------- CUSTOM THEME HEADER ----------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        text-align: center;
        font-weight: bold;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        text-align: center;
        color: gray;
        font-size: 16px;
        margin-bottom: 20px;
    }

    .card {
        background-color: #111827;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
    }
    </style>

    <div class="main-title">🏥 MediTrack AI Healthcare System</div>
    <div class="sub-title">Analytics • Intelligence • Prediction Engine</div>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD DATA ----------------
@st.cache_data(show_spinner=False)
def load_data():
    conn = sqlite3.connect("Medi.db")

    df = pd.read_sql_query("""
    SELECT 
        a.*,
        d.department,
        d.level,
        p.is_returning,
        c.clinic_name,
        ci.city_name
    FROM appointment_transactions a
    JOIN doctor_master d ON a.doctor_id = d.doctor_id
    JOIN patient_master p ON a.patient_id = p.patient_id
    JOIN clinic_master c ON d.clinic_id = c.clinic_id
    JOIN city_master ci ON c.city_id = ci.city_id
    """, conn)

    conn.close()
    return df


# ---------------- MAP FUNCTION (SAFE + FAST) ----------------
@st.cache_data(show_spinner=False)
def get_coordinates(clinic_name, city_name):
    geolocator = Nominatim(user_agent="meditrack_app")

    try:
        location = geolocator.geocode(f"{clinic_name}, {city_name}, Pakistan")
        if location:
            return location.latitude, location.longitude
    except:
        pass

    return None, None


# ---------------- LIMITED GEOCODING (IMPORTANT FIX) ----------------
@st.cache_data(show_spinner=False)
def add_coordinates(df):
    df = df.copy()

    # ONLY unique clinics (NOT full dataset)
    unique = df[["clinic_name", "city_name"]].drop_duplicates().head(15)

    lat_map = {}
    lon_map = {}

    for _, row in unique.iterrows():
        lat, lon = get_coordinates(row["clinic_name"], row["city_name"])
        lat_map[(row["clinic_name"], row["city_name"])] = lat
        lon_map[(row["clinic_name"], row["city_name"])] = lon

    df["lat"] = df.apply(lambda x: lat_map.get((x["clinic_name"], x["city_name"])), axis=1)
    df["lon"] = df.apply(lambda x: lon_map.get((x["clinic_name"], x["city_name"])), axis=1)

    return df


# ---------------- RUN DATA ----------------
with st.spinner("Loading data..."):
    df = load_data()

# ⚡ FIX: light map only (no full freeze)
df = add_coordinates(df)

map_df = df.dropna(subset=["lat", "lon"])


# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🎛 Filters")

city_filter = st.sidebar.multiselect(
    "City",
    df["city_name"].unique(),
    df["city_name"].unique()
)

dept_filter = st.sidebar.multiselect(
    "Department",
    df["department"].unique(),
    df["department"].unique()
)

status_filter = st.sidebar.multiselect(
    "Status",
    df["status"].unique(),
    df["status"].unique()
)

filtered_df = df[
    (df["city_name"].isin(city_filter)) &
    (df["department"].isin(dept_filter)) &
    (df["status"].isin(status_filter))
]

# ---------------- KPI SECTION ----------------
st.markdown("## 📊 Business Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
    <h2>📅 {len(filtered_df)}</h2>
    <p>Total Appointments</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    revenue = filtered_df[filtered_df['status']=='completed']['fee'].sum()
    st.markdown(f"""
    <div class="card">
    <h2>💰 {revenue:,}</h2>
    <p>Total Revenue</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    noshow = (filtered_df['status']=='no-show').mean()*100
    st.markdown(f"""
    <div class="card">
    <h2>⚠️ {noshow:.2f}%</h2>
    <p>No-show Rate</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- CITY ----------------
st.markdown("## 🌍 City Performance")
st.bar_chart(filtered_df["city_name"].value_counts())

st.divider()

# ---------------- MAP ----------------
st.markdown("## 🗺 Clinic Locations (Map View)")
st.map(map_df[["lat", "lon"]])

st.divider()

# ---------------- DEPARTMENT ----------------
st.markdown("## 🏥 Department Revenue")
st.bar_chart(filtered_df.groupby("department")["fee"].sum())

st.divider()

# ---------------- LOSS ----------------
st.markdown("## 💸 Revenue Loss Insight")

loss = filtered_df[filtered_df['status']=='no-show']['fee'].sum()

st.markdown(f"""
<div style="
    background: linear-gradient(90deg,#ff9966,#ff5e62);
    padding:20px;
    border-radius:12px;
    text-align:center;
    color:white;
    font-size:20px;">
    Total Revenue Loss due to No-shows:
    <b>{loss:,} PKR</b>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- HEATMAP ----------------
st.markdown("## 🔥 Patient Flow Heatmap")

heatmap = filtered_df.pivot_table(
    index="appointment_day",
    columns="appointment_hour",
    values="appointment_id",
    aggfunc="count"
).fillna(0)

fig, ax = plt.subplots()
sns.heatmap(heatmap, ax=ax, cmap="coolwarm")
st.pyplot(fig)

st.divider()

# ---------------- ML MODEL ----------------
st.markdown("## 🤖 AI Prediction Engine")

ml = filtered_df.copy()
ml["target"] = (ml["status"] == "no-show").astype(int)

le_dept = LabelEncoder()
le_day = LabelEncoder()

ml["department"] = le_dept.fit_transform(ml["department"])
ml["appointment_day"] = le_day.fit_transform(ml["appointment_day"])

X = ml[[
    "appointment_hour",
    "appointment_month",
    "department",
    "appointment_day",
    "is_returning"
]]

y = ml["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

st.success(f"Model Accuracy: {model.score(X_test, y_test):.2f}")

# ---------------- PREDICTION ----------------
st.markdown("### 🔮 Predict No-show Risk")

c1, c2, c3 = st.columns(3)

hour = c1.slider("Hour", 9, 20)
month = c2.slider("Month", 1, 12)
dept = c3.selectbox("Department", le_dept.classes_)

c4, c5 = st.columns(2)

day = c4.selectbox("Day", le_day.classes_)
ret = c5.selectbox("Returning Patient", [0, 1])

if st.button("Predict"):
    pred = model.predict([[hour, month,
                           le_dept.transform([dept])[0],
                           le_day.transform([day])[0],
                           ret]])[0]

    if pred == 1:
        st.error("⚠️ High Risk of No-show")
    else:
        st.success("✅ Patient Likely to Attend")