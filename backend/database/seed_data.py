import os
import traceback
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.user import User
from models.venue import Venue
from models.event import Event
from models.seat import Seat
from models.offer import Offer
from models.order import Order
from models.ticket import Ticket
from models.refund_request import RefundRequest
from models.support_case import SupportCase
from models.entry_log import EntryLog

def seed_data():
    db: Session = SessionLocal()
    try:
        # 1. Users
        print("Seeding Users...")
        users = [
            User(name="Admin User", email="admin@example.com", password="password123", role="admin"),
            User(name="John Doe", email="john@example.com", password="password123", role="user"),
            User(name="Jane Smith", email="jane@example.com", password="password123", role="user"),
            User(name="Alice Brown", email="alice@example.com", password="password123", role="user"),
            User(name="Bob Wilson", email="bob@example.com", password="password123", role="user"),
            User(name="Charlie Davis", email="charlie@example.com", password="password123", role="user"),
            User(name="Eve Miller", email="eve@example.com", password="password123", role="user"),
        ]
        db.add_all(users)
        db.commit()

        # 2. Venues
        print("Seeding Venues...")
        venues = [
            Venue(name="Madison Square Garden", city="New York", address="4 Pennsylvania Plaza", total_capacity=20000),
            Venue(name="Wembley Stadium", city="London", address="Wembley, London HA9 0WS", total_capacity=90000),
            Venue(name="O2 Arena", city="London", address="Peninsula Square, London SE10 0DX", total_capacity=20000),
            Venue(name="Staples Center", city="Los Angeles", address="1111 S Figueroa St", total_capacity=19000),
            Venue(name="Accor Stadium", city="Sydney", address="Edwin Flack Ave, Sydney Olympic Park", total_capacity=83500),
            Venue(name="Allianz Arena", city="Munich", address="Werner-Heisenberg-Allee 25", total_capacity=75000),
            Venue(name="Tokyo Dome", city="Tokyo", address="1-3-61 Koraku, Bunkyo City", total_capacity=55000),
        ]
        db.add_all(venues)
        db.commit()

        # 3. Offers
        print("Seeding Offers...")
        offers = [
            Offer(code="WELCOME10", discount_percent=Decimal("10.0"), max_discount_amount=Decimal("50.0"), expiry_date=date.today() + timedelta(days=30), is_active=True, usage_limit=100, used_count=0),
            Offer(code="SUMMER20", discount_percent=Decimal("20.0"), max_discount_amount=Decimal("100.0"), expiry_date=date.today() + timedelta(days=60), is_active=True, usage_limit=50, used_count=0),
            Offer(code="EARLYBIRD", discount_percent=Decimal("15.0"), max_discount_amount=Decimal("75.0"), expiry_date=date.today() + timedelta(days=15), is_active=True, usage_limit=200, used_count=0),
            Offer(code="FLASH30", discount_percent=Decimal("30.0"), max_discount_amount=Decimal("150.0"), expiry_date=date.today() + timedelta(days=1), is_active=True, usage_limit=20, used_count=0),
            Offer(code="HOLIDAY25", discount_percent=Decimal("25.0"), max_discount_amount=Decimal("120.0"), expiry_date=date.today() + timedelta(days=90), is_active=True, usage_limit=150, used_count=0),
            Offer(code="VIP50", discount_percent=Decimal("50.0"), max_discount_amount=Decimal("500.0"), expiry_date=date.today() + timedelta(days=365), is_active=True, usage_limit=10, used_count=0),
            Offer(code="EXPIRED5", discount_percent=Decimal("5.0"), max_discount_amount=Decimal("10.0"), expiry_date=date.today() - timedelta(days=1), is_active=False, usage_limit=100, used_count=50),
        ]
        db.add_all(offers)
        db.commit()

        # 4. Events
        print("Seeding Events...")
        events = [
            Event(name="Rock Concert", category="Music", event_date=date.today() + timedelta(days=10), ticket_price=Decimal("100.0"), max_tickets_per_user=4, status="Open", venue_id=venues[0].id),
            Event(name="Basketball Game", category="Sports", event_date=date.today() + timedelta(days=5), ticket_price=Decimal("80.0"), max_tickets_per_user=6, status="Open", venue_id=venues[3].id),
            Event(name="Tech Conference", category="Business", event_date=date.today() + timedelta(days=20), ticket_price=Decimal("200.0"), max_tickets_per_user=2, status="Open", venue_id=venues[2].id),
            Event(name="Art Exhibition", category="Culture", event_date=date.today() + timedelta(days=15), ticket_price=Decimal("25.0"), max_tickets_per_user=10, status="Open", venue_id=venues[6].id),
            Event(name="Football Match", category="Sports", event_date=date.today() + timedelta(days=7), ticket_price=Decimal("120.0"), max_tickets_per_user=5, status="Open", venue_id=venues[1].id),
            Event(name="Comedy Night", category="Entertainment", event_date=date.today() + timedelta(days=12), ticket_price=Decimal("50.0"), max_tickets_per_user=4, status="Open", venue_id=venues[5].id),
            Event(name="Magic Show", category="Entertainment", event_date=date.today() + timedelta(days=3), ticket_price=Decimal("40.0"), max_tickets_per_user=8, status="Open", venue_id=venues[4].id),
        ]
        db.add_all(events)
        db.commit()

        # 5. Seats
        print("Seeding Seats...")
        seats = []
        for i, event in enumerate(events):
            for row in range(1, 8):
                seats.append(Seat(seat_number=f"Row-{row}-Seat-{i+1}", status="Available", event_id=event.id))
        db.add_all(seats)
        db.commit()

        # 6. Orders
        print("Seeding Orders...")
        orders = [
            Order(user_id=users[1].id, offer_id=offers[0].id, total_amount=Decimal("100.0"), discount_amount=Decimal("10.0"), final_amount=Decimal("90.0"), payment_mode="Credit Card", order_status="Completed"),
            Order(user_id=users[2].id, offer_id=None, total_amount=Decimal("80.0"), discount_amount=Decimal("0.0"), final_amount=Decimal("80.0"), payment_mode="PayPal", order_status="Completed"),
            Order(user_id=users[3].id, offer_id=offers[2].id, total_amount=Decimal("200.0"), discount_amount=Decimal("30.0"), final_amount=Decimal("170.0"), payment_mode="Debit Card", order_status="Completed"),
            Order(user_id=users[4].id, offer_id=None, total_amount=Decimal("120.0"), discount_amount=Decimal("0.0"), final_amount=Decimal("120.0"), payment_mode="Credit Card", order_status="Pending"),
            Order(user_id=users[5].id, offer_id=offers[1].id, total_amount=Decimal("50.0"), discount_amount=Decimal("10.0"), final_amount=Decimal("40.0"), payment_mode="Credit Card", order_status="Cancelled"),
            Order(user_id=users[6].id, offer_id=None, total_amount=Decimal("25.0"), discount_amount=Decimal("0.0"), final_amount=Decimal("25.0"), payment_mode="UPI", order_status="Completed"),
            Order(user_id=users[1].id, offer_id=None, total_amount=Decimal("40.0"), discount_amount=Decimal("0.0"), final_amount=Decimal("40.0"), payment_mode="Credit Card", order_status="Completed"),
        ]
        db.add_all(orders)
        db.commit()

        # 7. Tickets
        print("Seeding Tickets...")
        tickets = [
            Ticket(order_id=orders[0].id, seat_id=seats[0].id, ticket_code="TICKET-001", status="Confirmed"),
            Ticket(order_id=orders[1].id, seat_id=seats[7].id, ticket_code="TICKET-002", status="Confirmed"),
            Ticket(order_id=orders[2].id, seat_id=seats[14].id, ticket_code="TICKET-003", status="Confirmed"),
            Ticket(order_id=orders[3].id, seat_id=seats[21].id, ticket_code="TICKET-004", status="Reserved"),
            Ticket(order_id=orders[5].id, seat_id=seats[28].id, ticket_code="TICKET-005", status="Confirmed"),
            Ticket(order_id=orders[6].id, seat_id=seats[35].id, ticket_code="TICKET-006", status="Confirmed"),
            Ticket(order_id=orders[6].id, seat_id=seats[42].id, ticket_code="TICKET-007", status="Confirmed"),
        ]
        db.add_all(tickets)
        db.commit()

        # 8. Refund Requests
        print("Seeding Refund Requests...")
        refunds = [
            RefundRequest(order_id=orders[4].id, reason="Changed my mind", status="Approved"),
            RefundRequest(order_id=orders[0].id, reason="Accidental purchase", status="Pending"),
        ]
        db.add_all(refunds)
        db.commit()

        # 9. Support Cases
        print("Seeding Support Cases...")
        cases = [
            SupportCase(user_id=users[1].id, description="Unable to apply coupon", status="Solved", resolution_note="Coupon was expired."),
            SupportCase(user_id=users[2].id, description="Payment failed but amount deducted", status="Open", resolution_note=""),
            SupportCase(user_id=users[3].id, description="Ticekt not received in email", status="In Progress", resolution_note="Verifying with mail server."),
            SupportCase(user_id=users[4].id, description="How to change seat?", status="Solved", resolution_note="Explained the policy."),
            SupportCase(user_id=users[5].id, description="Refund status update", status="Open", resolution_note=""),
            SupportCase(user_id=users[6].id, description="Website keeps crashing on mobile", status="In Progress", resolution_note="Investigating logs."),
            SupportCase(user_id=users[1].id, description="General enquiry about VIP benefits", status="Solved", resolution_note="Sent the details."),
        ]
        db.add_all(cases)
        db.commit()

        # 10. Entry Logs
        print("Seeding Entry Logs...")
        entry_logs = [
            EntryLog(ticket_id=tickets[0].id, entry_time=datetime.utcnow() + timedelta(days=10), status="Success"),
            EntryLog(ticket_id=tickets[1].id, entry_time=datetime.utcnow() + timedelta(days=5), status="Success"),
            EntryLog(ticket_id=tickets[2].id, entry_time=datetime.utcnow() + timedelta(days=20), status="Failed"),
            EntryLog(ticket_id=tickets[4].id, entry_time=datetime.utcnow() + timedelta(days=12), status="Success"),
            EntryLog(ticket_id=tickets[5].id, entry_time=datetime.utcnow() + timedelta(days=3), status="Success"),
            EntryLog(ticket_id=tickets[6].id, entry_time=datetime.utcnow() + timedelta(days=3), status="Success"),
        ]
        db.add_all(entry_logs)
        db.commit()

        print("Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
