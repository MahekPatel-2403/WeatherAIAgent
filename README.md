# 🌦️ Weather AI Agent

A simple AI-powered weather assistant that fetches real-time weather data for any city using an external API and processes it through a structured Python backend.

---

## 🚀 Features

* 🌍 Get real-time weather data for any city
* 🤖 AI-agent style architecture (modular design)
* ⚙️ Clean separation of logic (`app.py`, `_utils.py`)
* 🔌 API integration (WeatherAPI / Open-Meteo)
* 🧠 Easy to extend into a full AI agent

---

## 📁 Project Structure

```
Weather-AI-Agent/
│
├── app.py                # Main entry point
├── agent/
│   ├── __init__.py
│   ├── _utils.py        # Utility functions (API calls, parsing)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Installation

1. Clone the repository:

```
git clone https://github.com/your-username/weather-ai-agent.git
cd weather-ai-agent
```

2. Create a virtual environment:

```
python -m venv .venv
.venv\Scripts\activate   # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

---

## 🔑 API Setup

This project uses a weather API.

### Option 1: WeatherAPI

* Get your API key from: https://www.weatherapi.com/
* Replace in code:

```
API_KEY = "your_api_key"
```

---

## ▶️ Usage

Run the application:

```
python app.py
```

Enter a city name when prompted:

```
Enter city: Delhi
```

Example output:

```
Temperature: 32°C
Condition: Sunny
Humidity: 45%
```

---

## ⚠️ Common Issues

### ❌ ModuleNotFoundError

* Ensure correct imports:

```
from agent import _utils
```

---

### ❌ API Errors

* Check API key
* Ensure correct URL format:

```
http://api.weatherapi.com/v1/current.json?key=API_KEY&q=city
```

---

### ❌ Usage Limit Reached

* Free API plans have limits
* Switch to Open-Meteo (no API key required)

---

## 🧠 Future Improvements

* 🔄 Add forecast support
* 🌐 Build a FastAPI backend
* 💬 Integrate with LLM (LangChain)
* 📊 Add UI (React frontend)
* 🧠 Make it a fully autonomous AI agent

---

## 🤝 Contributing

Pull requests are welcome!
Feel free to fork and improve the project.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Mahek Patel**
Backend Developer | AI Enthusiast

---
