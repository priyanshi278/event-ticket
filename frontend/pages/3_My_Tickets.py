import streamlit as st
from utils.api import get_auth_headers

if "token" not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()

st.title("🎫 My Tickets")

# Note: In a production app, the backend should have a /customer/orders endpoint.
# Since we are using the routers provided by the backend without modification, 
# and the backend only had placeholder support for "view booking summary" in organizer router,
# we show the current session's booking status.

if "last_order" in st.session_state:
    order = st.session_state.last_order
    st.success(f"Latest Order ID: {order['id']}")
    st.markdown("### Ticket Details")
    st.info(f"Amount Paid: ₹{order['final_amount']}")
    st.write(f"Payment Mode: {order['payment_mode']}")
    st.write("Status: Confirmed")
    
    st.divider()
    if st.button("Request Refund"):
        st.session_state.refund_order_id = order['id']
        st.switch_page("pages/5_Support.py")

else:
    st.info("You haven't booked any tickets yet in this session.")
    if st.button("Explore Events"):
        st.switch_page("Home.py")
