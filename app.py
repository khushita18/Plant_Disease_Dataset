import os
import time
import streamlit as st
import tensorflow as tf
import numpy as np
import requests
from streamlit_lottie import st_lottie

base_path = os.path.dirname(os.path.abspath(__file__))


# ----------------------------
# 🌿 LOTTIE + CSS HELPERS
# ----------------------------
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS (make sure "style.css" exists)
local_css("style.css")

# ----------------------------
# 🌦️ WEATHER + REMEDIES SECTION
# ----------------------------
def get_weather_risk(city):
    api_key = "5553d7605e224d536367f39eb81cfcdc"  # Replace with your own API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return {"error": "Could not fetch weather data"}

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather_condition = data["weather"][0]["main"]

    # Simple logic for risk level
    if humidity > 80 and 20 <= temp <= 28:
        risk = "High"
    elif humidity > 60:
        risk = "Moderate"
    else:
        risk = "Low"

    return {
        "city": city,
        "temperature": temp,
        "humidity": humidity,
        "weather": weather_condition,
        "disease_risk": risk
    }

# Remedies dictionary
remedies = {
    "Apple___Apple_scab": {
        "chemical": "Apply fungicides containing mancozeb or captan at early signs of infection.",
        "organic": "Use neem oil or sulfur spray weekly during wet weather.",
        "preventive": "Plant resistant varieties and remove fallen leaves after harvest."
    },
    "Apple___Black_rot": {
        "chemical": "Spray copper or sulfur-based fungicides at the green-tip stage.",
        "organic": "Apply neem oil or compost tea during early spring.",
        "preventive": "Remove mummified fruits and prune infected branches."
    },
    "Apple___Cedar_apple_rust": {
        "chemical": "Use fungicides with myclobutanil or propiconazole during early spring.",
        "organic": "Prune out galls on nearby cedar trees to reduce spread.",
        "preventive": "Avoid planting apples near juniper or cedar trees."
    },
    "Apple___healthy": {
        "chemical": "No treatment required.",
        "organic": "Maintain regular pruning and organic compost feeding.",
        "preventive": "Continue routine monitoring to ensure plant health."
    },
    "Blueberry___healthy": {
        "chemical": "No treatment required.",
        "organic": "Keep soil acidic (pH 4.5–5.5) and mulch to retain moisture.",
        "preventive": "Avoid overwatering and ensure good air circulation."
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "chemical": "Use sulfur-based fungicides or myclobutanil sprays.",
        "organic": "Spray neem oil or milk solution (1:10 ratio) every week.",
        "preventive": "Prune trees to improve air circulation and reduce humidity."
    },
    "Cherry_(including_sour)___healthy": {
        "chemical": "No treatment needed.",
        "organic": "Maintain proper watering and sunlight.",
        "preventive": "Continue monitoring for early disease symptoms."
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "chemical": "Apply strobilurin-based fungicides like azoxystrobin or pyraclostrobin.",
        "organic": "Use compost tea or neem oil as preventive sprays.",
        "preventive": "Rotate crops and use resistant corn hybrids."
    },
    "Corn_(maize)___Common_rust_": {
        "chemical": "Spray with fungicides containing propiconazole or tebuconazole.",
        "organic": "Use sulfur or copper-based sprays as natural fungicides.",
        "preventive": "Plant resistant varieties and avoid dense planting."
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "chemical": "Apply fungicides like mancozeb or azoxystrobin at early symptoms.",
        "organic": "Use neem oil spray and maintain field sanitation.",
        "preventive": "Rotate crops and use disease-resistant hybrids."
    },
    "Corn_(maize)___healthy": {
        "chemical": "No treatment required.",
        "organic": "Ensure proper nitrogen levels in soil.",
        "preventive": "Monitor regularly for early leaf symptoms."
    },
    "Grape___Black_rot": {
        "chemical": "Use fungicides containing mancozeb or myclobutanil every 10–14 days.",
        "organic": "Spray neem oil or compost tea during wet periods.",
        "preventive": "Remove mummified berries and prune infected shoots."
    },
    "Grape___Esca_(Black_Measles)": {
        "chemical": "Apply fungicides containing carbendazim at pruning time.",
        "organic": "Use Trichoderma-based biofungicides to suppress infection.",
        "preventive": "Avoid pruning in wet weather and remove diseased wood."
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "chemical": "Spray with chlorothalonil or copper oxychloride.",
        "organic": "Use neem oil or sulfur dust as preventive treatment.",
        "preventive": "Ensure good canopy ventilation and avoid waterlogging."
    },
    "Grape___healthy": {
        "chemical": "No treatment required.",
        "organic": "Maintain vine health with compost tea sprays.",
        "preventive": "Prune vines regularly and remove fallen leaves."
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "chemical": "No chemical cure. Control psyllids using insecticides like imidacloprid.",
        "organic": "Use neem-based sprays to deter psyllid populations.",
        "preventive": "Remove infected trees and plant certified disease-free saplings."
    },
    "Peach___Bacterial_spot": {
        "chemical": "Apply copper-based bactericides or oxytetracycline sprays.",
        "organic": "Use garlic extract or neem oil sprays biweekly.",
        "preventive": "Avoid overhead irrigation and use resistant varieties."
    },
    "Peach___healthy": {
        "chemical": "No treatment required.",
        "organic": "Feed with compost and maintain good airflow.",
        "preventive": "Monitor regularly for leaf spots or pests."
    },
    "Pepper,_bell___Bacterial_spot": {
        "chemical": "Use copper-based sprays like copper hydroxide or oxychloride.",
        "organic": "Apply garlic extract or neem oil as natural bactericides.",
        "preventive": "Avoid handling wet plants and sanitize garden tools."
    },
    "Pepper,_bell___healthy": {
        "chemical": "No treatment required.",
        "organic": "Maintain nutrient balance and good watering schedule.",
        "preventive": "Rotate crops yearly to prevent disease build-up."
    },
    "Potato___Early_blight": {
        "chemical": "Spray copper-based fungicides or chlorothalonil every 7–10 days.",
        "organic": "Apply neem oil or compost tea weekly to reduce fungal spread.",
        "preventive": "Avoid overhead watering and rotate crops annually."
    },
    "Potato___Late_blight": {
        "chemical": "Use fungicides containing Mancozeb or Metalaxyl (Ridomil Gold).",
        "organic": "Spray a mix of baking soda and water on leaves as a natural deterrent.",
        "preventive": "Destroy infected plants and ensure proper spacing for airflow."
    },
    "Potato___healthy": {
        "chemical": "No treatment needed.",
        "organic": "Ensure proper watering and soil drainage.",
        "preventive": "Store seed potatoes in cool, dry places before planting."
    },
    "Raspberry___healthy": {
        "chemical": "No treatment needed.",
        "organic": "Mulch to retain moisture and prevent soil splash.",
        "preventive": "Prune old canes to maintain air circulation."
    },
    "Soybean___healthy": {
        "chemical": "No treatment needed.",
        "organic": "Maintain balanced fertilization for better resistance.",
        "preventive": "Rotate with non-legume crops to reduce pathogens."
    },
    "Squash___Powdery_mildew": {
        "chemical": "Apply sulfur-based fungicides or potassium bicarbonate sprays.",
        "organic": "Spray diluted milk (1:10) or neem oil weekly.",
        "preventive": "Water at the base and ensure good airflow between plants."
    },
    "Strawberry___Leaf_scorch": {
        "chemical": "Use copper-based fungicides during early infection.",
        "organic": "Apply compost tea or neem oil sprays weekly.",
        "preventive": "Avoid overhead watering and remove infected leaves."
    },
    "Strawberry___healthy": {
        "chemical": "No treatment needed.",
        "organic": "Apply compost tea and maintain mulch layer.",
        "preventive": "Inspect regularly for fungal symptoms."
    },
    "Tomato___Bacterial_spot": {
        "chemical": "Use copper-based bactericides or streptomycin sprays.",
        "organic": "Apply neem oil or garlic extract every 5 days.",
        "preventive": "Avoid splashing water on leaves and rotate crops."
    },
    "Tomato___Early_blight": {
        "chemical": "Apply fungicides like copper oxychloride or chlorothalonil.",
        "organic": "Spray neem oil twice a week to inhibit fungal growth.",
        "preventive": "Avoid splashing water on leaves and rotate tomato crops yearly."
    },
    "Tomato___Late_blight": {
        "chemical": "Spray Mancozeb or Metalaxyl fungicides every 5–7 days during humidity.",
        "organic": "Use compost extracts and neem oil sprays on early signs.",
        "preventive": "Avoid water stagnation and remove infected plants promptly."
    },
    "Tomato___Leaf_Mold": {
        "chemical": "Use mancozeb or copper oxychloride fungicides.",
        "organic": "Improve air circulation; use baking soda + water solution weekly.",
        "preventive": "Avoid overcrowding plants and maintain dryness."
    },
    "Tomato___Septoria_leaf_spot": {
        "chemical": "Use chlorothalonil-based fungicides every 7–10 days.",
        "organic": "Spray neem oil or compost tea for organic control.",
        "preventive": "Remove infected leaves and avoid working with wet plants."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "chemical": "Apply abamectin or spiromesifen as miticides.",
        "organic": "Spray neem oil or insecticidal soap twice a week.",
        "preventive": "Keep humidity high and wash leaves to remove mites."
    },
    "Tomato___Target_Spot": {
        "chemical": "Use fungicides containing chlorothalonil or mancozeb.",
        "organic": "Apply neem oil or copper sprays for organic control.",
        "preventive": "Avoid high humidity and ensure proper plant spacing."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "chemical": "No chemical cure. Control whiteflies with imidacloprid.",
        "organic": "Use yellow sticky traps and neem oil sprays to deter whiteflies.",
        "preventive": "Plant resistant varieties and remove infected plants."
    },
    "Tomato___Tomato_mosaic_virus": {
        "chemical": "No chemical cure. Disinfect tools with bleach after use.",
        "organic": "Use neem oil and maintain sanitation to reduce spread.",
        "preventive": "Avoid touching plants after handling tobacco."
    },
    "Tomato___healthy": {
        "chemical": "No treatment required.",
        "organic": "Maintain nutrient-rich soil and adequate watering.",
        "preventive": "Continue crop monitoring for early symptoms."
    }
}



def add_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            # filter: blur(8px);
            background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            
        }}
        /* Make text more readable */
        h1, h2, h3, h4, h5, h6, p, span, div {{
            color: #ffffff !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function
add_bg_image("https://images.unsplash.com/photo-1501004318641-b39e6451bec6")

# Main UI content
st.title("🌿 CropSavior: Predict & Prevent")
st.subheader("AI-Powered Plant Disease Detection & Prevention System")
st.write("Upload a leaf image and let our model detect potential diseases with accuracy and insight.")


# ----------------------------
# 🔍 MODEL PREDICTION FUNCTION
# ----------------------------
def model_prediction(test_image):
    model = tf.keras.models.load_model('trained_model.keras')
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.expand_dims(input_arr, axis=0)
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

# ----------------------------
# 🌿 STREAMLIT UI
# ----------------------------
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition"])

# HOME PAGE
if app_mode == "Home":
    st.header("🌿 Plant Disease Recognition System")
    st.image("home_page.jpg", use_container_width=True)

    lottie_plant = load_lottie_url("https://lottie.host/52e0a897-f07f-4ac4-8c8e-5a93f08a56fa/7i9r5S0G7R.json")
    if lottie_plant:
        st_lottie(lottie_plant, speed=1, height=300, key="plant")

    st.markdown("""
    Welcome to the **Plant Disease Recognition System**! 🌱  
    Upload a plant leaf image to detect possible diseases and get instant remedies.

    ### How It Works
    1. **Upload Image:** Go to *Disease Recognition* page and upload a plant image.
    2. **Analyze:** The model identifies potential diseases.
    3. **Result:** Get remedies and weather-based risk instantly.

    ### Why Choose Us?
    - 💡 AI-Powered Accuracy  
    - 🧩 User-Friendly Interface  
    - ⚡ Fast Predictions  

    👉 Start by selecting **Disease Recognition** from the sidebar.
    """)

# ABOUT PAGE

elif app_mode == "About":
    st.header("📘 About CropSavior")
    
    st.markdown("""
    ### 🌱 Overview  
    **CropSavior** is an AI-powered plant disease detection and prevention system designed to help farmers and agriculturists identify plant leaf diseases early.  
    By combining **Deep Learning**, **Weather Intelligence**, and **Preventive Remedies**, it promotes sustainable and data-driven farming.
    """)

    st.image(
        os.path.join(base_path, "overview.png"),
        caption="Empowering Sustainable Agriculture with AI",
        use_container_width=True
    )

    st.markdown("---")
    
    st.subheader("🎯 Objectives")
    st.markdown("""
    - Detect plant diseases using **image-based deep learning models**  
    - Provide **chemical, organic, and preventive remedies**  
    - Predict **disease risk levels** based on real-time weather data  
    - Empower farmers with **AI-driven insights** for early action  
    """)

    st.markdown("---")
    
    st.subheader("🧠 Technologies Used")
    st.markdown("""
    - **Frontend:** Streamlit (Python-based Web Framework)  
    - **Backend:** TensorFlow & Keras for Deep Learning  
    - **Database:** Local Model + Cloud Image Processing  
    - **API Integration:** OpenWeather API for weather analysis  
    - **Languages:** Python, HTML, CSS  
    """)

    st.image(
        "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1200&q=80",
        caption="AI & Data powering precision agriculture",
        use_container_width=True
    )

    st.markdown("---")


    st.subheader("🧬 Model Architecture")
    st.markdown("""
    - **Model Type:** Convolutional Neural Network (CNN)  
    - **Input Shape:** 128 × 128 × 3 (RGB Images)  
    - **Dataset:** PlantVillage (87K images, 38 classes)  
    - **Training Accuracy:** ~98%  
    - **Validation Accuracy:** ~96%  
    """)

    st.image(
        os.path.join(base_path, "model-architecture.png"),
        caption="CNN Architecture Overview",
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📊 Dataset Details")
    st.markdown("""
    - **Source:** [Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)  
    - **Total Images:** 87,000+  
    - **Classes:** 38 (Healthy + Diseased Categories)  
    - **Split:** 80% Training | 20% Validation  
    """)

    st.image(
        os.path.join(base_path, "dataset-details.png"),
        caption="Diverse crop leaf dataset for accurate disease classification",
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🚀 Future Enhancements")
    st.markdown("""
    - Integration with **IoT sensors** for soil and humidity tracking  
    - Support for **regional language voice interaction**  
    - Expansion to include **pest detection and nutrient deficiency analysis**  
    - Real-time farmer alerts via **WhatsApp/SMS APIs**  
    """)

    st.markdown("---")
    
    st.subheader("👩‍💻 Team & Acknowledgements")
    st.markdown("""
    **Developed By:** CropSavior Team  
    **Guided By:** Faculty, NMIMS MPSTME Mumbai  
    **Acknowledgement:** TensorFlow, Streamlit, and OpenWeather API  
    """)

    st.success("🌿 Together, we grow smarter and healthier crops with AI!")

elif app_mode == "About":
    st.header("📘 About CropSavior")

    st.markdown("""
    ### 🌱 Overview
    **CropSavior** is an AI-powered plant disease detection and prevention system designed to help farmers and agriculturists identify plant leaf diseases early.
    By combining **Deep Learning**, **Weather Intelligence**, and **Preventive Remedies**, it promotes sustainable and data-driven farming.
    """)

    st.image(
        "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1200&q=80",
        caption="Empowering Sustainable Agriculture with AI",
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🎯 Objectives")
    st.markdown("""
    - Detect plant diseases using **image-based deep learning models**
    - Provide **chemical, organic, and preventive remedies**
    - Predict **disease risk levels** based on real-time weather data
    - Empower farmers with **AI-driven insights** for early action
    """)

    st.markdown("---")

    st.subheader("🧠 Technologies Used")
    st.markdown("""
    - **Frontend:** Streamlit (Python-based Web Framework)
    - **Backend:** TensorFlow & Keras for Deep Learning
    - **Database:** Local Model + Cloud Image Processing
    - **API Integration:** OpenWeather API for weather analysis
    - **Languages:** Python, HTML, CSS
    """)

    st.image(
        "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1200&q=80",
        caption="AI & Data powering precision agriculture",
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🧬 Model Architecture")
    st.markdown("""
    - **Model Type:** Convolutional Neural Network (CNN)
    - **Input Shape:** 128 × 128 × 3 (RGB Images)
    - **Dataset:** PlantVillage (87K images, 38 classes)
    - **Training Accuracy:** ~98%
    - **Validation Accuracy:** ~96%
    """)

    st.image(
        "model-architecture.png",
        caption="CNN Architecture Overview",
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📊 Dataset Details")
    st.markdown("""
    - **Source:** [PlantVillage Dataset (Kaggle)](https://www.kaggle.com/datasets/emmarex/plantdisease)
    - **Total Images:** 87,000+
    - **Classes:** 38 (Healthy + Diseased Categories)
    - **Split:** 80% Training | 20% Validation
    """)

    st.image(
        "dataset-details.png",
        caption="Diverse crop leaf dataset for accurate disease classification",
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🚀 Future Enhancements")
    st.markdown("""
    - Integration with **IoT sensors** for soil and humidity tracking
    - Support for **regional language voice interaction**
    - Expansion to include **pest detection and nutrient deficiency analysis**
    - Real-time farmer alerts via **WhatsApp/SMS APIs**
    """)

    st.markdown("---")

    st.subheader("👩‍💻 Team & Acknowledgements")
    st.markdown("""
    **Developed By:** CropSavior Team
    **Guided By:** Faculty, NMIMS MPSTME Shirpur
    **Acknowledgement:** TensorFlow, Streamlit, and OpenWeather API
    """)

    st.success("🌿 Together, we grow smarter and healthier crops with AI!")


# DISEASE RECOGNITION PAGE
elif app_mode == "Disease Recognition":
    st.header("🔍 Disease Recognition")

    # lottie_plant = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")
    # if lottie_plant:
    #     st_lottie(lottie_plant, height=250, key="leaf")

    city = st.text_input("Enter your city for weather-based analysis (e.g., Pune):", "Pune")
    test_image = st.file_uploader("Upload a Leaf Image")

    if st.button("Show Image"):
        if test_image:
            st.image(test_image, use_container_width=True)
        else:
            st.warning("Please upload an image first.")

    if st.button("Predict"):
        if not test_image:
            st.warning("Please upload an image first.")
        else:
            with st.spinner("Analyzing image..."):
                # st.snow()
                result_index = model_prediction(test_image)

                # Class labels
                class_names = [
                    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
                    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
                    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
                    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
                    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
                    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
                    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
                    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                    'Tomato___healthy'
                ]

                # predicted_class = class_names[result_index]
                # st.success(f"✅ Model Prediction: **{predicted_class}**")
                
                # Calculate prediction + confidence
                prediction = model_prediction(test_image)
                model = tf.keras.models.load_model('trained_model.keras')

                # Preprocess the uploaded image again to get confidence
                image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
                input_arr = tf.keras.preprocessing.image.img_to_array(image)
                input_arr = np.expand_dims(input_arr, axis=0)
                prediction_probs = model.predict(input_arr)
                result_index = np.argmax(prediction_probs)
                predicted_class = class_names[result_index]
                confidence = float(np.max(prediction_probs)) * 100

                # Display prediction result
                st.success(f"✅ Model Prediction: **{predicted_class}**")
                st.info(f"🧠 Confidence Level: **{confidence:.2f}%**")

                # Add animated confidence bar
                progress_text = "🧪 Calculating Model Confidence..."
                progress_bar = st.progress(0)
                for percent in range(int(confidence)):
                    time.sleep(0.01)
                    progress_bar.progress(percent + 1)
                st.success("✅ Confidence analysis complete!")

                # Display remedies
                if predicted_class in remedies:
                    st.subheader("🌿 Suggested Remedies")

                    remedy = remedies[predicted_class]
                    st.write("**Chemical Treatment:**", remedy["chemical"])
                    st.write("**Organic Treatment:**", remedy["organic"])
                    st.write("**Preventive Measures:**", remedy["preventive"])
                else:
                    st.warning("No remedies found for this class.")

                # Weather-based risk analysis
                if city:
                    weather_data = get_weather_risk(city)
                if "error" not in weather_data:
                    st.markdown("---")
                    st.subheader("🌦️ Weather-Based Disease Risk")
                    st.write(f"**City:** {weather_data['city']}")
                    st.write(f"🌡️ **Temperature:** {weather_data['temperature']} °C")
                    st.write(f"💧 **Humidity:** {weather_data['humidity']}%")
                    st.write(f"🌤️ **Condition:** {weather_data['weather']}")
                    st.info(f"🔥 **Disease Risk Level:** {weather_data['disease_risk']}")
                else:
                    st.warning(weather_data["error"])

                #     time.sleep(0.01)
                #     progress_bar.progress(percent + 1)


                # remedies = remedies.get(predicted_class, {
                #     "chemical": "No specific chemical cure.",
                #     "organic": "Use neem oil or compost tea as a general remedy.",
                #     "preventive": "Ensure air circulation and crop rotation."
                # })
                
                # if confidence > 90:
                #     st.success(f"💪 The model is **very confident** ({confidence:.2f}%) in this prediction!")
                # elif confidence > 70:
                #     st.warning(f"🤔 The model is **moderately confident** ({confidence:.2f}%).")
                # else:
                #     st.error(f"😬 The model is **not very confident** ({confidence:.2f}%). Try another image.")


                # st.subheader("🌿 Remedies")
                # st.markdown(f"""
                # - **Chemical:** {remedies['chemical']}
                # - **Organic:** {remedies['organic']}
                # - **Preventive:** {remedies['preventive']}
                # """)

                # weather_data = get_weather_risk(city)
                # if "error" in weather_data:
                #     st.warning("⚠️ Could not fetch weather data.")
                # else:
                #     st.subheader(f"🌦️ Weather in {weather_data['city']}")
                #     st.markdown(f"""
                #     - Temperature: **{weather_data['temperature']}°C**
                #     - Humidity: **{weather_data['humidity']}%**
                #     - Condition: **{weather_data['weather']}**
                #     - Disease Risk: **{weather_data['disease_risk']}**
                #     """)


#-------------------------------------------------------------------------------------------------------------------

# def load_lottie_url(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()


# import streamlit as st
# import tensorflow as tf
# import numpy as np
# import requests
# from streamlit_lottie import st_lottie


# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("style.css")



# # ----------------------------
# # 🌦️ WEATHER + REMEDIES SECTION
# # ----------------------------
# def get_weather_risk(city):
#     api_key = "5553d7605e224d536367f39eb81cfcdc"  # Replace with your valid OpenWeatherMap API key
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

#     response = requests.get(url)
#     data = response.json()

#     if response.status_code != 200:
#         return {"error": "Could not fetch weather data"}

#     temp = data["main"]["temp"]
#     humidity = data["main"]["humidity"]
#     weather_condition = data["weather"][0]["main"]

#     # Simple logic for risk level
#     if humidity > 80 and 20 <= temp <= 28:
#         risk = "High"
#     elif humidity > 60:
#         risk = "Moderate"
#     else:
#         risk = "Low"

#     return {
#         "city": city,
#         "temperature": temp,
#         "humidity": humidity,
#         "weather": weather_condition,
#         "disease_risk": risk
#     }

# # Remedies dictionary
# disease_cures = {
#     "Potato___Early_blight": {
#         "chemical": "Spray copper-based fungicides or chlorothalonil every 7–10 days.",
#         "organic": "Apply neem oil or compost tea weekly to reduce fungal spread.",
#         "preventive": "Avoid overhead watering and rotate crops annually."
#     },
#     "Potato___Late_blight": {
#         "chemical": "Use fungicides containing Mancozeb or Metalaxyl (Ridomil Gold).",
#         "organic": "Spray a mix of baking soda and water on leaves as a natural deterrent.",
#         "preventive": "Destroy infected plants and ensure proper spacing for airflow."
#     },
#     "Tomato___Early_blight": {
#         "chemical": "Apply fungicides like copper oxychloride or chlorothalonil.",
#         "organic": "Spray neem oil twice a week to inhibit fungal growth.",
#         "preventive": "Avoid splashing water on leaves and rotate tomato crops yearly."
#     },
#     "Tomato___Late_blight": {
#         "chemical": "Spray Mancozeb or Metalaxyl fungicides. Repeat every 5–7 days during humidity.",
#         "organic": "Use compost extracts and neem oil sprays on early signs.",
#         "preventive": "Avoid water stagnation and remove infected plants promptly."
#     },
#     "Tomato___Bacterial_spot": {
#         "chemical": "Use copper-based sprays like copper hydroxide or oxychloride.",
#         "organic": "Apply garlic extract or neem oil spray as natural bactericides.",
#         "preventive": "Do not handle plants when wet and sanitize garden tools."
#     },
#     "Tomato___Leaf_Mold": {
#         "chemical": "Use mancozeb or copper oxychloride fungicides.",
#         "organic": "Improve air circulation; use baking soda + water solution weekly.",
#         "preventive": "Avoid overcrowding plants in greenhouses and maintain dryness."
#     },
#     "Apple___Black_rot": {
#         "chemical": "Spray copper or sulfur-based fungicides at the green-tip stage.",
#         "organic": "Apply neem oil or compost tea during early spring.",
#         "preventive": "Remove mummified fruits and prune infected branches."
#     },
#     "Orange___Haunglongbing_(Citrus_greening)": {
#         "chemical": "No chemical cure. Control psyllids using insecticides.",
#         "organic": "Use neem-based insect repellents to deter psyllids.",
#         "preventive": "Remove infected trees and plant certified disease-free saplings."
#     }
# }

# # ----------------------------
# # 🔍 MODEL PREDICTION FUNCTION
# # ----------------------------
# def model_prediction(test_image):
#     model = tf.keras.models.load_model('trained_model.keras')
#     image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
#     input_arr = tf.keras.preprocessing.image.img_to_array(image)
#     input_arr = np.array([input_arr])
#     prediction = model.predict(input_arr)
#     result_index = np.argmax(prediction)
#     return result_index

# # ----------------------------
# # 🌿 STREAMLIT UI
# # ----------------------------
# st.sidebar.title("Dashboard")
# app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition"])

# # Home Page
# if app_mode == "Home":
#     st.header("PLANT DISEASE RECOGNITION SYSTEM")
#     image_path = "home_page.jpg"
#     st.image(image_path, use_container_width=True)
#     lottie_plant = load_lottie_url("https://lottie.host/52e0a897-f07f-4ac4-8c8e-5a93f08a56fa/7i9r5S0G7R.json")
#     st_lottie(lottie_plant, speed=1, height=300, key="plant")

#     st.markdown("""
#     Welcome to the Plant Disease Recognition System! 🌿🔍
#     Upload an image of a plant leaf to detect potential diseases and get remedies instantly.
    
    
#     Our mission is to help in identifying plant diseases efficiently. Upload an image of a plant, and our system will analyze it to detect any signs of diseases. Together, let's protect our crops and ensure a healthier harvest!

#     ### How It Works
#     1. **Upload Image:** Go to the **Disease Recognition** page and upload an image of a plant with suspected diseases.
#     2. **Analysis:** Our system will process the image using advanced algorithms to identify potential diseases.
#     3. **Results:** View the results and recommendations for further action.

#     ### Why Choose Us?
#     - **Accuracy:** Our system utilizes state-of-the-art machine learning techniques for accurate disease detection.
#     - **User-Friendly:** Simple and intuitive interface for seamless user experience.
#     - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

#     ### Get Started
#     Click on the **Disease Recognition** page in the sidebar to upload an image and experience the power of our Plant Disease Recognition System!

#     ### About Us
#     Learn more about the project, our team, and our goals on the **About** page.
#     """)

# # About Page
# elif app_mode == "About":
#     st.header("About")
#     st.markdown("""
#     This system uses a deep learning model trained on 38 plant disease classes.
#     It helps identify diseases early and provides remedies with weather-based disease risk.
    
#     #### About Dataset
#     This dataset is recreated using offline augmentation from the original dataset. The original dataset can be found on this github repo. This dataset consists of about 87K rgb images of healthy and diseased crop leaves which is categorized into 38 different classes. The total dataset is divided into 80/20 ratio of training and validation set preserving the directory structure. A new directory containing 33 test images is created later for prediction purpose.
#     #### Content
#     1. train (70295 images)
#     2. test (33 images)
#     3. validation (17572 images)
#     """)

# # Disease Recognition Page
# elif app_mode == "Disease Recognition":
#     st.header("Disease Recognition")
#     from streamlit_lottie import st_lottie
#     import requests

#     def load_lottieurl(url: str):
#         r = requests.get(url)
#         if r.status_code != 200:
#             return None
#         return r.json()

#     # Load animation (you can change this URL to any Lottie animation)
#     lottie_plant = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")

#     st_lottie(lottie_plant, speed=1, reverse=False, loop=True, height=250, key="plant")

#     city = st.text_input("Enter your city for weather-based analysis (e.g., Pune):", "Pune")
#     test_image = st.file_uploader("Choose an Image:")

#     if st.button("Show Image"):
#         if test_image:
#             st.image(test_image, use_container_width=True)
#         else:
#             st.warning("Please upload an image first.")

#     if st.button("Predict"):
#         loading_animation = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_cg3r2r.json")
#         st_lottie(loading_animation, height=150, key="loading")

#         if test_image:
#             with st.spinner("Analyzing image..."):
#                 st.snow()
#                 st.write("Our Prediction:")
#                 result_index = model_prediction(test_image)

#                 # Reading class labels
#                 class_name = [
#                     'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
#                     'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
#                     'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
#                     'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
#                     'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
#                     'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
#                     'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
#                     'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
#                     'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
#                     'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
#                     'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
#                     'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
#                     'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
#                     'Tomato___healthy'
#                 ]

#                 predicted_class = class_name[result_index]
#                 st.success(f"✅ Model predicts: **{predicted_class}**")

#                 st.markdown(f"""
#                 <div class='result-card'>
#                     <h2>🌿 Prediction: <span style='color:#b7e4c7;'>{class_name[result_index]}</span></h2>
#                     <p>💧 Confidence: <strong>High</strong></p>
#                     <p>🌤️ Weather Data: {city} (Real-time)</p>
#                     <p>🌾 Remedies and Suggestions Below 👇</p>
#                 </div>
#                 """, unsafe_allow_html=True)

#                 # Remedies
#                 remedies = disease_cures.get(predicted_class, {
#                     "chemical": "No chemical cure available.",
#                     "organic": "Use neem oil or compost tea as general treatment.",
#                     "preventive": "Ensure proper air circulation and crop rotation."
#                 })
#                 st.subheader("🌿 Remedies:")
#                 st.markdown(f"""
#                 - **Chemical:** {remedies['chemical']}
#                 - **Organic:** {remedies['organic']}
#                 - **Preventive:** {remedies['preventive']}
#                 """)

#                 # Weather Data
#                 weather_data = get_weather_risk(city)
#                 if "error" in weather_data:
#                     st.warning("⚠️ Could not fetch weather data.")
#                 else:
#                     st.subheader(f"🌦️ Weather in {weather_data['city']}:")
#                     st.markdown(f"""
#                     - **Temperature:** {weather_data['temperature']}°C  
#                     - **Humidity:** {weather_data['humidity']}%  
#                     - **Condition:** {weather_data['weather']}  
#                     - **Disease Risk Level:** **{weather_data['disease_risk']}**
#                     """)
#         else:
#             st.warning("Please upload an image first.")



#-------------------------------------------------------------------------------------------------------------------


# import streamlit as st
# import tensorflow as tf
# import numpy as np


# def model_prediction(test_image):
    
#     model  = tf.keras.models.load_model('trained_model.keras')
#     image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128, 128))
#     input_arr = tf.keras.preprocessing.image.img_to_array(image)
#     input_arr = np.array([input_arr]) #Convert single image to a batch
#     prediction = model.predict(input_arr)
#     result_index = np.argmax(prediction)
#     return result_index

# #Sidebar
# st.sidebar.title("Dashboard")
# app_mode = st.sidebar.selectbox("Select Page",["Home","About","Disease Recognition"])

# #Home Page
# if(app_mode=="Home"):
#     st.header("PLANT DISEASE RECOGNITIONI SYSTEM")
#     image_path = "home_page.jpg"
#     st.image(image_path,use_container_width=True)
#     st.markdown(""" 
#     Welcome to the Plant Disease Recognition System! 🌿🔍
    
#     Our mission is to help in identifying plant diseases efficiently. Upload an image of a plant, and our system will analyze it to detect any signs of diseases. Together, let's protect our crops and ensure a healthier harvest!

#     ### How It Works
#     1. **Upload Image:** Go to the **Disease Recognition** page and upload an image of a plant with suspected diseases.
#     2. **Analysis:** Our system will process the image using advanced algorithms to identify potential diseases.
#     3. **Results:** View the results and recommendations for further action.

#     ### Why Choose Us?
#     - **Accuracy:** Our system utilizes state-of-the-art machine learning techniques for accurate disease detection.
#     - **User-Friendly:** Simple and intuitive interface for seamless user experience.
#     - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

#     ### Get Started
#     Click on the **Disease Recognition** page in the sidebar to upload an image and experience the power of our Plant Disease Recognition System!

#     ### About Us
#     Learn more about the project, our team, and our goals on the **About** page.
                

# """)
    
# #About Page
# if(app_mode=="About"):
#     st.header("About")
#     st.markdown("""
#     #### About Dataset
#     This dataset is recreated using offline augmentation from the original dataset. The original dataset can be found on this github repo. This dataset consists of about 87K rgb images of healthy and diseased crop leaves which is categorized into 38 different classes. The total dataset is divided into 80/20 ratio of training and validation set preserving the directory structure. A new directory containing 33 test images is created later for prediction purpose.
#     #### Content
#     1. train (70295 images)
#     2. test (33 images)
#     3. validation (17572 images)
                
# """)
    
# #Prediction Page
# elif(app_mode=="Disease Recognition"):
#     st.header("Disease Recognition")
#     test_image = st.file_uploader("Choose an Image:")
#     if(st.button("Show Image")):
#         st.image(test_image,width=4,use_container_width=True)
#     #Predict button
#     if(st.button("Predict")):
#         with st.spinner("Please Wait.."):
#             st.snow()
#             st.write("Our Prediction")
#             result_index = model_prediction(test_image)
#             #Reading Labels
#             class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
#                     'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
#                     'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
#                     'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
#                     'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
#                     'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
#                     'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
#                     'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
#                     'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
#                     'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
#                     'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
#                     'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
#                     'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
#                       'Tomato___healthy']
#             st.success("Model is Predicting it's a {}".format(class_name[result_index]))