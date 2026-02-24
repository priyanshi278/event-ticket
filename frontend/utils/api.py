import requests
import streamlit as st

BASE_URL = "https://event-ticket-rets.onrender.com"

def get_auth_headers():
    if "token" in st.session_state:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def safe_json(response):
    """Safely decode JSON response, handling non-JSON content gracefully."""
    try:
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()
        return {"detail": f"Backend returned non-JSON response (Status: {response.status_code})"}
    except Exception:
        return {"detail": "Failed to decode JSON from backend"}

# AUTH
def login(email, password):
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        data = safe_json(response)
        if response.status_code == 200:
            st.session_state.token = data.get("access_token")
            st.session_state.user_role = data.get("role")
            st.session_state.user_email = email
            return True, "Login successful"
        return False, data.get("detail", "Login failed")
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

def signup(name, email, password, role):
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json={
            "name": name,
            "email": email,
            "password": password,
            "role": role
        })
        data = safe_json(response)
        if response.status_code == 200:
            return True, "Signup successful! Please login."
        return False, data.get("detail", "Signup failed")
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

# CUSTOMER
def get_events():
    try:
        response = requests.get(f"{BASE_URL}/customer/events")
        data = safe_json(response)
        if response.status_code == 200:
            return data
        return []
    except:
        return []

def get_event_seats(event_id):
    try:
        response = requests.get(f"{BASE_URL}/customer/events/{event_id}/seats")
        data = safe_json(response)
        if response.status_code == 200:
            return data
        return []
    except:
        return []

def place_order(event_id, seat_ids, payment_mode="Credit Card", offer_id=None):
    try:
        headers = get_auth_headers()
        response = requests.post(f"{BASE_URL}/customer/orders", json={
            "event_id": event_id,
            "seat_ids": seat_ids,
            "payment_mode": payment_mode,
            "offer_id": offer_id
        }, headers=headers)
        data = safe_json(response)
        if response.status_code == 200:
            return True, data
        return False, data.get("detail", "Order failed")
    except Exception as e:
        return False, str(e)

def request_refund(order_id, reason):
    try:
        headers = get_auth_headers()
        response = requests.post(f"{BASE_URL}/customer/refund-request", json={
            "order_id": order_id,
            "reason": reason
        }, headers=headers)
        data = safe_json(response)
        return response.status_code == 200, data
    except:
        return False, "Connection error"

def raise_support_case(description):
    try:
        headers = get_auth_headers()
        response = requests.post(f"{BASE_URL}/customer/support-cases", json={
            "description": description
        }, headers=headers)
        data = safe_json(response)
        return response.status_code == 200, data
    except:
        return False, "Connection error"

# ENTRY MANAGER
def validate_ticket(ticket_code):
    try:
        headers = get_auth_headers()
        response = requests.post(f"{BASE_URL}/entry/validate-ticket", json={
            "ticket_code": ticket_code
        }, headers=headers)
        data = safe_json(response)
        if response.status_code == 200:
            return data
        return {"is_valid": False, "message": data.get("detail", "Validation failed")}
    except:
        return {"is_valid": False, "message": "Connection error"}

# SUPPORT EXECUTIVE
def get_support_cases():
    try:
        headers = get_auth_headers()
        response = requests.get(f"{BASE_URL}/support/cases", headers=headers)
        return safe_json(response) if response.status_code == 200 else []
    except:
        return []

def update_support_case(case_id, status, resolution_note):
    try:
        headers = get_auth_headers()
        response = requests.patch(f"{BASE_URL}/support/cases/{case_id}", json={
            "status": status,
            "resolution_note": resolution_note
        }, headers=headers)
        return response.status_code == 200
    except:
        return False

def get_refund_requests():
    try:
        headers = get_auth_headers()
        response = requests.get(f"{BASE_URL}/support/refunds", headers=headers)
        return safe_json(response) if response.status_code == 200 else []
    except:
        return []

def handle_refund_request(refund_id, status):
    try:
        headers = get_auth_headers()
        response = requests.patch(f"{BASE_URL}/support/refunds/{refund_id}", json={
            "status": status
        }, headers=headers)
        return response.status_code == 200
    except:
        return False

# ADMIN & OFFERS
def get_offers():
    try:
        response = requests.get(f"{BASE_URL}/offers/")
        data = safe_json(response)
        if response.status_code == 200:
            return data
        return []
    except:
        return []

def create_offer(data):
    try:
        headers = get_auth_headers()
        response = requests.post(f"{BASE_URL}/offers/", json=data, headers=headers)
        return response.status_code == 200
    except:
        return False
