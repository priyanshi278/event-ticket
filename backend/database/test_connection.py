import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Force load .env from the root directory
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

DATABASE_URL = os.getenv("DATABASE_URL")

def test_connection():
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in environment variables.")
        return

    print(f"Testing connection to: {DATABASE_URL.split('@')[-1]}") # Print only host for security
    
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(f"Query result: {result.scalar()}")
    except Exception as e:
        print(f"Database connection failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")

if __name__ == "__main__":
    test_connection()
