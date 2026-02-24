import streamlit as st
from utils.api import get_event_seats

if "token" not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()

if "selected_event" not in st.session_state:
    st.info("Please select an event from the home page first.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

event = st.session_state.selected_event
st.title(f"📍 {event['name']}")
st.markdown(f"**Category:** {event['category']} | **Date:** {event['event_date']}")
st.markdown(f"**Price per Seat:** ₹{event['ticket_price']}")

st.divider()

st.subheader("Select Your Seats")
seats = get_event_seats(event["id"])

if not seats:
    st.error("No seats found for this event. Please contact support.")
else:
    # Group seats into rows of 5 for display
    cols = st.columns(5)
    selected_seats = st.session_state.get("cart", [])
    
    for i, seat in enumerate(seats):
        with cols[i % 5]:
            is_available = seat["status"] == "Available"
            label = f"{seat['seat_number']}\n(Booked)" if not is_available else seat["seat_number"]
            
            # Simple button selection logic
            if is_available:
                if st.button(label, key=f"seat_{seat['id']}", type="primary" if seat["id"] in selected_seats else "secondary"):
                    if seat["id"] in selected_seats:
                        selected_seats.remove(seat["id"])
                    else:
                        if len(selected_seats) < event["max_tickets_per_user"]:
                            selected_seats.append(seat["id"])
                        else:
                            st.warning(f"Maximum {event['max_tickets_per_user']} tickets allowed!")
                    st.session_state.cart = selected_seats
                    st.rerun()
            else:
                st.button(label, key=f"seat_{seat['id']}", disabled=True)

st.sidebar.subheader("Cart")
if "cart" in st.session_state and st.session_state.cart:
    st.sidebar.write(f"Selected Seats: {len(st.session_state.cart)}")
    if st.sidebar.button("Proceed to Checkout"):
        st.switch_page("pages/2_Checkout.py")
else:
    st.sidebar.info("No seats selected.")

if st.button("Back to Events"):
    st.switch_page("Home.py")
