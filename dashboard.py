import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime
from collections import Counter
import re
import nltk

# Download required NLTK data for sentiment analysis
try:
    nltk.download('punkt')
    nltk.download('punkt_tab')
except:
    pass

# Import your collectors
from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from collectors.github_collector import fetch_github
from collectors.hacker_news_collector import fetch_hn
from collectors.youtube_collector import fetch_youtube

# Import your utils
from utils.cleaner import clean_text, filter_english
from utils.sentiment import add_sentiment
from utils.database import save_to_db

st.set_page_config(page_title="🛰️ OSINT COMMAND CENTER", layout="wide", page_icon="⚡")

# --- 🌌 NEON STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    div.stMetric { background: rgba(0, 242, 255, 0.03); border: 1px solid #00f2ff33; border-radius: 12px; }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { background: linear-gradient(135deg, #238636 0%, #2ea043 100%); color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background: #3fb950; transform: scale(1.02); transition: 0.2s; }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
c1, c2 = st.columns([0.15, 0.85])
with c1: st.write("# 📡")
with c2: 
    st.title("OSINT COMMAND CENTER v2.5")
    st.markdown("<p style='color: #8b949e; margin-top: -15px;'>CORE-ENGINE ACTIVE | SIGNAL LOCK READY</p>", unsafe_allow_html=True)

# --- SIDEBAR CONTROL ---
with st.sidebar:
    st.markdown("### 🔍 SIGNAL TARGET")
    query = st.text_input("TARGET QUERY:", "cybersecurity threats")
    limit = st.slider("SIGNAL DEPTH (Records):", 5, 20, 10)
    
    st.divider()
    if st.button("🚀 EXECUTE INFILTRATION", use_container_width=True):
        with st.status("📡 Intercepting Packets...", expanded=True) as status:
            data = []
            st.write("🛰️ Scanning X (Twitter)...")
            data += fetch_twitter(query, limit)
            st.write("👽 Penetrating Reddit...")
            data += fetch_reddit("technology", limit)
            st.write("🐙 Exploring GitHub...")
            data += fetch_github(query, limit)
            st.write("🌐 Intercepting Hacker News...")
            data += fetch_hn(limit)
            st.write("📺 Decoding YouTube signals...")
            data += fetch_youtube(query, limit)
            
            st.write("🧹 Scrubbing artifacts...")
            for d in data: d["text"] = clean_text(d.get("text", ""))
            data = filter_english(data)
            
            st.write("🧠 Extracting Sentiment...")
            data = add_sentiment(data)
            
            st.write("💾 Encoding to Database...")
            save_to_db(data)
            status.update(label="✅ SECTOR SCANNED. INTEL STORED.", state="complete", expanded=False)
        st.rerun()

    st.divider()
    st.markdown("### ⚙️ SYSTEM RECOVERY")
    if st.button("🗑️ WIPE DATABASE", use_container_width=True, type="secondary", help="Irreversibly clears all intercepted intelligence packets."):
        try:
            conn = sqlite3.connect("data/osint.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM osint_data")
            conn.commit()
            conn.close()
            st.warning("⚠️ INTELLIGENCE BUFFER PURGED.")
            st.rerun()
        except:
            st.error("❌ PURGE ACTION FAILED.")

# --- DATA PROCESSING ---
def load_data():
    try:
        conn = sqlite3.connect("data/osint.db")
        df = pd.read_sql("SELECT * FROM osint_data ORDER BY rowid DESC", conn)
        conn.close()
        return df
    except: return pd.DataFrame()

df = load_data()

if df.empty:
    st.info("🌑 SIGNAL LOST. INITIATE SCAN TO BEGIN PROTOCOL.")
else:
    # --- CYBER GAUGE & METRICS ---
    col1, col2 = st.columns([0.4, 0.6])
    
    with col1:
        avg_sent = df['sentiment'].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_sent,
            title = {'text': "⚡ SIGNAL VIBE GAUGE", 'font': {'size': 20, 'color': "#58a6ff"}},
            gauge = {
                'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "#58a6ff"},
                'bar': {'color': "#00f2ff"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#58a6ff",
                'steps': [
                    {'range': [-1, -0.2], 'color': 'rgba(255, 65, 54, 0.3)'},
                    {'range': [-0.2, 0.2], 'color': 'rgba(255, 255, 255, 0.1)'},
                    {'range': [0.2, 1], 'color': 'rgba(63, 185, 80, 0.3)'}],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': avg_sent}}))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#58a6ff", 'family': "Courier New"})
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("📦 TOTAL INTEL", f"{len(df):,}")
        m2.metric("📡 PLATFORMS", df['platform'].nunique())
        m3.metric("🧠 CORE SCORE", f"{avg_sent:.2f}")
        
        st.divider()
        st.markdown("### 📥 DATA PROTOCOL")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 DOWNLOAD INTEL REPORT (CSV)", csv, "osint_intel_report.csv", "text/csv", use_container_width=True)

    # --- INTELLIGENCE TABS ---
    t1, t2, t3 = st.tabs(["📉 SECTOR TRENDS", "🏷️ KEYWORD INTEL", "🕵️ INTEL LOGS"])
    
    with t1:
        st.markdown("### 📑 SENTIMENT POLARITY BY HUB")
        df_sent = df.groupby('platform')['sentiment'].mean().reset_index()
        fig_sent = px.bar(df_sent, x='platform', y='sentiment', color='platform',
                          template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig_sent, use_container_width=True)

    with t2:
        st.markdown("### 🏷️ TOP SECTOR KEYWORDS")
        def get_top_words(texts):
            words = []
            for t in texts:
                # Remove special chars and lowercase
                clean = re.sub(r'[^a-zA-Z\s]', '', t.lower())
                words.extend([w for w in clean.split() if len(w) > 4 and w not in ['about', 'should', 'could', 'would']])
            return Counter(words).most_common(12)
        
        top_words = get_top_words(df['text'])
        if top_words:
            w_df = pd.DataFrame(top_words, columns=['Word', 'Impact'])
            fig_words = px.bar(w_df, x='Impact', y='Word', orientation='h', 
                               template="plotly_dark", color='Impact', color_continuous_scale="Viridis")
            st.plotly_chart(fig_words, use_container_width=True)

    with t3:
        st.markdown("### 🕵️ RAW INTEL INTERCEPTION STREAM")
        st.dataframe(df[['platform', 'user', 'sentiment', 'text']].head(100), use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e;'>OSINT PROTOCOL ENABLED | BUILT BY ALOK SINHA</p>", unsafe_allow_html=True)
