# 🔎 OSINT Aggregation Pipeline

## 📌 Overview
This project is an **Open Source Intelligence (OSINT) pipeline** that collects, processes, and analyzes data from:
- 🐦 Twitter  
- 👽 Reddit  
- 🐙 GitHub  

It performs:
- Text cleaning  
- Language detection (English filtering)  
- Sentiment analysis (using TextBlob)  
- Storage into an **SQLite database**  
- Visualization of **average sentiment by platform**

---

## 🛠 Tools & Technologies
- **Data Collection**: Tweepy (Twitter), PRAW (Reddit), PyGithub (GitHub)  
- **Processing**: Regex (`re`), LangDetect  
- **Analysis**: TextBlob (sentiment polarity)  
- **Database**: SQLite  
- **Visualization**: Matplotlib, Pandas  

---

## 🚀 Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aloksinha123/osint-pipeline.git
   cd osint-pipeline
