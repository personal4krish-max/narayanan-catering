import streamlit as st
from modules.database import init_db, create_user, get_all_workers, get_dashboard_stats
from modules.auth import authenticate, set_session, logout

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Narayanan's Catering WMS",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DB Init ──────────────────────────────────────────────────────────────────
init_db()

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

  .main-header {
    background: linear-gradient(135deg, #FF6B35 0%, #f7931a 60%, #FF6B35 100%);
    padding: 28px 40px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 32px;
    box-shadow: 0 8px 32px rgba(255,107,53,0.25);
  }
  .main-header h1 { color: white; font-size: 2.4em; font-weight: 700; margin: 0; letter-spacing: 1px; }
  .main-header p  { color: #ffe0cc; font-size: 1.05em; margin: 6px 0 0; }

  .login-card {
    background: white;
    padding: 36px 40px;
    border-radius: 16px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.10);
    max-width: 460px;
    margin: 0 auto;
  }
  .login-card h2 { color: #1a1a2e; margin-bottom: 20px; font-weight: 700; }

  .stat-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.07);
    border-left: 5px solid #FF6B35;
    margin-bottom: 16px;
  }
  .stat-card .label { color: #888; font-size: 0.85em; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
  .stat-card .value { color: #1a1a2e; font-size: 2.2em; font-weight: 700; margin-top: 4px; }

  .badge-upcoming  { background:#e3f2fd; color:#1565c0; padding:3px 10px; border-radius:20px; font-size:0.8em; font-weight:600; }
  .badge-completed { background:#e8f5e9; color:#2e7d32; padding:3px 10px; border-radius:20px; font-size:0.8em; font-weight:600; }
  .badge-cancelled { background:#fce4ec; color:#c62828; padding:3px 10px; border-radius:20px; font-size:0.8em; font-weight:600; }
  .badge-pending   { background:#fff8e1; color:#f57f17; padding:3px 10px; border-radius:20px; font-size:0.8em; font-weight:600; }
  .badge-approved  { background:#e8f5e9; color:#2e7d32; padding:3px 10px; border-radius:20px; font-size:0.8em; font-weight:600; }
  .badge-rejected  { background:#fce4ec; color:#c62828; padding:3px 10px; border-radius:20px; font-size:0.8em; font-weight:600; }
  .badge-paid      { background:#e8f5e9; color:#2e7d32; padding:3px 10px; border-radius:20px; font-size:0.8em; font-weight:600; }

  .section-title {
    font-size: 1.4em;
    font-weight: 700;
    color: #1a1a2e;
    border-bottom: 3px solid #FF6B35;
    padding-bottom: 8px;
    margin-bottom: 20px;
  }
  .stButton > button {
    background: linear-gradient(135deg, #FF6B35, #f7931a) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
  }
  .stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px); }

  div[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.07);
    border-left: 4px solid #FF6B35;
  }

  .sidebar-info {
    background: linear-gradient(135deg, #FF6B35, #f7931a);
    color: white;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 16px;
    font-weight: 600;
  }
  .footer-note { font-size: 0.78em; color: #aaa; text-align: center; margin-top: 30px; }
</style>
""", unsafe_allow_html=True)

# ─── Session Defaults ─────────────────────────────────────────────────────────
for k, v in [("logged_in", False), ("user_id", None), ("role", None),
             ("username", None), ("worker_id", None), ("worker_name", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍽️ Narayanan's WMS")
    if st.session_state.logged_in:
        role_icon = "👔" if st.session_state.role == "manager" else "👷"
        st.markdown(
            f'<div class="sidebar-info">'
            f'{role_icon} {st.session_state.username}<br>'
            f'<small>{st.session_state.role.capitalize()}</small>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
        st.divider()
        if st.session_state.role == "manager":
            st.markdown("**Manager Pages**")
            st.page_link("pages/01_Manager_Dashboard.py",   label="📊 Dashboard")
            st.page_link("pages/03_Worker_Management.py",   label="👥 Workers")
            st.page_link("pages/04_Event_Management.py",    label="🎉 Events")
            st.page_link("pages/05_Leave_Management.py",    label="📋 Leave Requests")
            st.page_link("pages/06_Attendance.py",          label="✅ Attendance")
            st.page_link("pages/07_Payments.py",            label="💰 Payments")
            st.page_link("pages/08_AI_Allocation.py",       label="🤖 AI Allocation")
        else:
            st.markdown("**Worker Pages**")
            st.page_link("pages/02_Worker_Dashboard.py",    label="🏠 My Dashboard")
            st.page_link("pages/05_Leave_Management.py",    label="📋 My Leaves")
            st.page_link("pages/07_Payments.py",            label="💰 My Payments")
    else:
        st.info("Please log in to access the system.")

# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🍽️ Narayanan's Catering</h1>
  <p>Workforce Management System — Smart. Efficient. Transparent.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.logged_in:
    # ── Welcome screen after login ─────────────────────────────────────────
    stats = get_dashboard_stats()
    name = st.session_state.worker_name or st.session_state.username
    st.markdown(f"### Welcome back, **{name}**! 👋")

    if st.session_state.role == "manager":
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👷 Total Workers",   stats["total_workers"])
        col2.metric("✅ Available",        stats["available_workers"])
        col3.metric("🎉 Total Events",    stats["total_events"])
        col4.metric("📅 Upcoming",        stats["upcoming_events"])

        col5, col6, col7 = st.columns(3)
        col5.metric("📋 Pending Leaves",  stats["pending_leaves"])
        col6.metric("💸 Pending Payments", stats["pending_payments"])
        col7.metric("💰 Total Paid",      f"₹{stats['total_paid']:,.0f}")

        st.info("👈 Use the sidebar navigation to manage workers, events, attendance, and payments.")
    else:
        st.info("👈 Use the sidebar to view your assigned events, apply for leave, and check payments.")

else:
    # ── Login / Register Tabs ─────────────────────────────────────────────
    tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register as Worker"])

    with tab_login:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("#### Sign In")
        with st.form("login_form"):
            identifier = st.text_input("📱 Phone Number / Username",
                                       placeholder="Enter phone or username")
            password   = st.text_input("🔒 Password", type="password",
                                       placeholder="Enter password")
            submitted  = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if not identifier or not password:
                st.error("Please fill in all fields.")
            else:
                user, err = authenticate(identifier, password)
                if err:
                    st.error(f"❌ {err}")
                else:
                    set_session(user)
                    st.success("✅ Login successful!")
                    st.rerun()

        st.markdown("---")
        st.markdown(
            "**Demo Credentials:**\n\n"
            "- Manager → `admin` / `admin123`\n"
            "- Worker  → phone number / last 4 digits + `@wms`  e.g. `0001@wms`"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_register:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("#### Worker Self-Registration")
        with st.form("register_form"):
            r_name   = st.text_input("Full Name")
            r_phone  = st.text_input("Phone Number (used as username & login ID)")
            r_skill  = st.selectbox("Skill", ["Cook", "Server", "Helper", "Supervisor"])
            r_exp    = st.number_input("Years of Experience", 0, 40, 0)
            r_addr   = st.text_area("Address (optional)")
            r_emg    = st.text_input("Emergency Contact (optional)")
            r_pass   = st.text_input("Create Password", type="password")
            r_pass2  = st.text_input("Confirm Password", type="password")
            reg_btn  = st.form_submit_button("Register", use_container_width=True)

        if reg_btn:
            if not all([r_name, r_phone, r_pass]):
                st.error("Name, phone, and password are required.")
            elif r_pass != r_pass2:
                st.error("Passwords do not match.")
            elif len(r_phone) < 10:
                st.error("Enter a valid phone number.")
            else:
                from modules.database import create_worker
                uid, err = create_user(r_phone, r_pass, "worker", r_phone)
                if err:
                    st.error(f"❌ Registration failed: {err}")
                else:
                    ok, err2 = create_worker(uid, r_name, r_phone, r_skill,
                                             r_exp, 500.0, r_addr, r_emg)
                    if ok:
                        st.success("✅ Registered successfully! You can now log in.")
                    else:
                        st.error(f"❌ Worker profile error: {err2}")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer-note">© 2025 Narayanan\'s Catering Workforce Management System · Built with ❤️ using Streamlit</div>', unsafe_allow_html=True)
