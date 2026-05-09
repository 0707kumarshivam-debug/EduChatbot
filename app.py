import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime
import re

# ============================================
# CONFIGURATION
# ============================================

# Initialize OpenAI client (replace with your actual key)
client = OpenAI(api_key="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")

st.set_page_config(
    page_title="EduBot - Education Assistant",
    page_icon="🎓",
    layout="wide"
)

# ============================================
# BASIC CSS
# ============================================

st.markdown("""
<style>
    .user-msg {
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 5px 0;
        text-align: right;
        max-width: 70%;
        margin-left: auto;
    }

    .bot-msg {
        background-color: #e9ecef;
        color: black;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 5px 0;
        max-width: 70%;
        margin-right: auto;
    }

    .course-card {
        border: 1px solid #ddd;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        background-color: #f9f9f9;
    }

    .stButton button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
    }

    .stButton button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# DATA LOADING
# ============================================

@st.cache_data
def load_courses():
    """Load course data"""
    try:
        df = pd.read_csv("courses.csv")
    except:
        # Sample data if CSV not found
        df = pd.DataFrame({
            'course': ['Python Programming', 'Data Science', 'Web Development',
                       'Machine Learning', 'Digital Marketing'],
            'fees': [29990, 49990, 39990, 59990, 24990],
            'duration': ['3 months', '8 months', '6 months', '6 months', '2 months'],
            'level': ['Beginner', 'Intermediate', 'Beginner', 'Advanced', 'Beginner']
        })
    return df


df = load_courses()


# ============================================
# HELPER FUNCTIONS
# ============================================

def search_course(query):
    """Search for course information"""
    query_lower = query.lower()

    for _, row in df.iterrows():
        if row['course'].lower() in query_lower:
            return f"""
            📚 **{row['course']}**
            💰 Fees: ₹{row['fees']:,}
            ⏱️ Duration: {row['duration']}
            📊 Level: {row['level']}
            """
    return None


def get_all_courses():
    """Get all courses as HTML"""
    html = "<div><h4>📚 All Available Courses:</h4>"
    for _, row in df.iterrows():
        html += f"""
        <div class='course-card'>
            <b>{row['course']}</b><br>
            💰 ₹{row['fees']:,} | ⏱️ {row['duration']} | 📊 {row['level']}
        </div>
        """
    html += "</div>"
    return html


def get_personalized_recommendation(query):
    """Simple personalized recommendation"""
    query_lower = query.lower()

    if 'beginner' in query_lower or 'start' in query_lower:
        beginner_courses = df[df['level'] == 'Beginner']
        if not beginner_courses.empty:
            course = beginner_courses.iloc[0]
            return f"🎯 **Recommendation:** For beginners, try **{course['course']}**! (₹{course['fees']:,}, {course['duration']})"

    elif 'advanced' in query_lower:
        advanced_courses = df[df['level'] == 'Advanced']
        if not advanced_courses.empty:
            course = advanced_courses.iloc[0]
            return f"🚀 **Advanced course:** **{course['course']}** is perfect for you! (₹{course['fees']:,})"

    return None


# ============================================
# SESSION STATE INITIALIZATION
# ============================================

# Initialize chat history
if "messages" not in st.session_state:
    welcome_msg = "👋 Hello! I'm EduBot! Ask me about courses, fees, enrollment, or technical support!"
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

# Track last clicked button
if "last_button" not in st.session_state:
    st.session_state.last_button = None

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## 🎓 EduBot")
    st.markdown("---")

    st.markdown("### 📚 Courses")
    for _, row in df.iterrows():
        st.markdown(f"• **{row['course']}** - ₹{row['fees']:,}")

    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    Ask me about:
    • Course details
    • Fees and duration
    • Enrollment process
    • Technical support
    """)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "👋 Chat cleared! How can I help you?"}]
        st.session_state.last_button = None
        st.rerun()

# ============================================
# MAIN CHAT INTERFACE
# ============================================

st.markdown("# 🎓 EduBot - AI Education Assistant")
st.caption("Ask me anything about courses, fees, enrollment, or technical support")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>👤 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# ============================================
# QUICK QUESTIONS (IMPROVED - Auto clear previous)
# ============================================

st.markdown("### Quick Questions")

# Create 4 columns for buttons
col1, col2, col3, col4 = st.columns(4)

# Button click handlers with session state tracking
with col1:
    if st.button("📚 All Courses", use_container_width=True, key="btn_all"):
        st.session_state.last_button = "all_courses"
        # Clear previous messages except welcome
        st.session_state.messages = [st.session_state.messages[0]]  # Keep only welcome message
        # Add new user question
        st.session_state.messages.append({"role": "user", "content": "Show me all courses"})
        # Add bot response
        response = get_all_courses()
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col2:
    if st.button("💰 Course Fees", use_container_width=True, key="btn_fees"):
        st.session_state.last_button = "fees"
        # Clear previous messages except welcome
        st.session_state.messages = [st.session_state.messages[0]]
        # Add new user question
        st.session_state.messages.append({"role": "user", "content": "What are the course fees?"})
        # Generate response
        response = "💰 **Course Fees:**\n\n"
        for _, row in df.iterrows():
            response += f"• **{row['course']}**: ₹{row['fees']:,}\n"
        response += "\n💡 Want details about a specific course? Just ask!"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col3:
    if st.button("✅ Enrollment", use_container_width=True, key="btn_enroll"):
        st.session_state.last_button = "enroll"
        # Clear previous messages except welcome
        st.session_state.messages = [st.session_state.messages[0]]
        # Add new user question
        st.session_state.messages.append({"role": "user", "content": "How to enroll?"})
        # Generate response
        response = """
        ✅ **Enrollment Process:**

        1️⃣ Select your desired course
        2️⃣ Click "Enroll Now" button
        3️⃣ Fill in your details
        4️⃣ Complete payment
        5️⃣ Start learning instantly!

        💳 **Payment Options:** Credit Card, Debit Card, UPI, NetBanking
        """
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col4:
    if st.button("🎯 Recommendations", use_container_width=True, key="btn_rec"):
        st.session_state.last_button = "rec"
        # Clear previous messages except welcome
        st.session_state.messages = [st.session_state.messages[0]]
        # Add new user question
        st.session_state.messages.append({"role": "user", "content": "Recommend a beginner course"})
        # Generate response
        response = get_personalized_recommendation("beginner course")
        if not response:
            response = "🎯 **Popular Courses:**\n\n" + "\n".join(
                [f"• {row['course']} (₹{row['fees']:,})" for _, row in df.head(3).iterrows()])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# ============================================
# CHAT INPUT
# ============================================

# Chat input for custom questions
chat_input = st.chat_input("Type your question here...")

if chat_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": chat_input})

    # Generate bot response
    response = None

    # Check for course search
    if "show me all courses" in chat_input.lower() or "list courses" in chat_input.lower():
        response = get_all_courses()
    elif "course fees" in chat_input.lower() or "fees of" in chat_input.lower():
        response = "💰 **Course Fees:**\n\n"
        for _, row in df.iterrows():
            response += f"• **{row['course']}**: ₹{row['fees']:,}\n"
        response += "\n💡 Want details about a specific course? Just ask!"
    elif "how to enroll" in chat_input.lower() or "enrollment" in chat_input.lower():
        response = """
        ✅ **Enrollment Process:**

        1️⃣ Select your desired course
        2️⃣ Click "Enroll Now" button
        3️⃣ Fill in your details
        4️⃣ Complete payment
        5️⃣ Start learning instantly!

        💳 **Payment Options:** Credit Card, Debit Card, UPI, NetBanking
        """
    else:
        # Search for specific course
        course_info = search_course(chat_input)
        if course_info:
            response = course_info + "\n\n✨ Interested? Type 'enroll' to get started!"
        else:
            # Use OpenAI for other queries
            try:
                system_prompt = """You are EduBot, an AI assistant for an online education platform. 
                Answer questions about courses, fees, enrollment, and technical support only. 
                Keep answers short and helpful."""

                api_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chat_input}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                response = api_response.choices[0].message.content
            except Exception as e:
                response = f"⚠️ Sorry, I'm having trouble. Please try again.\n\nTip: Try 'Python course details'"

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ============================================
# FOOTER
# ============================================

st.markdown("---")


st.caption("💡 **Tip:** Be specific! Try 'Python course fees?' or 'How do I enroll in Data Science?'")