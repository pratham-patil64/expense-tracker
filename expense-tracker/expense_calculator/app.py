from flask import Flask, render_template, request, redirect, session
import psycopg2
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a secure, random key in production

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="expense_tracker",
    user="postgres",
    password="Pratham@0604",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create tables if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    description TEXT,
    amount NUMERIC,
    category TEXT,
    date DATE DEFAULT CURRENT_DATE
);
""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    amount = request.form['amount']
    category = request.form['category']
    cur.execute("INSERT INTO expenses (description, amount, category) VALUES (%s, %s, %s)",
                (description, amount, category))
    conn.commit()
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)

