import streamlit as st
from utils.api import get_offers, place_order

if "token" not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()

if "selected_event" not in st.session_state or "cart" not in st.session_state or not st.session_state.cart:
    st.info("Your cart is empty.")
    if st.button("Browse Events"):
        st.switch_page("Home.py")
    st.stop()

event = st.session_state.selected_event
cart = st.session_state.cart

st.title("🛒 Checkout")
st.markdown(f"### {event['name']}")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Summary")
    st.write(f"Number of Tickets: {len(cart)}")
    st.write(f"Price per Ticket: ₹{event['ticket_price']}")
    total = len(cart) * float(event['ticket_price'])
    st.markdown(f"**Total Amount: ₹{total}**")

with col2:
    st.subheader("Apply Offer")
    offers = get_offers()
    selected_offer = st.selectbox("Select Discount Code", ["None"] + [o["code"] for o in offers])
    
    offer_id = None
    if selected_offer != "None":
        offer = next(o for o in offers if o["code"] == selected_offer)
        offer_id = offer["id"]
        st.success(f"{offer['discount_percent']}% discount applied!")

st.divider()

st.subheader("Payment Method")
payment_mode = st.radio("Choose Payment Mode", ["Credit Card", "UPI", "Net Banking", "Cash"])

if st.button("Pay & Book Ticket"):
    with st.spinner("Processing payment..."):
        success, result = place_order(event["id"], cart, payment_mode, offer_id)
        if success:
            st.success("Booking confirmed! Your tickets are generated.")
            st.session_state.last_order = result
            # Clear cart
            del st.session_state.cart
            st.button("View My Ticket", on_click=lambda: st.switch_page("pages/3_My_Tickets.py"))
        else:
            st.error(f"Error: {result}")

if st.button("Change Seats"):
    st.switch_page("pages/1_Event_Details.py")
