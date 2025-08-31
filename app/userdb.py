import psycopg2
import bcrypt

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="userdb",
    user="admin",
    password="admin123"
)
cur = conn.cursor()

# --- Function to register a new user ---
def register_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed)
        )
        conn.commit()
        print(f"User '{username}' registered successfully.")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Username already exists.")

# --- Function to login ---
def login_user(username, password):
    cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].tobytes()):
        print(f"Login successful. Welcome, {username}!")
        return True
    else:
        print("Login failed. Invalid username or password.")
        return False

# --- Example usage ---
if __name__ == "__main__":
    # Insert a test user
    register_user("anjitha", "mypassword123")

    # Try logging in
    login_user("anjitha", "mypassword123")

# Close connection
cur.close()
conn.close()
