# 📡 OSINT Intelligence & Sentiment Pipeline

An automated, multi-platform intelligence pipeline that collects, extracts, and analyzes user-sentiment data across five major platforms: **Twitter**, **Reddit**, **GitHub**, **Hacker News**, and **YouTube**.

---

## **🚀 Key Features**
- **🔍 Multi-Source Collection**: Real-time data gathering from 5 major social/open-source platforms.
- **🧹 NLP Processing**: Automated text cleaning, URL removal, and English-language filtering.
- **🧠 Sentiment Analytics**: Uses **TextBlob** to assign polarity scores (-1.0 to 1.0) to all collected data.
- **📊 1-Click Dashboard**: Built with **Streamlit** to provide an interactive, visual look at live sentiment data.
- **💾 Persistent Storage**: Uses a local **SQLite** database for high-performance retrieval and historical analysis.

---

## **📂 Project Structure**
- `main.py`: CLI-based entry point for scheduled runs.
- `dashboard.py`: Interactive web-based dashboard and control panel.
- `collectors/`: Specialized modules for each platform (Twitter, Reddit, GitHub, HN, YouTube).
- `utils/`: Core processing logic (cleaner, database, sentiment, visualizer).
- `data/`: Local database storage (`osint.db`).
- `reports/`: Automatically generated PNG sentiment visualizations.

---

## **🛠 Setup & Installation**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Configure Environment Variables**
Create a `.env` file from the template and add your API keys:
```bash
cp .env.template .env
```

### **3. Launch the Dashboard**
Enjoy the visual experience:
```bash
streamlit run dashboard.py
```

---

## **📊 Visualization Preview**
The dashboard visualizes average sentiment across platforms using **Plotly**, allowing you to compare user moods and trending sentiments in real-time.

---

## **⚖️ License**
This project is licensed under the **MIT License**.
