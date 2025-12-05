# styles.py - All CSS styling for the TalentScout AI application

def get_app_styles():
    """Returns the complete CSS styling for the Streamlit app"""
    return """
<style>
    /* Animated gradient background - works reliably in Streamlit */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.1); }
    }
    
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Floating orbs for depth */
    .floating-orbs {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.5;
    }
    
    .orb-1 {
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.8) 0%, transparent 70%);
        top: -100px;
        right: -100px;
        animation: float 8s ease-in-out infinite;
    }
    
    .orb-2 {
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(118, 75, 162, 0.8) 0%, transparent 70%);
        bottom: -50px;
        left: -50px;
        animation: float 10s ease-in-out infinite reverse;
    }
    
    .orb-3 {
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(72, 187, 120, 0.6) 0%, transparent 70%);
        top: 40%;
        left: 30%;
        animation: pulse 6s ease-in-out infinite;
    }
    
    .orb-4 {
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(236, 72, 153, 0.5) 0%, transparent 70%);
        top: 20%;
        right: 20%;
        animation: float 12s ease-in-out infinite;
    }
    
    /* Ensure content is above orbs */
    .main .block-container {
        position: relative;
        z-index: 1;
    }
    
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.98) 0%, rgba(48, 43, 99, 0.95) 100%) !important;
        backdrop-filter: blur(20px);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 50%, rgba(236, 72, 153, 0.8) 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    /* Message bubbles with glass effect */
    .assistant-message {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        border-radius: 20px 20px 20px 4px;
        margin: 1rem 0;
        max-width: 85%;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        animation: slideInLeft 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        line-height: 1.6;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(55, 65, 81, 0.9) 0%, rgba(75, 85, 99, 0.9) 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        border-radius: 20px 20px 4px 20px;
        margin: 1rem 0;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: slideInRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        line-height: 1.6;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px) scale(0.95); }
        to { opacity: 1; transform: translateX(0) scale(1); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px) scale(0.95); }
        to { opacity: 1; transform: translateX(0) scale(1); }
    }
    
    /* Sidebar styling */
    .sidebar-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .sidebar-card:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.05) 100%);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .sidebar-card h3 {
        color: #a78bfa;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.25rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    
    .status-active {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.2) 0%, rgba(56, 178, 172, 0.2) 100%);
        color: #68d391;
        border: 1px solid rgba(72, 187, 120, 0.4);
        box-shadow: 0 0 20px rgba(72, 187, 120, 0.2);
    }
    
    .status-ended {
        background: linear-gradient(135deg, rgba(245, 101, 101, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
        color: #fc8181;
        border: 1px solid rgba(245, 101, 101, 0.4);
        box-shadow: 0 0 20px rgba(245, 101, 101, 0.2);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        border: 2px solid rgba(255,255,255,0.15) !important;
        border-radius: 14px !important;
        color: white !important;
        padding: 0.9rem 1.25rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.25), 0 8px 25px rgba(102, 126, 234, 0.2) !important;
        background: rgba(255,255,255,0.12) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.4) !important;
    }
    
    /* Chat input specific */
    [data-testid="stChatInput"] {
        background: rgba(255,255,255,0.05) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ec4899 100%) !important;
        background-size: 200% 200% !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5) !important;
        background-position: 100% 50% !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        border: 2px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stMetricValue"] {
        color: #a78bfa !important;
    }
    
    /* Progress items */
    .progress-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0;
        transition: all 0.2s ease;
    }
    
    .progress-item:hover {
        transform: translateX(5px);
    }
    
    /* Divider styling */
    hr {
        border-color: rgba(255,255,255,0.1) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Hide Streamlit branding but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Style the sidebar collapse button to be always visible */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        color: white !important;
        background: rgba(102, 126, 234, 0.8) !important;
        border-radius: 8px !important;
        margin: 0.5rem !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(118, 75, 162, 0.9) !important;
    }
</style>

<!-- Floating orbs for animated background effect -->
<div class="floating-orbs">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
</div>
"""
