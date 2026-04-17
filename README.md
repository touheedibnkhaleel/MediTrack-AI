# MediTrack-AI
MediTrack AI is a healthcare analytics system that simulates hospital data to analyze appointments, revenue, and patient behavior. It features an interactive dashboard built with Streamlit to visualize key insights like no-show rates and department performance. The project also includes a machine learning model that predicts whether a patient will miss an appointment. A FastAPI backend is used for basic CRUD operations, and clinic locations are mapped for geographical insights. Overall, it demonstrates an end-to-end data pipeline combining analytics, visualization, and AI.

🧠 Key Features
📊 1. Business Intelligence Dashboard
Total Appointments tracking
Revenue calculation
No-show rate monitoring
Department-wise revenue analysis
City-wise performance insights
💸 2. Revenue Loss Analysis
Calculates financial loss due to missed appointments
Highlights operational inefficiencies
🔥 3. Patient Flow Heatmap
Visualizes peak hours and busy days
Helps understand hospital workload distribution
🗺 4. Clinic Location Mapping
Displays clinic locations on a map using latitude & longitude
Helps visualize geographical distribution of healthcare services
🤖 5. AI Prediction Engine
Machine Learning model predicts whether a patient will:
Attend appointment ✅
Miss appointment (No-show) ⚠️
Helps in proactive decision-making
🌐 6. REST API (FastAPI)
Add new patients
View patient records
Update appointment status
Delete appointments
🏗️ Project Architecture
generate_data.py   → Creates synthetic healthcare dataset (SQLite)
api.py             → FastAPI backend (CRUD operations)
app.py             → Streamlit dashboard + ML model
🛠️ Technologies Used
🐍 Programming Language
Python
📊 Data Analysis & Visualization
Pandas
Matplotlib
Seaborn
🤖 Machine Learning
Scikit-learn (Random Forest Classifier)
🌐 Backend API
FastAPI
Uvicorn
📊 Frontend Dashboard
Streamlit
🗄️ Database
SQLite
🗺️ Mapping
Geopy (OpenStreetMap / Nominatim)
