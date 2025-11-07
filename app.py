import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate soil health score
def calculate_soil_health(ph, moisture, microbial_activity, humidity, contamination):
    # Normalize values (assuming ranges: pH 0-14, moisture 0-100%, microbial 0-100, humidity 0-100%, contamination 0-100)
    ph_score = 100 - abs(ph - 7) * 10  # Optimal pH around 7
    moisture_score = moisture  # Assuming 0-100%
    microbial_score = microbial_activity  # Assuming 0-100%
    humidity_score = humidity  # Assuming 0-100%
    contamination_score = 100 - contamination  # Lower contamination is better

    # Overall health score (weighted average)
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # Equal weights for simplicity
    scores = [ph_score, moisture_score, microbial_score, humidity_score, contamination_score]
    overall_score = np.average(scores, weights=weights)

    return overall_score, ph_score, moisture_score, microbial_score, humidity_score, contamination_score

# Function to detect contamination level
def detect_contamination(contamination):
    if contamination < 20:
        return "Low"
    elif contamination < 50:
        return "Moderate"
    else:
        return "High"

# Function to recommend crops based on soil health
def recommend_crops(overall_score, ph, moisture):
    recommendations = []
    if overall_score > 70:
        if ph >= 6 and ph <= 8:
            if moisture > 50:
                recommendations = ["Rice", "Sugarcane", "Wheat"]
            else:
                recommendations = ["Maize", "Soybean", "Cotton"]
        else:
            recommendations = ["Adjust pH first"]
    else:
        recommendations = ["Improve soil health: Add organic matter, reduce contamination"]
    return recommendations

# Streamlit app
st.title("Soil Health Monitoring App")

st.sidebar.header("Input Soil Parameters")

ph = st.sidebar.slider("Soil pH", 0.0, 14.0, 7.0)
moisture = st.sidebar.slider("Soil Moisture (%)", 0.0, 100.0, 50.0)
microbial_activity = st.sidebar.slider("Microbial Activity (%)", 0.0, 100.0, 70.0)
humidity = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 60.0)
contamination = st.sidebar.slider("Contamination Level (%)", 0.0, 100.0, 10.0)

if st.sidebar.button("Analyze Soil Health"):
    overall_score, ph_score, moisture_score, microbial_score, humidity_score, contamination_score = calculate_soil_health(ph, moisture, microbial_activity, humidity, contamination)
    contamination_level = detect_contamination(contamination)
    recommendations = recommend_crops(overall_score, ph, moisture)

    st.header("Soil Health Results")
    st.write(f"Overall Soil Health Score: {overall_score:.2f}/100")

    # Display individual scores
    st.subheader("Parameter Scores")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("pH Score", f"{ph_score:.2f}")
        st.metric("Moisture Score", f"{moisture_score:.2f}")
    with col2:
        st.metric("Microbial Activity Score", f"{microbial_score:.2f}")
        st.metric("Humidity Score", f"{humidity_score:.2f}")
    with col3:
        st.metric("Contamination Score", f"{contamination_score:.2f}")
        st.metric("Contamination Level", contamination_level)

    # Recommendations
    st.subheader("Recommended Crops")
    if recommendations:
        for crop in recommendations:
            st.write(f"- {crop}")
    else:
        st.write("No specific recommendations available.")

    # Visualization
    st.subheader("Soil Health Visualization")
    fig, ax = plt.subplots()
    parameters = ['pH', 'Moisture', 'Microbial', 'Humidity', 'Contamination']
    scores = [ph_score, moisture_score, microbial_score, humidity_score, contamination_score]
    ax.bar(parameters, scores, color=['blue', 'green', 'red', 'purple', 'orange'])
    ax.set_ylabel('Score')
    ax.set_title('Soil Parameter Scores')
    st.pyplot(fig)