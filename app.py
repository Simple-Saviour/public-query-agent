import os
os.environ["TIKTOKEN_CACHE_DIR"] = os.path.expanduser("~/.tiktoken_cache")


import streamlit as st
import pandas as pd
import time
from langchain_core.messages import HumanMessage
from core.graph import app_graph
from tools.analytics_tool import analytics_log
from tools.email_tool import send_email_notification
from utils.helpers import check_login
# NEW IMPORT for uploading files
from utils.ingest import ingest_pdf_file 

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="CitizenAssist AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS STYLING
# ==========================================
st.markdown("""
    <style>
    .stChatMessage {
        background-color: #f9f9f9;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
    }
    h1 { color: #2c3e50; }
    [data-testid="stSidebar"] { background-color: #f4f6f9; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ==========================================
# 4. SIDEBAR: LOGIN
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2344/2344684.png", width=70)
    st.title("Civic Portal")
    st.markdown("---")
    
    if not st.session_state.user_role:
        st.subheader("🔐 Secure Login")
        with st.form("login_form"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            
            if submitted:
                role = check_login(user, pwd)
                if role:
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    else:
        st.success(f"👤 **{st.session_state.user_role.upper()}**")
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.user_role = None
            st.rerun()

# ==========================================
# 5. ADMIN VIEW (Uploads & Analytics)
# ==========================================
if st.session_state.user_role == "admin":
    st.title("🛡️ Admin Administration")
    
    # Tabs for different Admin functions
    tab1, tab2 = st.tabs(["📂 Upload Policy Docs", "📊 Analytics Dashboard"])
    
    # --- TAB 1: UPLOAD KNOWLEDGE BASE ---
    with tab1:
        st.subheader("Update Knowledge Base")
        st.markdown("Upload new government policy PDFs here. The AI will ingest them immediately.")
        
        # 1. File Uploader
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        # 2. Category Selector
        category = st.selectbox(
            "Select Category",
            ["Tax", "Permits", "Social Services", "General"]
        )
        
        # 3. Upload Logic
        if st.button("🚀 Process & Ingest", type="primary"):
            if uploaded_file and category:
                with st.spinner("Reading PDF, splitting text, and updating Vector Database..."):
                    # Save temp file
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Call Ingest Function
                    success, msg = ingest_pdf_file(temp_path, category)
                    
                    # Cleanup
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    if success:
                        st.success(f"Done! {msg}")
                        st.balloons()
                    else:
                        st.error(f"Failed: {msg}")
            else:
                st.warning("Please upload a file and select a category.")

    # --- TAB 2: ANALYTICS ---
    with tab2:
        st.subheader("Live System Stats")
        df = pd.DataFrame(list(analytics_log.items()), columns=["Category", "Count"])
        st.bar_chart(df.set_index("Category"), color="#2E86C1")
        st.metric("Total Queries Processed", sum(analytics_log.values()))

# ==========================================
# 6. CITIZEN VIEW (Chatbot Only)
# ==========================================
elif st.session_state.user_role == "citizen":
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("🏛️ Public Services Assistant")
        st.markdown("Ask about **Taxes**, **Permits**, or **Social Schemes**.")
    with col2:
        if st.button("🧹 Clear"):
            st.session_state.messages = []
            st.rerun()

    st.divider()

    # Chat History
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            status = st.status("🧠 **System Processing...**", expanded=True)
            try:
                # Run AI Graph
                status.write("🕵️ **Supervisor:** Routing query...")
                time.sleep(0.5) 
                
                inputs = {"messages": [HumanMessage(content=prompt)]}
                result = app_graph.invoke(inputs)
                final_res = result.get("final_response", "Error generating response.")
                
                # Visuals
                status.write("🔍 **Specialist Agent:** Searching uploaded docs...")
                time.sleep(0.5)
                status.write("✅ **QA Agent:** Verifying...")
                status.update(label="Response Ready", state="complete", expanded=False)
                
                st.markdown(final_res)
                st.session_state.messages.append({"role": "assistant", "content": final_res})
                
                # Actions
                st.markdown("---")
                c1, c2 = st.columns([1, 4])
                with c1:
                    if st.button("📩 Email Me"):
                        st.toast("Email Sent!", icon="📧")
                        
            except Exception as e:
                status.update(label="Error", state="error")
                st.error(str(e))

# ==========================================
# 7. GUEST VIEW
# ==========================================
else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👋 Please **Log In** via the sidebar.")
    st.markdown("""
    **Credentials:**
    - Admin: `admin` / `123` (Upload Docs)
    - Citizen: `citizen` / `123` (Chat)
    """)