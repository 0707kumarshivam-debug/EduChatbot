import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os
import json

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="EduVerse",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# CHAT HISTORY LOGGER
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_HISTORY_FILE = os.path.join(BASE_DIR, "chat_history.csv")


def save_chat(user_message, bot_reply):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_data = pd.DataFrame({
        "timestamp": [timestamp],
        "user_message": [user_message],
        "bot_reply": [bot_reply]
    })

    try:
        print("📁 CSV PATH:", CHAT_HISTORY_FILE, flush=True)

        if os.path.exists(CHAT_HISTORY_FILE) and os.path.getsize(CHAT_HISTORY_FILE) > 0:
            old_df = pd.read_csv(CHAT_HISTORY_FILE)
            updated_df = pd.concat([old_df, new_data], ignore_index=True)
            updated_df.to_csv(CHAT_HISTORY_FILE, index=False, encoding="utf-8")
            print("✅ Chat appended to CSV", flush=True)
        else:
            new_data.to_csv(CHAT_HISTORY_FILE, index=False, encoding="utf-8")
            print("✅ New CSV created", flush=True)

    except Exception as e:
        print("❌ CSV Save Error:", e, flush=True)

# =========================================
# GLOBAL CSS
# =========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;700&family=DM+Sans:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
.stApp { background: #f0ede8; font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* NAVBAR */
.navbar { display: flex; justify-content: space-between; align-items: center; padding: 18px 48px; background: #0f1117; border-bottom: 1px solid #1e2130; }
.nav-logo { font-family: 'Fraunces', serif; font-size: 26px; font-weight: 700; color: #f5f0e8; letter-spacing: -0.5px; }
.nav-logo span { color: #e8b84b; }
.nav-links { display: flex; gap: 32px; align-items: center; }
.nav-link { color: #8b95a8; font-size: 14px; font-weight: 500; cursor: pointer; }
.nav-cta { background: #e8b84b; color: #0f1117; padding: 10px 22px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; border: none; }

/* HERO */
.hero { display: grid; grid-template-columns: 1fr 1fr; gap: 0; min-height: 480px; background: #0f1117; padding: 64px 48px; align-items: center; }
.hero-left h1 { font-family: 'Fraunces', serif; font-size: 52px; font-weight: 700; color: #f5f0e8; line-height: 1.1; margin: 0 0 16px; letter-spacing: -1.5px; }
.hero-left h1 em { font-style: normal; color: #e8b84b; }
.hero-left p { font-size: 17px; color: #8b95a8; line-height: 1.6; margin: 0 0 32px; max-width: 480px; }
.hero-btns { display: flex; gap: 14px; flex-wrap: wrap; }
.btn-primary { background: #e8b84b; color: #0f1117; padding: 14px 28px; border-radius: 10px; font-weight: 600; font-size: 15px; text-decoration: none; display: inline-block; }
.btn-outline { border: 1.5px solid #2a2f3e; color: #f5f0e8; padding: 14px 28px; border-radius: 10px; font-weight: 600; font-size: 15px; text-decoration: none; display: inline-block; }
.hero-stats { display: flex; gap: 36px; margin-top: 40px; }
.stat-num { font-family: 'Fraunces', serif; font-size: 28px; font-weight: 700; color: #f5f0e8; }
.stat-label { font-size: 13px; color: #8b95a8; margin-top: 2px; }
.hero-right { display: flex; justify-content: center; align-items: center; }
.hero-badge-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; max-width: 360px; }
.hero-badge { background: #1a1f2e; border: 1px solid #2a2f3e; border-radius: 14px; padding: 20px; text-align: center; }
.hero-badge .hb-icon { font-size: 32px; margin-bottom: 8px; }
.hero-badge .hb-label { font-size: 13px; color: #8b95a8; font-weight: 500; }
.hero-badge .hb-value { font-family: 'Fraunces', serif; font-size: 18px; font-weight: 600; color: #f5f0e8; margin-top: 4px; }

/* SECTIONS */
.section-wrap { padding: 40px 48px 0 48px; }
.section-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 24px; }
.section-title { font-family: 'Fraunces', serif; font-size: 32px; font-weight: 700; color: #1a1814; letter-spacing: -0.8px; }
.section-link { font-size: 14px; font-weight: 600; color: #2563eb; cursor: pointer; }

/* WHY SECTION */
.why-section { background: #0f1117; padding: 60px 48px; margin-top: 8px; }
.why-title { font-family: 'Fraunces', serif; font-size: 36px; font-weight: 700; color: #f5f0e8; text-align: center; margin-bottom: 8px; }
.why-sub { text-align: center; color: #8b95a8; font-size: 15px; margin-bottom: 40px; }
.why-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.why-card { background: #1a1f2e; border: 1px solid #2a2f3e; border-radius: 16px; padding: 28px 22px; text-align: center; }
.why-icon { font-size: 36px; margin-bottom: 14px; }
.why-heading { font-family: 'Fraunces', serif; font-size: 18px; font-weight: 600; color: #f5f0e8; margin-bottom: 8px; }
.why-text { font-size: 13px; color: #8b95a8; line-height: 1.6; }

/* FOOTER */
.footer { background: #0f1117; padding: 48px 48px 24px; border-top: 1px solid #1e2130; margin-top: 48px; }
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
.footer-logo { font-family: 'Fraunces', serif; font-size: 22px; font-weight: 700; color: #f5f0e8; margin-bottom: 10px; }
.footer-logo span { color: #e8b84b; }
.footer-desc { font-size: 13px; color: #8b95a8; line-height: 1.6; max-width: 260px; }
.footer-col-title { font-size: 13px; font-weight: 600; color: #f5f0e8; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.6px; }
.footer-link { display: block; font-size: 13px; color: #8b95a8; margin-bottom: 8px; cursor: pointer; }
.footer-bottom { border-top: 1px solid #1e2130; padding-top: 20px; display: flex; justify-content: space-between; align-items: center; }
.footer-copy { font-size: 12px; color: #8b95a8; }
.footer-badges { display: flex; gap: 10px; }
.badge { background: #1a1f2e; border: 1px solid #2a2f3e; padding: 4px 12px; border-radius: 20px; font-size: 11px; color: #8b95a8; }

[data-testid="stHorizontalBlock"] { padding-left: 48px; padding-right: 48px; }
iframe { display: block; border: none !important; }
</style>
""", unsafe_allow_html=True)

# =========================================
# NAVBAR
# =========================================

st.markdown("""
<div class="navbar">
    <div class="nav-logo">Edu<span>Verse</span></div>
    <div class="nav-links">
        <span class="nav-link">Courses</span>
        <span class="nav-link">Projects</span>
        <span class="nav-link">Mentors</span>
        <span class="nav-link">Placements</span>
        <span class="nav-link">Blog</span>
        <button class="nav-cta">Get Started</button>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# HERO
# =========================================

st.markdown("""
<div class="hero">
    <div class="hero-left">
        <h1>Master <em>AI &amp; Data</em><br>Skills That Pay</h1>
        <p>Industry-led programs in Python, Data Science, Machine Learning
        and AI — with real projects, mentorship, and placement support.</p>
        <div class="hero-btns">
            <a class="btn-primary" href="#">Explore Courses</a>
            <a class="btn-outline" href="#">Chat with EduBot</a>
        </div>
        <div class="hero-stats">
            <div><div class="stat-num">12,000+</div><div class="stat-label">Students Enrolled</div></div>
            <div><div class="stat-num">94%</div><div class="stat-label">Placement Rate</div></div>
            <div><div class="stat-num">4.8 Star</div><div class="stat-label">Average Rating</div></div>
        </div>
    </div>
    <div class="hero-right">
        <div class="hero-badge-grid">
            <div class="hero-badge"><div class="hb-icon">🐍</div><div class="hb-label">Python</div><div class="hb-value">Beginner</div></div>
            <div class="hero-badge"><div class="hb-icon">🤖</div><div class="hb-label">Machine Learning</div><div class="hb-value">Advanced</div></div>
            <div class="hero-badge"><div class="hb-icon">📊</div><div class="hb-label">Data Science</div><div class="hb-value">Industry</div></div>
            <div class="hero-badge"><div class="hb-icon">🧠</div><div class="hb-label">Gen AI</div><div class="hb-value">Cutting Edge</div></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# SEARCH + FILTERS
# =========================================

col_search, col_cat, col_level, col_dur = st.columns([3, 1.5, 1.5, 1.5])
with col_search:
    st.text_input("", placeholder="Search courses — Python, AI, Power BI...", label_visibility="collapsed")
with col_cat:
    st.selectbox("", ["All Categories", "Data Science", "AI / ML", "Programming", "Analytics", "Cloud"],
                 label_visibility="collapsed")
with col_level:
    st.selectbox("", ["All Levels", "Beginner", "Intermediate", "Advanced"], label_visibility="collapsed")
with col_dur:
    st.selectbox("", ["Any Duration", "Less than 3 Months", "3 to 6 Months", "6+ Months"], label_visibility="collapsed")

# =========================================
# FEATURED COURSES — Section Header
# =========================================

st.markdown("""
<div class="section-wrap">
    <div class="section-header">
        <div class="section-title">Featured Courses</div>
        <span class="section-link">View All</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# FEATURED COURSES — Card Grid
# =========================================

courses = [
    ("thumb-blue", "🐍", "Beginner", "Python Programming",
     "From fundamentals to OOP, file handling, and automation with real-world projects.",
     "Rs. 29,990", "3 Months · 60 hrs"),
    ("thumb-purple", "📊", "Industry", "Data Science",
     "Statistics, Pandas, SQL, EDA, and 5 industry-grade capstone projects.",
     "Rs. 49,990", "8 Months · 200 hrs"),
    ("thumb-green", "🤖", "Advanced", "Machine Learning",
     "Supervised, unsupervised, deep learning, NLP and model deployment pipelines.",
     "Rs. 59,990", "6 Months · 150 hrs"),
    ("thumb-amber", "📈", "Analytics", "Power BI",
     "DAX, data modelling, live dashboards and enterprise reporting workflows.",
     "Rs. 34,990", "3 Months · 75 hrs"),
    ("thumb-rose", "🧠", "Cutting Edge", "Generative AI",
     "LLMs, prompt engineering, LangChain, RAG systems and AI product building.",
     "Rs. 54,990", "4 Months · 100 hrs"),
    ("thumb-teal", "☁️", "Cloud", "AWS + Azure",
     "Cloud fundamentals, storage, compute, deployment and certification prep.",
     "Rs. 44,990", "5 Months · 120 hrs"),
    ("thumb-indigo", "🗄️", "Database", "SQL and NoSQL",
     "MySQL, PostgreSQL, MongoDB — queries, indexing, and database design patterns.",
     "Rs. 24,990", "2 Months · 50 hrs"),
    ("thumb-orange", "📉", "Finance", "Financial Analytics",
     "Excel, Python for finance, risk modelling and investment analytics dashboards.",
     "Rs. 39,990", "4 Months · 90 hrs"),
]

cards_html = ""
for thumb, icon, tag, title, desc, price, duration in courses:
    cards_html += f"""
    <div class="course-card">
        <div class="course-thumb {thumb}">{icon}</div>
        <div class="course-body">
            <span class="course-tag">{tag}</span>
            <div class="course-title">{title}</div>
            <div class="course-desc">{desc}</div>
            <div class="course-footer-row">
                <div>
                    <div class="course-price">{price}</div>
                    <div class="course-duration">{duration}</div>
                </div>
                <button class="enroll-btn">Enroll Now</button>
            </div>
        </div>
    </div>"""

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #f0ede8; font-family: 'DM Sans', sans-serif; padding: 0 48px 24px 48px; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }}
  .course-card {{ background: #fff; border-radius: 16px; overflow: hidden; border: 1px solid #e5e1d8; cursor: pointer; transition: transform .18s, box-shadow .18s; }}
  .course-card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 28px rgba(0,0,0,0.08); }}
  .course-thumb {{ height: 130px; display: flex; align-items: center; justify-content: center; font-size: 50px; }}
  .thumb-blue   {{ background: linear-gradient(135deg, #dbeafe, #bfdbfe); }}
  .thumb-purple {{ background: linear-gradient(135deg, #ede9fe, #ddd6fe); }}
  .thumb-green  {{ background: linear-gradient(135deg, #dcfce7, #bbf7d0); }}
  .thumb-amber  {{ background: linear-gradient(135deg, #fef3c7, #fde68a); }}
  .thumb-rose   {{ background: linear-gradient(135deg, #ffe4e6, #fecdd3); }}
  .thumb-teal   {{ background: linear-gradient(135deg, #ccfbf1, #99f6e4); }}
  .thumb-indigo {{ background: linear-gradient(135deg, #e0e7ff, #c7d2fe); }}
  .thumb-orange {{ background: linear-gradient(135deg, #ffedd5, #fed7aa); }}
  .course-body {{ padding: 16px 18px 20px; }}
  .course-tag {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; letter-spacing: 0.4px; text-transform: uppercase; background: #f0ede8; color: #6b6357; margin-bottom: 8px; }}
  .course-title {{ font-family: 'Fraunces', serif; font-size: 17px; font-weight: 600; color: #1a1814; margin: 0 0 6px; line-height: 1.3; }}
  .course-desc {{ font-size: 13px; color: #8a8072; line-height: 1.5; margin: 0 0 14px; }}
  .course-footer-row {{ display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid #f0ede8; }}
  .course-price {{ font-size: 17px; font-weight: 700; color: #1a1814; }}
  .course-duration {{ font-size: 12px; color: #8a8072; margin-top: 2px; }}
  .enroll-btn {{ background: #1a1814; color: #f5f0e8; padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; transition: background .2s; }}
  .enroll-btn:hover {{ background: #e8b84b; color: #0f1117; }}
</style>
</head>
<body>
  <div class="grid">{cards_html}</div>
</body>
</html>
""", height=780, scrolling=False)

# =========================================
# WHY CHOOSE US
# =========================================

st.markdown("""
<div class="why-section">
    <div class="why-title">Why 12,000+ Students Choose EduVerse</div>
    <div class="why-sub">Everything you need to land a tech career in one platform.</div>
    <div class="why-grid">
        <div class="why-card">
            <div class="why-icon">🤖</div>
            <div class="why-heading">EduBot AI Tutor</div>
            <div class="why-text">24/7 AI assistant that answers doubts, explains concepts, and reviews your code in real time.</div>
        </div>
        <div class="why-card">
            <div class="why-icon">🏗️</div>
            <div class="why-heading">Industry Projects</div>
            <div class="why-text">Build 5 to 10 real projects per course with data from actual companies to strengthen your portfolio.</div>
        </div>
        <div class="why-card">
            <div class="why-icon">🎯</div>
            <div class="why-heading">Placement Support</div>
            <div class="why-text">Resume review, mock interviews, LinkedIn optimisation, and direct referrals to 200+ hiring partners.</div>
        </div>
        <div class="why-card">
            <div class="why-icon">🏅</div>
            <div class="why-heading">Verified Certificates</div>
            <div class="why-text">Industry-recognised certifications with QR verification — directly shareable on LinkedIn.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# STUDENT STORIES — Section Header
# =========================================

st.markdown("""
<div class="section-wrap">
    <div class="section-header">
        <div class="section-title">Student Stories</div>
        <span class="section-link">Read More</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# STUDENT STORIES — Card Grid
# =========================================

testimonials = [
    ("#6366f1", "PR", "Priya Rajan", "Data Analyst, Infosys, Bangalore",
     "EduVerse's Data Science program completely transformed my career. I went from a commerce background to landing a data analyst role at a top MNC in just 8 months."),
    ("#0891b2", "AK", "Arjun Kumar", "ML Engineer, Swiggy, Delhi",
     "The ML course content is on par with international programs. EduBot helped me clear every concept at 2 AM when I was stuck. Incredible platform."),
    ("#d97706", "SM", "Shreya Mehta", "Business Analyst, TCS, Mumbai",
     "Placement cell is outstanding. Got 3 interview calls within 2 weeks of completing the program. The mock interviews really prepared me for the real thing."),
]

t_cards_html = ""
for color, initials, name, role, quote in testimonials:
    t_cards_html += f"""
    <div class="testimonial-card">
        <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <div class="testimonial-text">"{quote}"</div>
        <div class="testimonial-author">
            <div class="author-avatar" style="background:{color};">{initials}</div>
            <div>
                <div class="author-name">{name}</div>
                <div class="author-role">{role}</div>
            </div>
        </div>
    </div>"""

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #f0ede8; font-family: 'DM Sans', sans-serif; padding: 0 48px 24px 48px; }}
  .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }}
  .testimonial-card {{ background: #fff; border: 1px solid #e5e1d8; border-radius: 16px; padding: 24px; transition: transform .18s, box-shadow .18s; }}
  .testimonial-card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.07); }}
  .stars {{ color: #e8b84b; font-size: 15px; margin-bottom: 12px; }}
  .testimonial-text {{ font-size: 14px; color: #4a4540; line-height: 1.7; margin-bottom: 16px; font-style: italic; }}
  .testimonial-author {{ display: flex; align-items: center; gap: 10px; }}
  .author-avatar {{ width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; color: white; flex-shrink: 0; }}
  .author-name {{ font-weight: 600; font-size: 14px; color: #1a1814; }}
  .author-role {{ font-size: 12px; color: #8a8072; }}
</style>
</head>
<body>
  <div class="grid">{t_cards_html}</div>
</body>
</html>
""", height=290, scrolling=False)
st.markdown("""
<div 
</div>
""", unsafe_allow_html=True)

# =========================================
# STREAMLIT BACKEND ENDPOINT
# =========================================

if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = []

chat_data = st.text_area(
    label="chat_backend_receiver",
    key="chat_backend_receiver",
    height=1,
    label_visibility="collapsed"
)

if chat_data:
    print("✅ Python received:", chat_data, flush=True)

    try:
        data = json.loads(chat_data)

        user_message = data.get("user_message", "").strip()
        bot_reply = data.get("bot_reply", "").strip()

        current_pair = (user_message, bot_reply)

        if user_message and bot_reply and current_pair not in st.session_state.chat_logs:
            save_chat(user_message, bot_reply)
            st.session_state.chat_logs.append(current_pair)
            print("✅ Saved Successfully", flush=True)

    except Exception as e:
        print("❌ Save Error:", e, flush=True)

# =========================================
# FLOATING EDUBOT CHATBOT WIDGET
# =========================================

# Pull secrets and escape backticks so they don't break JS template literals
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

SYSTEM_PROMPT = (
    "You are EduBot, the friendly AI assistant for EduVerse — India's leading edtech platform based in Delhi.\n\n"
    "EduVerse courses:\n"
    "- Python Programming (Beginner) — Rs. 29,990 | 3 Months · 60 hrs\n"
    "- Data Science (Industry) — Rs. 49,990 | 8 Months · 200 hrs\n"
    "- Machine Learning (Advanced) — Rs. 59,990 | 6 Months · 150 hrs\n"
    "- Power BI (Analytics) — Rs. 34,990 | 3 Months · 75 hrs\n"
    "- Generative AI (Cutting Edge) — Rs. 54,990 | 4 Months · 100 hrs\n"
    "- AWS + Azure (Cloud) — Rs. 44,990 | 5 Months · 120 hrs\n"
    "- SQL and NoSQL (Database) — Rs. 24,990 | 2 Months · 50 hrs\n"
    "- Financial Analytics (Finance) — Rs. 39,990 | 4 Months · 90 hrs\n\n"
    "Contact Information:\n"
    "Phone: +91-7827833259\n"
    "Email: 0707kumar.shivam@gmail.com\n"
    "Office: Tower B hauz khas village 110030, India\n\n"
    "edubot personal information:\n"
    "Creator -  Shivam kumar bharti.\n"
    "Key facts: 12,000+ students, 94% placement rate, 4.8 star rating, 200+ hiring partners, "
    "verified LinkedIn certificates, Delhi-based.\n"
    "Be warm, concise, and helpful. Keep responses under 120 words. Use line breaks for readability."
)

# Escape for JS template literals
safe_key = GROQ_API_KEY.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
safe_system = SYSTEM_PROMPT.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

# ════════════════════════════════════════════════════════════════════════════════
# THE FIX: Inject a <script> into the parent (Streamlit) document that appends
# the floating chat widget directly to document.body of the top-level page.
# This completely bypasses the iframe fixed-position limitation.
# ════════════════════════════════════════════════════════════════════════════════

CHATBOT_INJECTOR = f"""
<script>
(function() {{
  // ── Guard: only inject once ──────────────────────────────────────────────
  if (window.parent.document.getElementById('ev-chat-fab')) return;

  const p = window.parent.document;

  // ── 1. Inject Google Fonts into parent <head> ────────────────────────────
  if (!p.getElementById('ev-fonts')) {{
    const lnk = p.createElement('link');
    lnk.id   = 'ev-fonts';
    lnk.rel  = 'stylesheet';
    lnk.href = 'https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap';
    p.head.appendChild(lnk);
  }}

  // ── 2. Inject CSS into parent <head> ─────────────────────────────────────
  if (!p.getElementById('ev-chat-style')) {{
    const style = p.createElement('style');
    style.id = 'ev-chat-style';
    style.textContent = `
      #ev-chat-fab {{
        position: fixed !important;
        bottom: 28px !important;
        right: 28px !important;
        width: 62px !important;
        height: 62px !important;
        border-radius: 50% !important;
        background: #e8b84b !important;
        border: none !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 28px rgba(232,184,75,0.55) !important;
        z-index: 2147483647 !important;
        transition: transform .22s, box-shadow .22s !important;
        font-family: 'DM Sans', sans-serif !important;
      }}
      #ev-chat-fab:hover {{
        transform: scale(1.08) !important;
        box-shadow: 0 6px 36px rgba(232,184,75,0.65) !important;
      }}
      #ev-chat-fab .ev-ic {{ position:absolute; transition: opacity .25s, transform .3s; }}
      #ev-chat-fab .ev-ic-chat  {{ opacity:1; transform:rotate(0deg); }}
      #ev-chat-fab .ev-ic-close {{ opacity:0; transform:rotate(-90deg); }}
      #ev-chat-fab.open .ev-ic-chat  {{ opacity:0; transform:rotate(90deg); }}
      #ev-chat-fab.open .ev-ic-close {{ opacity:1; transform:rotate(0deg); }}
      #ev-badge {{
        position:absolute; top:-3px; right:-3px;
        width:19px; height:19px; background:#ef4444;
        border:2.5px solid #fff; border-radius:50%;
        font-size:10px; font-weight:700; color:#fff;
        display:flex; align-items:center; justify-content:center;
        pointer-events:none; font-family:'DM Sans',sans-serif;
      }}
      .ev-pulse {{
        position:absolute; width:62px; height:62px; border-radius:50%;
        background:rgba(232,184,75,.28);
        animation:ev-pulse 2.2s ease-out infinite; pointer-events:none;
      }}
      @keyframes ev-pulse {{
        0%   {{ transform:scale(1);   opacity:.8; }}
        100% {{ transform:scale(1.9); opacity:0;  }}
      }}
      #ev-chat-win {{
        position: fixed !important;
        bottom: 106px !important;
        right: 28px !important;
        width: 376px !important;
        height: 560px !important;
        background: #13171f !important;
        border-radius: 22px !important;
        border: 1px solid #252d3d !important;
        display: flex !important;
        flex-direction: column !important;
        z-index: 2147483646 !important;
        overflow: hidden !important;
        box-shadow: 0 24px 72px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.04) !important;
        transform: scale(.86) translateY(20px) !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transition: transform .35s cubic-bezier(.34,1.5,.64,1), opacity .25s ease !important;
        font-family: 'DM Sans', sans-serif !important;
      }}
      #ev-chat-win.open {{
        transform: scale(1) translateY(0) !important;
        opacity: 1 !important;
        pointer-events: all !important;
      }}
      /* ── Header ── */
      #ev-hdr {{
        background: #0c0f16;
        padding: 14px 16px;
        display: flex;
        align-items: center;
        gap: 11px;
        flex-shrink: 0;
        border-bottom: 1px solid #1e2535;
      }}
      .ev-av {{
        width: 40px; height: 40px; border-radius: 12px;
        background: linear-gradient(135deg,#e8b84b,#f5d080);
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; flex-shrink: 0;
      }}
      .ev-name {{ font-family:'Fraunces',serif; font-size:15px; font-weight:600; color:#f0ece4; line-height:1.2; }}
      .ev-status {{ display:flex; align-items:center; gap:5px; font-size:11px; color:#34c98a; margin-top:2px; font-family:'DM Sans',sans-serif; }}
      .ev-dot {{ width:6px; height:6px; border-radius:50%; background:#34c98a; animation:blink 2s infinite; }}
      @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:.25}} }}
      .ev-min-btn {{
        background:none; border:none; cursor:pointer; color:#5a6480;
        padding:6px; border-radius:8px; margin-left:auto;
        transition:color .2s, background .2s; display:flex;
      }}
      .ev-min-btn:hover {{ color:#f0ece4; background:#1e2535; }}
      /* ── Messages ── */
      #ev-msgs {{
        flex:1; overflow-y:auto; padding:14px 14px 8px;
        display:flex; flex-direction:column; gap:10px;
        scroll-behavior:smooth;
      }}
      #ev-msgs::-webkit-scrollbar {{ width:3px; }}
      #ev-msgs::-webkit-scrollbar-thumb {{ background:#252d3d; border-radius:3px; }}
      .ev-row {{ display:flex; gap:8px; animation:ev-fadein .3s ease; }}
      .ev-row.usr {{ flex-direction:row-reverse; }}
      @keyframes ev-fadein {{ from{{opacity:0;transform:translateY(9px)}} to{{opacity:1;transform:translateY(0)}} }}
      .ev-mav {{
        width:28px; height:28px; border-radius:8px;
        background:linear-gradient(135deg,#e8b84b,#f5d080);
        display:flex; align-items:center; justify-content:center;
        font-size:14px; flex-shrink:0; align-self:flex-end;
      }}
      .ev-mav.u {{
        background:#1e2535; font-size:11px; font-weight:700;
        color:#6b7a99; font-family:'DM Sans',sans-serif;
      }}
      .ev-bub {{
        max-width:80%; padding:10px 13px; font-size:13px;
        line-height:1.65; word-break:break-word;
        font-family:'DM Sans',sans-serif; white-space:pre-wrap;
      }}
      .ev-bub.b {{ background:#1b2130; color:#bdc8de; border-radius:16px 16px 16px 4px; }}
      .ev-bub.u {{ background:#e8b84b; color:#1a1208; border-radius:16px 16px 4px 16px; font-weight:500; }}
      /* Quick replies */
      .ev-qr {{ display:flex; flex-wrap:wrap; gap:5px; margin-top:6px; }}
      .ev-qc {{
        background:transparent; border:1px solid #252d3d;
        color:#6b7a99; border-radius:20px; padding:5px 11px;
        font-size:11px; font-weight:500; cursor:pointer;
        transition:all .2s; font-family:'DM Sans',sans-serif;
      }}
      .ev-qc:hover {{ border-color:#e8b84b; color:#e8b84b; background:rgba(232,184,75,.08); }}
      /* Typing */
      .ev-typing {{
        background:#1b2130; border-radius:16px 16px 16px 4px;
        padding:12px 15px; display:flex; gap:4px; align-items:center;
      }}
      .ev-td {{
        width:6px; height:6px; border-radius:50%; background:#4a5470;
        animation:ev-tba 1.2s infinite;
      }}
      .ev-td:nth-child(2) {{ animation-delay:.2s; }}
      .ev-td:nth-child(3) {{ animation-delay:.4s; }}
      @keyframes ev-tba {{ 0%,60%,100%{{transform:translateY(0)}} 30%{{transform:translateY(-6px)}} }}
      /* Input */
      #ev-inp-area {{
        padding:11px 13px 13px; background:#0c0f16;
        flex-shrink:0; border-top:1px solid #1e2535;
      }}
      .ev-inp-row {{ display:flex; gap:8px; align-items:center; }}
      #ev-input {{
        flex:1; background:#1b2130; border:1px solid #252d3d;
        border-radius:12px; padding:9px 13px;
        font-size:13px; color:#f0ece4; outline:none;
        font-family:'DM Sans',sans-serif; transition:border-color .2s;
        height:40px; resize:none;
      }}
      #ev-input::placeholder {{ color:#3a4260; }}
      #ev-input:focus {{ border-color:#e8b84b; }}
      #ev-send {{
        width:40px; height:40px; border-radius:11px;
        background:#e8b84b; border:none; cursor:pointer;
        display:flex; align-items:center; justify-content:center;
        flex-shrink:0; transition:transform .15s, background .2s; color:#1a1208;
      }}
      #ev-send:hover {{ transform:scale(1.07); background:#f5d080; }}
      #ev-send:disabled {{ background:#1e2535; cursor:not-allowed; transform:none; color:#3a4260; }}
      .ev-pb {{ text-align:center; font-size:10px; color:#2a3248; margin-top:7px; font-family:'DM Sans',sans-serif; }}
    `;
    p.head.appendChild(style);
  }}

  // ── 3. Build the FAB ────────────────────────────────────────────────────────
  const fab = p.createElement('button');
  fab.id = 'ev-chat-fab';
  fab.setAttribute('aria-label', 'Open EduBot chat');
  fab.innerHTML = `
    <div class="ev-pulse"></div>
    <span class="ev-ic ev-ic-chat">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none"
           stroke="#0f1117" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </span>
    <span class="ev-ic ev-ic-close">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
           stroke="#0f1117" stroke-width="2.6" stroke-linecap="round">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </span>
    <div id="ev-badge">1</div>
  `;
  p.body.appendChild(fab);

  // ── 4. Build the Chat Window ─────────────────────────────────────────────
  const win = p.createElement('div');
  win.id = 'ev-chat-win';
  win.setAttribute('role', 'dialog');
  win.setAttribute('aria-label', 'EduBot chat');
  win.innerHTML = `
    <div id="ev-hdr">
      <div class="ev-av">🤖</div>
      <div>
        <div class="ev-name">EduBot AI</div>
        <div class="ev-status"><div class="ev-dot"></div>Online · Powered by Groq</div>
      </div>
      <button class="ev-min-btn" id="ev-close-btn" aria-label="Minimise chat">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
      </button>
    </div>
    <div id="ev-msgs">
      <div class="ev-row" id="ev-welcome">
        <div class="ev-mav">🤖</div>
        <div>
          <div class="ev-bub b">Hi! I'm EduBot 👋 I help you find the right course, explain concepts, and answer career questions. What would you like to know?</div>
          <div class="ev-qr">
            <button class="ev-qc" data-q="Which course is best for beginners?">Best for beginners?</button>
            <button class="ev-qc" data-q="What is your placement rate?">Placement rate?</button>
            <button class="ev-qc" data-q="Tell me about the Generative AI course">Gen AI course</button>
          </div>
        </div>
      </div>
    </div>
    <div id="ev-inp-area">
      <div class="ev-inp-row">
        <input id="ev-input" type="text" placeholder="Ask EduBot anything…" aria-label="Type your message" autocomplete="off"/>
        <button id="ev-send" aria-label="Send message">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
      <div class="ev-pb">Powered by Groq · EduVerse 2026</div>
    </div>
  `;
  p.body.appendChild(win);

  // ── 5. Wire up JS logic ───────────────────────────────────────────────────
  const SYS = `{safe_system}`;
  const KEY = `{safe_key}`;
  let hist = [];
  let busy = false;

  function toggleChat() {{
    win.classList.toggle('open');
    fab.classList.toggle('open');
    const badge = p.getElementById('ev-badge');
    if (win.classList.contains('open')) {{
      if (badge) badge.style.display = 'none';
      setTimeout(() => p.getElementById('ev-input').focus(), 360);
      const msgs = p.getElementById('ev-msgs');
      msgs.scrollTop = msgs.scrollHeight;
    }}
  }}

  fab.addEventListener('click', toggleChat);
  p.getElementById('ev-close-btn').addEventListener('click', toggleChat);

  // Quick replies
  win.querySelectorAll('.ev-qc').forEach(btn => {{
    btn.addEventListener('click', () => sendQ(btn.dataset.q));
  }});

  function sendQ(text) {{
    p.getElementById('ev-input').value = text;
    sendMsg();
  }}

  function addMsg(role, text, chips) {{
    const msgs = p.getElementById('ev-msgs');
    const row  = p.createElement('div');
    row.className = 'ev-row' + (role === 'u' ? ' usr' : '');

    const av   = p.createElement('div');
    av.className = 'ev-mav' + (role === 'u' ? ' u' : '');
    av.textContent = role === 'u' ? 'ME' : '🤖';

    const wrap = p.createElement('div');
    const bub  = p.createElement('div');
    bub.className = 'ev-bub ' + role;
    bub.textContent = text;
    wrap.appendChild(bub);

    if (chips && role === 'b') {{
      const qr = p.createElement('div');
      qr.className = 'ev-qr';
      ['Tell me more', 'Compare courses', 'How to enroll?'].forEach(label => {{
        const btn = p.createElement('button');
        btn.className = 'ev-qc';
        btn.textContent = label;
        btn.addEventListener('click', () => sendQ(label));
        qr.appendChild(btn);
      }});
      wrap.appendChild(qr);
    }}

    if (role === 'u') {{ row.appendChild(wrap); row.appendChild(av); }}
    else              {{ row.appendChild(av);   row.appendChild(wrap); }}

    msgs.appendChild(row);
    msgs.scrollTop = msgs.scrollHeight;
  }}

  function showTyping() {{
    const msgs = p.getElementById('ev-msgs');
    const row  = p.createElement('div');
    row.id = 'ev-typing-row';
    row.className = 'ev-row';
    const av = p.createElement('div');
    av.className = 'ev-mav';
    av.textContent = '🤖';
    const tb = p.createElement('div');
    tb.className = 'ev-typing';
    tb.innerHTML = '<div class="ev-td"></div><div class="ev-td"></div><div class="ev-td"></div>';
    row.appendChild(av);
    row.appendChild(tb);
    msgs.appendChild(row);
    msgs.scrollTop = msgs.scrollHeight;
  }}

async function sendMsg() {{
    if (busy) return;
    const inp = p.getElementById('ev-input');
    const txt = inp.value.trim();
    if (!txt) return;

    inp.value = '';
    p.getElementById('ev-send').disabled = true;
    addMsg('u', txt, false);
    hist.push({{ role: 'user', content: txt }});

    busy = true;
    showTyping();

    try {{
      const messages = [{{ role: 'system', content: SYS }}, ...hist];
      const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + KEY
        }},
        body: JSON.stringify({{
          model: 'llama-3.3-70b-versatile',
          messages,
          temperature: 0.7,
          max_tokens: 300
        }})
      }});
      const data  = await res.json();
      const reply = data?.choices?.[0]?.message?.content
                    ?? 'Sorry, I could not get a response right now. Please try again!';
      hist.push({{ role: 'assistant', content: reply }});

      const tr = p.getElementById('ev-typing-row');
      if (tr) tr.remove();
      addMsg('b', reply, true);

// ── Save to Streamlit backend ──────────────────────────────────────
      console.log('STEP 1: Reply received =', reply);

      const payload = {{ user_message: txt, bot_reply: reply }};
      console.log('STEP 2: Payload built =', JSON.stringify(payload));

      const allTextareas = p.querySelectorAll('textarea');
      console.log('STEP 3: Total textareas found =', allTextareas.length);
     // Replace your textarea-finding logic with this:
let targetTextarea = null;

const allFrames = [p, ...Array.from(p.querySelectorAll("iframe"))
  .map(f => {{
    try {{ return f.contentDocument; }} catch(e) {{ return null; }}
  }})
  .filter(Boolean)
];

for (const doc of allFrames) {{
  const areas = doc.querySelectorAll("textarea");

  areas.forEach(ta => {{
    const label = ta.getAttribute("aria-label");
    if (label === "chat_backend_receiver") {{
      targetTextarea = ta;
    }}
  }});
}}

console.log("STEP 5 Target =", targetTextarea);

if (targetTextarea) {{
  const win = targetTextarea.ownerDocument.defaultView;

  const setter = Object.getOwnPropertyDescriptor(
    win.HTMLTextAreaElement.prototype,
    "value"
  ).set;

  setter.call(targetTextarea, JSON.stringify(payload));

  targetTextarea.focus();

  targetTextarea.dispatchEvent(
    new win.InputEvent("input", {{
      bubbles: true,
      inputType: "insertText",
      data: JSON.stringify(payload)
    }})
  );

  targetTextarea.dispatchEvent(
    new win.Event("change", {{ bubbles: true }})
  );

  targetTextarea.blur();

  console.log("STEP 6: ✅ Sent to Streamlit textarea");
}} else {{
  console.error("❌ chat_backend_receiver textarea not found");
}}
    }} catch (err) {{
      console.error('EduBot error:', err);
      const tr = p.getElementById('ev-typing-row');
      if (tr) tr.remove();
      addMsg('b', 'Oops! Connection issue. Please check your network and try again.', false);
    }}
    busy = false;
    p.getElementById('ev-send').disabled = false;
    inp.focus();
  }}

  // Enter key
  p.getElementById('ev-input').addEventListener('keydown', e => {{
    if (e.key === 'Enter') {{ e.preventDefault(); sendMsg(); }}
  }});

  p.getElementById('ev-send').addEventListener('click', sendMsg);

}})();
</script>
"""

# Render a zero-height iframe that injects the widget into the parent document
components.html(CHATBOT_INJECTOR, height=0, scrolling=False)

# =========================================
# FOOTER
# =========================================

st.markdown("""
<div class="footer">
    <div class="footer-grid">
        <div>
            <div class="footer-logo">Edu<span>Verse</span></div>
            <div class="footer-desc">India's leading AI-powered edtech platform for data, coding and technology careers. Based in Delhi.</div>
        </div>
        <div>
            <div class="footer-col-title">Courses</div>
            <span class="footer-link">Python Programming</span>
            <span class="footer-link">Data Science</span>
            <span class="footer-link">Machine Learning</span>
            <span class="footer-link">Generative AI</span>
            <span class="footer-link">Power BI</span>
        </div>
        <div>
            <div class="footer-col-title">Company</div>
            <span class="footer-link">About Us</span>
            <span class="footer-link">Mentors</span>
            <span class="footer-link">Placement Partners</span>
            <span class="footer-link">Careers</span>
            <span class="footer-link">Blog</span>
        </div>
        <div>
            <div class="footer-col-title">Support</div>
            <span class="footer-link">Help Centre</span>
            <span class="footer-link">Contact Us</span>
            <span class="footer-link">Privacy Policy</span>
            <span class="footer-link">Terms and Conditions</span>
            <span class="footer-link">Refund Policy</span>
        </div>
    </div>
    <div class="footer-bottom">
        <div class="footer-copy">© 2026 EduVerse. All Rights Reserved. Delhi 110030</div>
        <div class="footer-badges">
            <span class="badge">NASSCOM Member</span>
            <span class="badge">Startup India</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
