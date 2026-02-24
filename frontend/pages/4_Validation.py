import streamlit as st
from utils.api import validate_ticket

if "token" not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()

if st.session_state.user_role not in ["entry_manager", "admin"]:
    st.error("Access Denied. Only Entry Managers can access this page.")
    st.stop()

st.title("🎫 Ticket Validation")
st.markdown("Enter the ticket code below to validate entry.")

ticket_code = st.text_input("Ticket Code (e.g., TC-1-1)")

if st.button("Validate Admission"):
    if ticket_code:
        result = validate_ticket(ticket_code)
        if result["is_valid"]:
            st.balloons()
            st.success("✅ VALID TICKET")
            info = result.get("ticket_info", {})
            st.markdown(f"**Event:** {info.get('event')}")
            st.markdown(f"**Seat:** {info.get('seat')}")
            st.markdown(f"**Code:** {info.get('ticket_code')}")
        else:
            st.error(f"❌ INVALID: {result['message']}")
    else:
        st.warning("Please enter a code.")
