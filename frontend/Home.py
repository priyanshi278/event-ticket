import streamlit as st
from utils.api import login, signup, get_events

st.set_page_config(page_title="EventTik - Ticket Booking", layout="wide")

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .welcome-card {
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

if "token" not in st.session_state:
    st.title("🎟️ EventTik")
    st.subheader("Your one-stop destination for events and tickets.")

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.markdown("### Welcome Back")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                success, msg = login(email, password)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        
        with tab2:
            st.markdown("### Create New Account")
            name = st.text_input("Full Name")
            new_email = st.text_input("Email", key="signup_email")
            new_pass = st.text_input("Password", type="password", key="signup_pass")
            role = st.selectbox("I am a...", ["customer", "organizer", "entry_manager", "support"])
            if st.button("Sign Up"):
                success, msg = signup(name, new_email, new_pass, role)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

else:
    # Authenticated State
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.user_email}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role.capitalize()}")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.title("🎭 Upcoming Events")
    events = get_events()
    
    if not events:
        st.info("No upcoming events at the moment.")
    else:
        for event in events:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {event['name']}")
                    st.caption(f"{event['category']} | 📅 {event['event_date']}")
                with col2:
                    st.markdown(f"**₹{event['ticket_price']}**")
                    if st.button("Buy Tickets", key=f"btn_{event['id']}"):
                        st.session_state.selected_event = event
                        st.switch_page("pages/1_Event_Details.py")
                st.divider()
