# streamlit_app.py
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
import json

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:5000/predict")

# Page config
st.set_page_config(page_title="CropSavior", page_icon="🌾", layout="centered")

# --- Custom CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Header section ---
st.title("🌾 CropSavior — AI-based Crop Disease Detection")
st.write("Upload a crop image and get instant AI-powered disease predictions.")

# --- Optional animation ---
try:
    with open("assets/animation.json") as f:
        st_lottie(json.load(f), height=200, key="intro_animation")
except:
    pass

# --- Image uploader ---
uploaded_file = st.file_uploader("📸 Upload a Leaf Image", type=["jpg", "jpeg", "png"])

user_id = st.text_input("👤 Enter User ID (optional)", value="user_1")
lat = st.text_input("📍 Latitude (optional)")
lon = st.text_input("📍 Longitude (optional)")

# --- Predict button ---
if st.button("🔍 Analyze Disease"):
    if uploaded_file is None:
        st.warning("Please upload a leaf image first.")
    else:
        with st.spinner("Processing... Please wait"):
            files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"user_id": user_id, "lat": lat, "lon": lon}
            try:
                response = requests.post(API_URL, files=files, data=data)
                if response.status_code == 200:
                    result = response.json()

                    st.success("✅ Prediction Complete!")
                    st.subheader(f"**Detected Disease:** {result['disease']}")
                    st.write(f"**Confidence:** {result['confidence']:.2f}")

                    st.markdown("### 🧪 Remedies:")
                    for r in result["remedies"]:
                        st.write(f"- {r}")

                    if result.get("image_url"):
                        st.image(result["image_url"], caption="Annotated Image", use_column_width=True)
                    else:
                        st.warning("Annotated image not available.")
                else:
                    st.error(f"❌ Server Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")


#------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests
# from PIL import Image
# from streamlit_lottie import st_lottie

# # ------------------ LOTTIE HELPER ------------------
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# # ------------------ PAGE CONFIG ------------------
# st.set_page_config(page_title="🌾 CropSavior | AI Plant Doctor", layout="wide")

# # ------------------ BACKGROUND & GLOBAL STYLE ------------------
# def set_website_style(bg_url):
#     st.markdown(f"""
#         <style>
#         /* Background */
#         .stApp {{
#             background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
#                         url("{bg_url}") center/cover fixed;
#             color: #f0fdf4;
#             font-family: 'Poppins', sans-serif;
#         }}

#         /* Navbar */
#         .navbar {{
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             padding: 1rem 3rem;
#             background: rgba(0, 0, 0, 0.5);
#             backdrop-filter: blur(12px);
#             border-bottom: 1px solid rgba(255, 255, 255, 0.15);
#         }}
#         .nav-links a {{
#             margin: 0 15px;
#             text-decoration: none;
#             color: #fff;
#             font-weight: 500;
#             transition: color 0.3s;
#         }}
#         .nav-links a:hover {{
#             color: #a7ff83;
#         }}

#         /* Logo Animation */
#         .logo {{
#             font-size: 1.8rem;
#             font-weight: 700;
#             background: linear-gradient(90deg, #76ff03, #d4fc79);
#             -webkit-background-clip: text;
#             color: transparent;
#             animation: glow 2.5s infinite alternate;
#         }}
#         @keyframes glow {{
#             from {{ text-shadow: 0 0 10px #00e676; }}
#             to {{ text-shadow: 0 0 25px #76ff03; }}
#         }}

#         /* Glass card */
#         .glass-card {{
#             background: rgba(255, 255, 255, 0.08);
#             backdrop-filter: blur(14px);
#             padding: 60px 80px;
#             border-radius: 25px;
#             margin: 60px auto;
#             max-width: 720px;
#             box-shadow: 0 0 40px rgba(0,0,0,0.35);
#             text-align: center;
#             animation: fadeIn 1s ease-in-out;
#         }}
#         @keyframes fadeIn {{
#             from {{ opacity: 0; transform: translateY(30px); }}
#             to {{ opacity: 1; transform: translateY(0); }}
#         }}

#         /* Buttons */
#         div.stButton > button:first-child {{
#             background: linear-gradient(90deg, #00e676, #76ff03);
#             color: #000;
#             border: none;
#             border-radius: 30px;
#             font-weight: 700;
#             padding: 0.8rem 2.5rem;
#             transition: all 0.3s ease;
#         }}
#         div.stButton > button:hover {{
#             transform: scale(1.05);
#             box-shadow: 0 0 25px #76ff03;
#         }}

#         /* Footer */
#         footer {{
#             text-align: center;
#             color: #ccc;
#             margin-top: 80px;
#             padding: 30px 0;
#             border-top: 1px solid rgba(255, 255, 255, 0.15);
#             font-size: 0.9rem;
#         }}

#         h2, h3, p, label {{
#             color: #eaffea !important;
#         }}
#         </style>
#     """, unsafe_allow_html=True)

# # ------------------ SET BACKGROUND ------------------
# set_website_style("https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1600&q=80")

# # ------------------ NAVBAR ------------------
# st.markdown("""
#     <div class="navbar">
#         <div class="logo">🌾 CropSavior</div>
#         <div class="nav-links">
#             <a href="#home">Home</a>
#             <a href="#about">About</a>
#             <a href="#contact">Contact</a>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# # ------------------ AGRICULTURE ANIMATION ------------------
# lottie_agriculture = load_lottieurl("https://lottie.host/1ef4a0f4-1a18-4e06-a9d9-9e6f91a6eecb/6iSz6eAqKm.json")

# if lottie_agriculture:
#     st_lottie(lottie_agriculture, height=320, key="farm_animation")

# # ------------------ MAIN SECTION ------------------
# st.markdown("<div id='home' class='glass-card'>", unsafe_allow_html=True)
# st.markdown("<h2>🧠 AI-Powered Plant Disease Detection</h2>", unsafe_allow_html=True)
# st.write("Upload a plant leaf image and enter your city to predict disease and get live weather insights 🌦️.")

# # 🌿 Leaf Scan Animation
# lottie_leaf = load_lottieurl("https://lottie.host/2c79e3c4-36ce-4d90-b021-cfbb81df43c3/I8aClxP6zM.json")

# if lottie_leaf:
#     st_lottie(lottie_leaf, height=240, key="leaf_scan")

# st.markdown("<h3 style='text-align:center; margin-top:20px;'>🌿 Detect Plant Diseases Instantly with AI</h3>", unsafe_allow_html=True)

# uploaded_file = st.file_uploader("📸 Upload Leaf Image", type=["jpg", "jpeg", "png"])
# city = st.text_input("🏙️ Enter City Name (e.g., Pune)")

# if uploaded_file and city:
#     if st.button("🔍 Predict Disease"):
#         with st.spinner("🔍 Analyzing image and fetching weather data..."):
#             files = {"file": uploaded_file.getvalue()}
#             data = {"city": city}

#             try:
#                 response = requests.post("http://127.0.0.1:5000/predict", files={"file": uploaded_file}, data=data)
#                 if response.status_code == 200:
#                     result = response.json()
#                     st.success(f"✅ Prediction Successful for {result['city']}")
#                     st.image(uploaded_file, caption="Uploaded Leaf", use_column_width=True)

#                     st.subheader(f"🌱 Disease: {result['predicted_class']}")
#                     st.write(f"**Confidence:** {result['confidence']}%")

#                     st.subheader("💧 Weather Details:")
#                     st.write(f"🌤️ Weather: {result['weather_data']['weather']}")
#                     st.write(f"🌡️ Temperature: {result['weather_data']['temperature']}°C")
#                     st.write(f"💦 Humidity: {result['weather_data']['humidity']}%")
#                     st.write(f"🌾 Risk Level: {result['weather_data']['disease_risk']}")

#                     st.subheader("🩺 Remedies:")
#                     st.write(f"**Organic:** {result['remedies']['organic']}")
#                     st.write(f"**Chemical:** {result['remedies']['chemical']}")
#                     st.write(f"**Preventive:** {result['remedies']['preventive']}")
#                 else:
#                     st.error("❌ Could not fetch prediction. Please check your backend server.")
#             except Exception as e:
#                 st.error(f"⚠️ Error: {e}")
# else:
#     st.info("Please upload a leaf image and enter a city to begin.")
# st.markdown("</div>", unsafe_allow_html=True)

# # ------------------ ABOUT SECTION ------------------
# st.markdown("""
#     <div id='about' style='text-align:center; margin-top:100px;'>
#         <h2>🌿 About CropSavior</h2>
#         <p style='max-width:750px; margin:auto; color:#d0f0c0; font-size:1.1rem;'>
#             CropSavior uses advanced deep learning models to detect plant diseases from leaf images. 
#             Combined with real-time weather insights, it helps farmers take immediate action to prevent crop losses. 
#             Built to support sustainability, efficiency, and smarter farming practices. 🚜
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # ------------------ CONTACT SECTION ------------------
# st.markdown("""
#     <div id='contact' style='text-align:center; margin-top:100px;'>
#         <h2>📩 Contact Us</h2>
#         <p style='color:#b2dfdb;'>Have questions, feedback, or collaboration ideas?</p>
#         <p>📧 Email: <a href='mailto:cropsavior.ai@gmail.com' style='color:#69f0ae;'>cropsavior.ai@gmail.com</a></p>
#         <p>🌐 Website: <a href='https://www.linkedin.com/in/tusharpatil/' target='_blank' style='color:#69f0ae;'>LinkedIn | CropSavior Team</a></p>
#     </div>
# """, unsafe_allow_html=True)

# # ------------------ FOOTER ------------------
# st.markdown("""
#     <footer>
#         © 2025 CropSavior | Designed with 💚 for Smarter Farming
#     </footer>
# """, unsafe_allow_html=True)


#------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests
# from PIL import Image
# from streamlit_lottie import st_lottie

# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()


# # ------------------ PAGE CONFIG ------------------
# st.set_page_config(page_title="🌾 CropSavior | AI Plant Doctor", layout="wide")

# # ------------------ BACKGROUND & GLOBAL STYLE ------------------
# def set_website_style(bg_url):
#     st.markdown(f"""
#         <style>
#         /* Background */
#         .stApp {{
#             background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
#                         url("{bg_url}") center/cover fixed;
#             color: white;s
#             font-family: 'Poppins', sans-serif;
#         }}

#         /* Navbar */
#         .navbar {{
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             padding: 1rem 3rem;
#             background: rgba(0, 0, 0, 0.4);
#             backdrop-filter: blur(10px);
#             border-bottom: 1px solid rgba(255, 255, 255, 0.1);
#         }}
#         .nav-links a {{
#             margin: 0 15px;
#             text-decoration: none;
#             color: #fff;
#             font-weight: 500;
#             transition: color 0.3s;
#         }}
#         .nav-links a:hover {{
#             color: #69f0ae;
#         }}

#         /* Logo Animation */
#         .logo {{
#             font-size: 1.6rem;
#             font-weight: 700;
#             background: linear-gradient(90deg, #00e676, #76ff03);
#             -webkit-background-clip: text;
#             color: transparent;
#             animation: glow 3s infinite alternate;
#         }}
#         @keyframes glow {{
#             from {{ text-shadow: 0 0 10px #00e676; }}
#             to {{ text-shadow: 0 0 25px #76ff03; }}
#         }}

#         /* Glass card for main UI */
#         .glass-card {{
#             background: rgba(255, 255, 255, 0.08);
#             backdrop-filter: blur(10px);
#             padding: 50px 70px;
#             border-radius: 25px;
#             margin: 60px auto;
#             max-width: 700px;
#             box-shadow: 0 0 30px rgba(0,0,0,0.3);
#             text-align: center;
#             animation: fadeIn 1s ease-in-out;
#         }}
#         @keyframes fadeIn {{
#             from {{ opacity: 0; transform: translateY(30px); }}
#             to {{ opacity: 1; transform: translateY(0); }}
#         }}

#         /* Buttons */
#         div.stButton > button:first-child {{
#             background: linear-gradient(90deg, #00e676, #76ff03);
#             color: #fff;
#             border: none;
#             border-radius: 30px;
#             font-weight: bold;
#             padding: 0.8rem 2.5rem;
#             transition: all 0.3s ease;
#         }}
#         div.stButton > button:hover {{
#             transform: scale(1.05);
#             box-shadow: 0 0 20px #00e676;
#         }}

#         /* Footer */
#         footer {{
#             text-align: center;
#             color: #bbb;
#             margin-top: 80px;
#             padding: 30px 0;
#             border-top: 1px solid rgba(255, 255, 255, 0.1);
#             font-size: 0.9rem;
#         }}
#         </style>
#     """, unsafe_allow_html=True)

# # ------------------ SET BACKGROUND ------------------
# set_website_style("https://images.unsplash.com/photo-1501004318641-b39e6451bec6")

# # ------------------ NAVBAR ------------------
# st.markdown("""
#     <div class="navbar">
#         <div class="logo">🌾 CropSavior</div>
#         <div class="nav-links">
#             <a href="#home">Home</a>
#             <a href="#about">About</a>
#             <a href="#contact">Contact</a>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# # ------------------ AGRICULTURE ANIMATION ------------------
# lottie_agriculture = load_lottieurl("https://lottie.host/1ef4a0f4-1a18-4e06-a9d9-9e6f91a6eecb/6iSz6eAqKm.json")

# if lottie_agriculture:
#     st_lottie(lottie_agriculture, height=320, key="farm_animation")


# # ------------------ MAIN SECTION ------------------
# st.markdown("<div id='home' class='glass-card'>", unsafe_allow_html=True)
# st.markdown("<h2>🧠 AI-Powered Plant Disease Detection</h2>", unsafe_allow_html=True)
# st.write("Upload a plant leaf image and enter your city to predict disease and get live weather insights 🌦️.")

# # 🌿 AI Animation Section
# from streamlit_lottie import st_lottie

# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# # Load a Lottie animation (beautiful leaf scan)
# lottie_leaf = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")

# if lottie_leaf:
#     st_lottie(lottie_leaf, height=280, key="leaf_scan")

# uploaded_file = st.file_uploader("📸 Upload Leaf Image", type=["jpg", "jpeg", "png"])


# # 🌿 ADD THIS SECTION BELOW
# st.markdown("<h3 style='text-align:center;'>🌿 Detect Plant Diseases Instantly with AI</h3>", unsafe_allow_html=True)

# st.image(
#     "https://lottie.host/2e0d0919-9ad7-4ff9-bbe3-c58322263d1f/leafscan.gif",  # ✅ Working replacement GIF
#     caption="Smart Leaf Scan in Action",
#     use_container_width=True
# )

# # 🌿 END OF ADDED SECTION
# uploaded_file = st.file_uploader("📸 Upload Leaf Image", type=["jpg", "jpeg", "png"])
# city = st.text_input("🏙️ Enter City Name (e.g., Pune)")

# if uploaded_file and city:
#     if st.button("🔍 Predict Disease"):
#         with st.spinner("Analyzing image and fetching weather data..."):
#             files = {"file": uploaded_file.getvalue()}
#             data = {"city": city}

#             try:
#                 response = requests.post("http://127.0.0.1:5000/predict", files={"file": uploaded_file}, data=data)
#                 if response.status_code == 200:
#                     result = response.json()
#                     st.success(f"✅ Prediction Successful for {result['city']}")
#                     st.image(uploaded_file, caption="Uploaded Leaf", use_column_width=True)

#                     st.subheader(f"🌱 Disease: {result['predicted_class']}")
#                     st.write(f"**Confidence:** {result['confidence']}%")

#                     st.subheader("💧 Weather Details:")
#                     st.write(f"🌤️ Weather: {result['weather_data']['weather']}")
#                     st.write(f"🌡️ Temperature: {result['weather_data']['temperature']}°C")
#                     st.write(f"💦 Humidity: {result['weather_data']['humidity']}%")
#                     st.write(f"🌾 Risk Level: {result['weather_data']['disease_risk']}")

#                     st.subheader("🩺 Remedies:")
#                     st.write(f"**Organic:** {result['remedies']['organic']}")
#                     st.write(f"**Chemical:** {result['remedies']['chemical']}")
#                     st.write(f"**Preventive:** {result['remedies']['preventive']}")
#                 else:
#                     st.error("❌ Could not fetch prediction. Please check your backend server.")
#             except Exception as e:
#                 st.error(f"⚠️ Error: {e}")
# else:
#     st.info("Please upload a leaf image and enter a city to begin.")
# st.markdown("</div>", unsafe_allow_html=True)

# # ------------------ ABOUT SECTION ------------------
# st.markdown("""
#     <div id='about' style='text-align:center; margin-top:100px;'>
#         <h2>🌿 About CropSavior</h2>
#         <p style='max-width:750px; margin:auto; color:#e0f7fa; font-size:1.1rem;'>
#             CropSavior uses advanced deep learning models to detect plant diseases from leaf images. 
#             Combined with real-time weather insights, it helps farmers take immediate action to prevent crop losses. 
#             Built to support sustainability, efficiency, and smarter farming practices. 🚜
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # ------------------ CONTACT SECTION ------------------
# st.markdown("""
#     <div id='contact' style='text-align:center; margin-top:100px;'>
#         <h2>📩 Contact Us</h2>
#         <p style='color:#b2dfdb;'>Have questions, feedback, or collaboration ideas?</p>
#         <p>📧 Email: <a href='mailto:cropsavior.ai@gmail.com' style='color:#69f0ae;'>cropsavior.ai@gmail.com</a></p>
#         <p>🌐 Website: <a href='https://www.linkedin.com/in/tusharpatil/' target='_blank' style='color:#69f0ae;'>LinkedIn | Tushar Patil</a></p>
#     </div>
# """, unsafe_allow_html=True)

# # ------------------ FOOTER ------------------
# st.markdown("""
#     <footer>
#         © 2025 CropSavior | Designed with 💚 by <b>Tushar Patil</b>
#     </footer>
# """, unsafe_allow_html=True)



#------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests
# from PIL import Image

# # --------------------- PAGE CONFIG ---------------------
# st.set_page_config(page_title="🌾 CropSavior | AI Plant Doctor", layout="wide")

# # --------------------- BACKGROUND STYLING ---------------------
# def set_background(image_url):
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{image_url}");
#             background-size: cover;
#             background-position: center;
#             background-attachment: fixed;
#             color: #ffffff;
#             font-family: 'Poppins', sans-serif;
#         }}

#         /* Headings & Text */
#         h1, h2, h3, h4, h5, h6, p, span, div {{
#             color: #ffffff !important;
#         }}

#         /* Center Card */
#         .glass-card {{
#             background: rgba(255, 255, 255, 0.08);
#             backdrop-filter: blur(10px);
#             padding: 40px 60px;
#             border-radius: 25px;
#             box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
#             margin-top: 50px;
#             text-align: center;
#             animation: fadeIn 1.2s ease-in-out;
#         }}

#         /* Button styling */
#         div.stButton > button:first-child {{
#             background: linear-gradient(90deg, #00c853, #64dd17);
#             color: white;
#             font-weight: bold;
#             border-radius: 30px;
#             padding: 0.75em 2.5em;
#             border: none;
#             transition: all 0.3s ease;
#         }}

#         div.stButton > button:hover {{
#             transform: scale(1.05);
#             box-shadow: 0 0 20px #00e676;
#         }}

#         /* Animations */
#         @keyframes fadeIn {{
#             from {{ opacity: 0; transform: translateY(20px); }}
#             to {{ opacity: 1; transform: translateY(0); }}
#         }}

#         /* Footer */
#         footer {{
#             text-align: center;
#             padding: 20px;
#             color: #bbb;
#             font-size: 0.9em;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # --------------------- ADD BACKGROUND ---------------------
# set_background("https://images.unsplash.com/photo-1501004318641-b39e6451bec6")

# # --------------------- HEADER ---------------------
# st.markdown(
#     """
#     <h1 style='text-align:center; font-size:3em; font-weight:700; background:linear-gradient(90deg, #00e676, #76ff03); -webkit-background-clip:text; color:transparent;'>
#         🌾 CropSavior
#     </h1>
#     <h3 style='text-align:center; color:#b9f6ca; margin-top:-15px;'>AI-Powered Plant Disease Detection</h3>
#     """,
#     unsafe_allow_html=True
# )

# # --------------------- MAIN CARD ---------------------
# st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

# uploaded_file = st.file_uploader("📸 Upload a Leaf Image", type=["jpg", "jpeg", "png"])
# city = st.text_input("🏙️ Enter City Name (e.g., Pune)")

# if uploaded_file and city:
#     if st.button("🔍 Predict Disease"):
#         with st.spinner("Analyzing image and fetching weather data..."):
#             files = {"file": uploaded_file.getvalue()}
#             data = {"city": city}
            
#             try:
#                 response = requests.post("http://127.0.0.1:5000/predict", files={"file": uploaded_file}, data=data)
#                 if response.status_code == 200:
#                     result = response.json()
#                     st.success(f"✅ Prediction Successful for {result['city']}")
#                     st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

#                     st.subheader(f"🌱 Disease: {result['predicted_class']}")
#                     st.write(f"**Confidence:** {result['confidence']}%")

#                     st.subheader("💧 Weather Details:")
#                     st.write(f"🌤️ Weather: {result['weather_data']['weather']}")
#                     st.write(f"🌡️ Temperature: {result['weather_data']['temperature']}°C")
#                     st.write(f"💦 Humidity: {result['weather_data']['humidity']}%")
#                     st.write(f"🌾 Risk Level: {result['weather_data']['disease_risk']}")

#                     st.subheader("🩺 Remedies:")
#                     st.write(f"**Organic:** {result['remedies']['organic']}")
#                     st.write(f"**Chemical:** {result['remedies']['chemical']}")
#                     st.write(f"**Preventive:** {result['remedies']['preventive']}")
#                 else:
#                     st.error("❌ Failed to connect with the server. Please try again.")
#             except Exception as e:
#                 st.error(f"⚠️ Error: {e}")
# else:
#     st.info("Please upload an image and enter a city name to start.")

# st.markdown("</div>", unsafe_allow_html=True)

# # --------------------- ABOUT SECTION ---------------------
# st.markdown(
#     """
#     <div style='text-align:center; margin-top:60px;'>
#         <h2>🌿 About CropSavior</h2>
#         <p style='max-width:700px; margin:auto; color:#e0f7fa;'>
#             CropSavior is an AI-driven platform designed to help farmers and plant enthusiasts detect leaf diseases early.
#             By integrating image analysis and live weather data, it offers accurate predictions and actionable remedies
#             to reduce crop losses and improve sustainability.
#         </p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# # --------------------- FOOTER ---------------------
# st.markdown(
#     """
#     <footer>
#         © 2025 CropSavior | Designed with 💚 by Tushar Patil
#     </footer>
#     """,
#     unsafe_allow_html=True
# )


#-----------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests
# from PIL import Image
# import base64

# # ----------------------------
# # 🌿 PAGE CONFIGURATION
# # ----------------------------
# st.set_page_config(page_title="CropSavior 🌾", page_icon="🌿", layout="centered")

# # Custom CSS for styling
# st.markdown("""
#     <style>
#         body {
#             background: linear-gradient(135deg, #d9f7e9 0%, #bff0da 100%);
#             font-family: 'Poppins', sans-serif;
#         }
#         .title {
#             text-align: center;
#             color: #155724;
#             font-size: 2.3em;
#             font-weight: 700;
#             margin-bottom: -5px;
#         }
#         .subtitle {
#             text-align: center;
#             color: #3c763d;
#             font-size: 1.1em;
#             margin-bottom: 30px;
#         }
#         .stButton button {
#             background: linear-gradient(90deg, #34c759, #28a745);
#             color: white;
#             border: none;
#             padding: 12px 25px;
#             border-radius: 10px;
#             font-size: 16px;
#             transition: 0.3s;
#         }
#         .stButton button:hover {
#             background: linear-gradient(90deg, #28a745, #34c759);
#             transform: scale(1.05);
#         }
#         .result-box {
#             background-color: #ffffff;
#             border-radius: 12px;
#             padding: 20px;
#             margin-top: 30px;
#             box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
#         }
#         img {
#             border-radius: 10px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ----------------------------
# # 🌾 HEADER
# # ----------------------------
# st.markdown('<h1 class="title">🌾 CropSavior</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Smart Plant Disease Detector powered by AI & Weather Intelligence</p>', unsafe_allow_html=True)

# # ----------------------------
# # 📸 IMAGE UPLOAD & CITY INPUT
# # ----------------------------
# uploaded_file = st.file_uploader("📸 Upload Plant Leaf Image", type=["jpg", "jpeg", "png"])
# city = st.text_input("🏙️ Enter City Name (e.g., Mumbai)")

# # ----------------------------
# # 🚀 PREDICTION LOGIC
# # ----------------------------
# if uploaded_file and city:
#     if st.button("🔍 Predict Disease"):
#         with st.spinner("Analyzing image and fetching weather data..."):
#             files = {"file": uploaded_file.getvalue()}
#             data = {"city": city}

#             try:
#                 response = requests.post("http://127.0.0.1:5000/predict", files={"file": uploaded_file}, data=data)

#                 if response.status_code == 200:
#                     result = response.json()
#                     st.success(f"✅ Prediction successful for {result['city']}")

#                     # Display uploaded image
#                     st.image(uploaded_file, caption="Uploaded Leaf Image", use_column_width=True)

#                     # Display results
#                     st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                     st.subheader("🧠 Prediction Results")
#                     st.write(f"**Disease:** {result['predicted_class']}")
#                     st.write(f"**Confidence:** {result['confidence']}%")

#                     st.subheader("🌦 Weather & Risk")
#                     weather = result['weather_data']
#                     st.write(f"**Weather:** {weather['weather']}")
#                     st.write(f"**Temperature:** {weather['temperature']} °C")
#                     st.write(f"**Humidity:** {weather['humidity']}%")
#                     st.warning(f"**Disease Risk:** {weather['disease_risk']}")

#                     st.subheader("💊 Remedies & Prevention")
#                     st.write(f"**Organic:** {result['remedies']['organic']}")
#                     st.write(f"**Chemical:** {result['remedies']['chemical']}")
#                     st.write(f"**Preventive:** {result['remedies']['preventive']}")
#                     st.markdown('</div>', unsafe_allow_html=True)

#                 else:
#                     st.error("❌ Failed to get prediction from the Flask backend. Please check the server.")
#             except Exception as e:
#                 st.error(f"⚠️ Error connecting to backend: {str(e)}")
# else:
#     st.info("Please upload a leaf image and enter a city name to proceed.")

# # ----------------------------
# # 🌿 FOOTER
# # ----------------------------
# st.markdown("""
# ---
# <p style='text-align:center; color:gray;'>
# 🌱 Built with ❤️ by <b>Tushar Patil</b> | CropSavior Project
# </p>
# """, unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests
# from PIL import Image
# import io

# st.set_page_config(page_title="🌿 CropSavior", layout="centered")

# st.title("🌾 CropSavior: Smart Plant Disease Detector")
# st.write("Upload a plant leaf image and select your city to predict the disease and view weather conditions.")

# uploaded_file = st.file_uploader("📸 Upload Leaf Image", type=["jpg", "jpeg", "png"])
# city = st.text_input("🏙️ Enter City Name (e.g., Pune)")

# if uploaded_file and city:
#     if st.button("🔍 Predict Disease"):
#         with st.spinner("Analyzing image and fetching weather..."):
#             files = {"file": uploaded_file.getvalue()}
#             data = {"city": city}
            
#             # Send request to your Flask backend
#             response = requests.post("http://127.0.0.1:5000/predict", files={"file": uploaded_file}, data=data)
            
#             if response.status_code == 200:
#                 result = response.json()
#                 st.success(f"✅ Prediction Successful for {result['city']}")

#                 st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
#                 st.subheader(f"🌱 Disease: {result['predicted_class']}")
#                 st.write(f"**Confidence:** {result['confidence']}%")

#                 st.subheader("💧 Weather Details:")
#                 st.write(f"🌤️ Weather: {result['weather_data']['weather']}")
#                 st.write(f"🌡️ Temperature: {result['weather_data']['temperature']}°C")
#                 st.write(f"💦 Humidity: {result['weather_data']['humidity']}%")
#                 st.write(f"🌾 Risk Level: {result['weather_data']['disease_risk']}")

#                 st.subheader("🩺 Remedies:")
#                 st.write(f"**Organic:** {result['remedies']['organic']}")
#                 st.write(f"**Chemical:** {result['remedies']['chemical']}")
#                 st.write(f"**Preventive:** {result['remedies']['preventive']}")
#             else:
#                 st.error("❌ Failed to get prediction from the server. Please try again.")
# else:
#     st.info("Please upload an image and enter a city name to proceed.")
