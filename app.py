
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from remediation import analyze_soil


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SoilSense AI",
    page_icon="🌱",
    layout="wide"
)

MODEL_PATH = Path(__file__).with_name("crop_model.pkl")

FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]


# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.markdown(
    """
    <h1 style="color:#2E7D32;">
        🌱 SoilSense AI
    </h1>

    <h3>
        Real-Time Intelligence for Soil Nutrient
        Evaluation and Ecosystem Remediation
    </h3>

    <p>
        An intelligent soil analysis platform combining
        machine learning, soil evaluation, crop prediction,
        and ecosystem remediation recommendations.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# MODEL AVAILABILITY
# --------------------------------------------------

if not MODEL_PATH.exists():
    st.error(
        "Trained model not found. Run "
        "'python train_model.py' first."
    )
    st.stop()

try:
    model = load_model()
except Exception as error:
    st.error(f"Unable to load the trained model: {error}")
    st.stop()


# --------------------------------------------------
# SIDEBAR: SOIL INPUTS
# --------------------------------------------------

st.sidebar.header("🧪 Soil Parameters")

st.sidebar.caption(
    "Enter soil measurements using the conventions "
    "of the training dataset."
)

n = st.sidebar.number_input(
    "Nitrogen (N)",
    min_value=0.0,
    max_value=300.0,
    value=90.0
)

p = st.sidebar.number_input(
    "Phosphorus (P)",
    min_value=0.0,
    max_value=300.0,
    value=42.0
)

k = st.sidebar.number_input(
    "Potassium (K)",
    min_value=0.0,
    max_value=300.0,
    value=43.0
)

ph = st.sidebar.number_input(
    "Soil pH",
    min_value=0.0,
    max_value=14.0,
    value=6.5,
    step=0.1
)

st.sidebar.divider()

st.sidebar.header("🌦️ Growing Conditions")

temperature = st.sidebar.number_input(
    "Temperature (°C)",
    min_value=-10.0,
    max_value=60.0,
    value=25.0
)

humidity = st.sidebar.number_input(
    "Humidity (%)",
    min_value=0.0,
    max_value=100.0,
    value=80.0
)

rainfall = st.sidebar.number_input(
    "Rainfall (mm)",
    min_value=0.0,
    max_value=5000.0,
    value=200.0
)

st.sidebar.divider()

analyze = st.sidebar.button(
    "🔍 Analyze Soil",
    type="primary",
    use_container_width=True
)

st.sidebar.caption(
    "This prototype analyzes manually entered values. "
    "Results appear immediately after submission."
)


# --------------------------------------------------
# INTRODUCTION
# --------------------------------------------------

st.info(
    "The system evaluates supplied soil measurements, "
    "predicts crops using a trained ML model, and generates "
    "rule-based remediation suggestions. It does not use "
    "live sensors or independently confirm soil deficiencies."
)


# --------------------------------------------------
# INITIAL SCREEN
# --------------------------------------------------

if not analyze:

    st.subheader("Welcome to SoilSense AI")

    st.write(
        "Enter the soil parameters in the sidebar and "
        "click Analyze Soil to generate your report."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🧪 Soil Evaluation")
        st.write(
            "Examine NPK measurements and interpret "
            "soil acidity or alkalinity."
        )

    with col2:
        st.markdown("### 🌾 Crop Intelligence")
        st.write(
            "Predict suitable crop categories using "
            "a trained machine learning model."
        )

    with col3:
        st.markdown("### 🌍 Ecosystem Remediation")
        st.write(
            "Explore potential soil improvement measures "
            "and environmental considerations."
        )

    st.stop()


# --------------------------------------------------
# VALIDATE INPUTS
# --------------------------------------------------

if not 0 <= ph <= 14:
    st.error("Please enter a valid soil pH value.")
    st.stop()

if not all(
    np.isfinite(value)
    for value in [
        n, p, k, ph,
        temperature, humidity, rainfall
    ]
):
    st.error("All input values must be finite numbers.")
    st.stop()


# --------------------------------------------------
# PREPARE MODEL INPUT
# --------------------------------------------------

input_data = pd.DataFrame(
    [[
        n,
        p,
        k,
        temperature,
        humidity,
        ph,
        rainfall
    ]],
    columns=FEATURES
)


# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------

try:
    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]
    classes = model.classes_

    ranked_indices = np.argsort(probabilities)[::-1][:5]

except Exception as error:
    st.error(f"Crop prediction failed: {error}")
    st.stop()


try:
    soil_report = analyze_soil(n, p, k, ph)

except Exception as error:
    st.error(f"Soil analysis failed: {error}")
    st.stop()


# --------------------------------------------------
# SOIL OVERVIEW
# --------------------------------------------------

st.success("Soil analysis completed successfully.")

st.subheader("📊 Soil Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Nitrogen (N)", f"{n:g}")
col2.metric("Phosphorus (P)", f"{p:g}")
col3.metric("Potassium (K)", f"{k:g}")
col4.metric("Soil pH", f"{ph:.1f}")

col5, col6, col7 = st.columns(3)

col5.metric("Temperature", f"{temperature:g} °C")
col6.metric("Humidity", f"{humidity:g}%")
col7.metric("Rainfall", f"{rainfall:g} mm")


# --------------------------------------------------
# SECTION 1: SOIL NUTRIENT EVALUATION
# --------------------------------------------------

st.divider()

st.header("🔬 1. Soil Nutrient Evaluation")

st.write(
    "The following observations are generated from "
    "the entered measurements and the configured "
    "soil evaluation rules."
)

for finding in soil_report["findings"]:
    st.write(f"• {finding}")

st.warning(
    "NPK values are reported as entered. Their units "
    "and applicable reference ranges must be verified "
    "before classifying nutrients as deficient or excessive."
)


# --------------------------------------------------
# SECTION 2: SOIL pH ANALYSIS
# --------------------------------------------------

st.subheader("Soil Acidity and Alkalinity")

if ph < 5.5:

    st.warning(
        "The soil falls in the strongly acidic range "
        "used by this prototype. Crop tolerance and "
        "additional soil testing should be considered."
    )

elif ph < 6.5:

    st.info(
        "The soil falls in the moderately to slightly "
        "acidic range used by this prototype."
    )

elif ph <= 7.5:

    st.success(
        "The soil falls in the near-neutral range "
        "used by this prototype."
    )

elif ph <= 8.5:

    st.warning(
        "The soil falls in the alkaline range used by "
        "this prototype. Investigate crop requirements "
        "and possible nutrient availability issues."
    )

else:

    st.error(
        "The soil falls in the highly alkaline range "
        "used by this prototype. Additional soil "
        "assessment is recommended."
    )

st.caption(
    "These are broad interpretive ranges, not a "
    "crop-specific diagnosis."
)


# --------------------------------------------------
# SECTION 3: NPK VISUALIZATION
# --------------------------------------------------

st.subheader("NPK Measurement Visualization")

nutrient_data = pd.DataFrame({
    "Nutrient": [
        "Nitrogen",
        "Phosphorus",
        "Potassium"
    ],
    "Value": [n, p, k]
})

chart_col, details_col = st.columns([1.3, 1])

with chart_col:

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.bar(
        nutrient_data["Nutrient"],
        nutrient_data["Value"]
    )

    ax.set_ylabel("Entered measurement")
    ax.set_title("NPK Measurements")

    st.pyplot(fig)
    plt.close(fig)

with details_col:

    st.markdown("### Measurement Summary")

    for _, row in nutrient_data.iterrows():
        st.write(
            f"**{row['Nutrient']}:** {row['Value']:g}"
        )

    st.write(
        "The chart compares the numerical inputs. "
        "It does not establish nutrient sufficiency "
        "because the values may have different "
        "agronomic interpretations."
    )


# --------------------------------------------------
# SECTION 4: ML CROP RECOMMENDATION
# --------------------------------------------------

st.divider()

st.header("🌾 2. Intelligent Crop Recommendation")

st.markdown(
    f"""
    <div style="
        background-color:#E8F5E9;
        padding:24px;
        border-radius:12px;
        border-left:6px solid #2E7D32;
    ">
        <h2 style="color:#1B5E20;">
            {str(prediction).title()}
        </h2>
        <p>
            Top prediction from the trained
            crop classification model.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "The model uses N, P, K, temperature, humidity, "
    "pH, and rainfall. Its prediction is not a guarantee "
    "of crop success."
)

st.subheader("🏆 Top 5 Model Predictions")

ranked_crops = pd.DataFrame({
    "Crop": [
        str(classes[i]).title()
        for i in ranked_indices
    ],
    "Model Score (%)": [
        round(float(probabilities[i]) * 100, 2)
        for i in ranked_indices
    ]
})

st.dataframe(
    ranked_crops,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Model scores are classifier outputs and are not "
    "necessarily calibrated probabilities of successful "
    "cultivation. The ranking is based on the model, "
    "not a separately validated agronomic suitability score."
)


# --------------------------------------------------
# SECTION 5: ECOSYSTEM REMEDIATION
# --------------------------------------------------

st.divider()

st.header("🌱 3. Ecosystem Remediation Plan")

st.write(
    "Potential soil management actions based on the "
    "configured rule-based evaluation:"
)

for recommendation in soil_report["remediation"]:
    st.markdown(f"- {recommendation}")

st.info(
    "Amendment selection and application rates require "
    "appropriate soil testing and crop-specific guidance. "
    "The prototype does not calculate fertilizer dosages."
)


# --------------------------------------------------
# SECTION 6: ENVIRONMENTAL IMPACT
# --------------------------------------------------

st.divider()

st.header("🌍 4. Environmental Impact Assessment")

for impact in soil_report["environmental_impacts"]:
    st.markdown(f"- {impact}")

st.caption(
    "These are potential environmental impacts associated "
    "with general soil conditions and management practices. "
    "They are not measurements of actual environmental damage."
)


# --------------------------------------------------
# SECTION 7: DOWNLOAD REPORT
# --------------------------------------------------

st.divider()

st.header("📄 5. Integrated Soil Analysis Report")

report = f"""
SOILSENSE AI
Real-Time Intelligence for Soil Nutrient Evaluation
and Ecosystem Remediation

==================================================
SOIL MEASUREMENTS
==================================================

Nitrogen (N): {n}
Phosphorus (P): {p}
Potassium (K): {k}
Soil pH: {ph}

Temperature: {temperature} °C
Humidity: {humidity} %
Rainfall: {rainfall} mm

==================================================
SOIL NUTRIENT EVALUATION
==================================================

{chr(10).join('- ' + item for item in soil_report['findings'])}

==================================================
CROP RECOMMENDATION
==================================================

Top predicted crop: {str(prediction).title()}

Top 5 model predictions:

{ranked_crops.to_string(index=False)}

==================================================
ECOSYSTEM REMEDIATION
==================================================

{chr(10).join('- ' + item for item in soil_report['remediation'])}

==================================================
ENVIRONMENTAL IMPACT ASSESSMENT
==================================================

{chr(10).join('- ' + item for item in soil_report['environmental_impacts'])}

==================================================
IMPORTANT LIMITATIONS
==================================================

This application is a dataset-driven college prototype.

The crop prediction depends on the trained dataset
and the supplied input values.

NPK deficiencies have not been confirmed unless
validated soil-testing thresholds are applied.

The environmental impacts are potential risks,
not confirmed measurements of environmental damage.

Fertilizer dosages and amendment requirements are
not calculated by this prototype.

Consult qualified agricultural guidance before
making cultivation or soil-treatment decisions.
"""

st.download_button(
    label="⬇️ Download Complete Soil Report",
    data=report,
    file_name="soilsense_soil_analysis_report.txt",
    mime="text/plain",
    use_container_width=True
)

st.divider()

st.caption(
    "SoilSense AI | Dataset-driven soil evaluation "
    "and ecosystem remediation prototype"
)

