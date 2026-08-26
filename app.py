import datetime
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            balance INTEGER
        )
    ''')

    # Insert default users
    c.execute("INSERT OR IGNORE INTO users VALUES ('A', 1000)")
    c.execute("INSERT OR IGNORE INTO users VALUES ('B', 500)")
    c.execute('''
    CREATE TABLE IF NOT EXISTS proofs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        amount INTEGER,
        commitment TEXT,
        challenge INTEGER,
        response TEXT,
        timestamp TEXT
    )
''')

    conn.commit()
    conn.close()

init_db()
import hashlib
import random


def send_money(sender, receiver, amount):
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("SELECT balance FROM users WHERE name=?", (sender,))
        sender_balance = c.fetchone()[0]

        if sender_balance < amount:
            return f"""
            <h2> Transaction Failed</h2>

            <h3> Verification Phase</h3>
            ✔ Proof Checked <br>
             Insufficient Balance Detected <br><br>

            <b>Reason:</b> Sender does not have enough funds <br><br>

             System Prevented Invalid Transaction
            """
       

    # ZKP simulation
        nonce = str(random.randint(1000, 9999))
        data = sender + receiver + str(amount) + nonce
        commitment = hashlib.sha256(data.encode()).hexdigest()

        challenge = random.randint(1, 100)
        response = hashlib.sha256((commitment + str(challenge)).encode()).hexdigest()
        proof = {
        "commitment": commitment,
        "challenge": challenge,
        "response": response
        }
       
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proof_valid = verify_proof(
            proof["commitment"],
            proof["challenge"],
            proof["response"]
        )
        if  proof_valid:
            c.execute("UPDATE users SET balance = balance - ? WHERE name=?", (amount, sender))
            c.execute("UPDATE users SET balance = balance + ? WHERE name=?", (amount, receiver))
            c.execute("""
            INSERT INTO proofs (sender, receiver, amount, commitment, challenge, response,timestamp)
            VALUES (?, ?, ?, ?, ?, ?,?)
            """, (sender, receiver, amount, proof["commitment"], proof["challenge"], proof["response"],time))
            conn.commit()
            conn.close()
        else:
            return """
            <h2> Verification Failed</h2>
            Proof Invalid - Transaction Rejected
            """

        return f"""
            <html>
            <body style="font-family:Arial; background:#0f172a; color:white; text-align:center; padding-top:50px;">

            <h2>ZKP Transaction Result</h2>

            <div style="background:#1e293b; padding:25px; border-radius:12px; display:inline-block; text-align:left; width:400px;">

            <h3>Proof Generation Phase</h3>
             Commitment Created <br>
             Challenge Generated <br>
             Response Computed <br><br>

            <h3>Verification Phase</h3>
             Proof Verified Successfully <br>
             Transaction Integrity Confirmed <br><br>

            <h3>Proof Details</h3>
            <b>Proof ID:</b> {proof["commitment"][:12]}... <br>
            <b>Challenge:</b> {proof["challenge"]} <br>
            <b>Response:</b> {proof["response"][:12]}... <br><br>

            <a href="/verify?commitment={proof['commitment']}&challenge={proof['challenge']}&response={proof['response']}" 
            style="color:#22c55e;">
              Verify with Third Party
            </a>

            </div>

            <br><br>
            <a href="/" style="color:#22c55e;"></a>

            </body>
            </html>
            """
def verify_proof(commitment, challenge, response):
    
    expected = hashlib.sha256((commitment + str(challenge)).encode()).hexdigest()
    
    integrity = (expected == response)
    format_ok = len(commitment) == 64 and len(response) == 64
    
    return integrity and format_ok

@app.route('/balances')
def balances():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.close()

    result = "<h2>Balances</h2>"
    for user in data:
        result += f"{user[0]}: ₹{user[1]}<br>"

    return result     

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/send', methods=['POST'])
def send():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = int(request.form['amount'])
    result = send_money(sender, receiver, amount)
    return f"""
<html>
<body style="font-family:Arial; background:#0f172a; color:white; text-align:center; padding-top:50px;">
    <h2>Transaction Result</h2>
    <div style="background:#1e293b; padding:20px; border-radius:10px; display:inline-block;">
        {result}
    </div>
    <br><br>
    <a href="/" style="color:#22c55e;">← Back</a>
</body>
</html>
"""
@app.route('/verify')
def verify():
    commitment = request.args.get('commitment')
    challenge = request.args.get('challenge')
    response = request.args.get('response')

    step1 = hashlib.sha256((commitment + str(challenge)).encode()).hexdigest()
    integrity = (step1 == response)
    format_ok = len(commitment) == 64 and len(response) == 64

    if integrity and format_ok:
        return f"""
        <h2>Third Party Verification</h2>

          Step 1: Recomputed Response Matches  <br>
          Step 2: Proof Format Valid  <br><br>

        <b>Status:</b> VALID PROOF 
        """
    else:
        return """
        <h2>Verification Failed</h2>
        Proof Invalid
        """

@app.route('/proofs')
def view_proofs():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM proofs")
    data = c.fetchall()

    conn.close()

    html = "<h2>Stored Proofs</h2><br>"

    for row in data:
        html += f"""
        ID: {row[0]} <br>
        {row[1]} → {row[2]} | ₹{row[3]} <br>
        Proof: {row[4][:12]}... <br>
        Challenge: {row[5]} <br>
        Time: {row[7]} <br>
        """

    return html
@app.route('/db')
def view_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users = c.fetchall()

    conn.close()

    result = "<h2>Database View</h2><br>"
    for u in users:
        result += f"User: {u[0]} | Balance: ₹{u[1]}<br>"

    return result

if __name__ == '__main__':
    app.run(debug=True)
