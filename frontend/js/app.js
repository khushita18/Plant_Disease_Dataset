const API_URL = "http://localhost:5000/predict"; // Flask backend

const imageInput = document.getElementById("imageInput");
const cityInput = document.getElementById("city");
const analyzeBtn = document.getElementById("analyzeBtn");
const preview = document.getElementById("preview");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const resultContent = document.getElementById("resultContent");

// Lottie Animation
const anim = lottie.loadAnimation({
  container: document.getElementById("lottieContainer"),
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "https://assets6.lottiefiles.com/packages/lf20_touohxv0.json"
});

imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.innerHTML = `<img src="${e.target.result}" alt="Preview Image" />`;
    };
    reader.readAsDataURL(file);
  }
});

analyzeBtn.addEventListener("click", async () => {
  const file = imageInput.files[0];
  const city = cityInput.value;

  if (!file) {
    alert("Please upload a leaf image first.");
    return;
  }

  loading.classList.remove("hidden");
  result.classList.add("hidden");

  const formData = new FormData();
  formData.append("image", file);
  formData.append("city", city);

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    loading.classList.add("hidden");
    result.classList.remove("hidden");

    if (res.status === 200) {
      resultContent.innerHTML = `
        <h3>${data.disease}</h3>
        <p><strong>Confidence:</strong> ${data.confidence}%</p>
        <h4>🌦️ Weather Info:</h4>
        <p>${data.weather?.main?.temp ? `${data.weather.main.temp}°C, ${data.weather.weather[0].main}` : "N/A"}</p>
        <h4>💊 Remedies:</h4>
        <ul>${data.remedies.map(r => `<li>${r}</li>`).join("")}</ul>
      `;
    } else {
      resultContent.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
    }
  } catch (err) {
    loading.classList.add("hidden");
    alert("Server Error: Unable to fetch prediction.");
    console.error(err);
  }
});
