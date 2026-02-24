import streamlit as st
from utils.api import (
    request_refund, 
    raise_support_case, 
    get_support_cases, 
    update_support_case, 
    get_refund_requests, 
    handle_refund_request
)

if "token" not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()

st.title("🎧 Support & Refunds")

tab1, tab2 = st.tabs(["Raise Issue/Refund", "Support Dashboard"])

with tab1:
    st.subheader("New Support Case")
    desc = st.text_area("Describe your issue or refund reason")
    
    order_id = st.number_input("Order ID (for refunds)", value=st.session_state.get("refund_order_id", 0), step=1)
    
    if st.button("Submit Request"):
        if desc:
            if order_id > 0:
                success, result = request_refund(order_id, desc)
            else:
                success, result = raise_support_case(desc)
            
            if success:
                st.success("Request submitted successfully!")
            else:
                st.error(f"Error: {result}")
        else:
            st.warning("Please provide a description.")

with tab2:
    if st.session_state.user_role not in ["support", "admin"]:
        st.info("The dashboard is only available for Support Executives.")
    else:
        st.subheader("Active Cases")
        cases = get_support_cases()
        refunds = get_refund_requests()
        
        if not refunds and not cases:
            st.info("No active cases found.")
        
        if refunds:
            st.markdown("### Refund Requests")
            for r in refunds:
                with st.expander(f"Refund #{r['id']} - Status: {r['status']}"):
                    st.write(f"Order ID: {r['order_id']}")
                    st.write(f"Reason: {r['reason']}")
                    if r['status'] == "Pending":
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Approve", key=f"app_{r['id']}"):
                                if handle_refund_request(r['id'], "Approved"):
                                    st.success("Approved!")
                                    st.rerun()
                        with col2:
                            if st.button("Reject", key=f"rej_{r['id']}"):
                                if handle_refund_request(r['id'], "Rejected"):
                                    st.error("Rejected!")
                                    st.rerun()
        
        if cases:
            st.markdown("### General Support Cases")
            for c in cases:
                with st.expander(f"Case #{c['id']} - {c['status']}"):
                    st.write(c['description'])
                    note = st.text_input("Resolution Note", value=c['resolution_note'], key=f"note_{c['id']}")
                    status = st.selectbox("Update Status", ["Open", "In Progress", "Resolved", "Closed"], index=["Open", "In Progress", "Resolved", "Closed"].index(c['status']) if c['status'] in ["Open", "In Progress", "Resolved", "Closed"] else 0, key=f"stat_{c['id']}")
                    if st.button("Update Case", key=f"upd_{c['id']}"):
                        if update_support_case(c['id'], status, note):
                            st.success("Updated!")
                            st.rerun()
