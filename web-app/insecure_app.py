from flask import Flask, request, render_template_string, redirect, make_response, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Simulated DB for SQL Injection
conn = sqlite3.connect("users.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

@app.route("/")
def home():
    return """
    <h1>Insecure App</h1>
    <ul>
        <li><a href="/xss">XSS Demo</a></li>
        <li><a href="/sqli">SQL Injection Demo</a></li>
        <li><a href="/csrf">CSRF Demo</a></li>
        <li><a href="/upload">Insecure File Upload</a></li>
        <li><a href="/login">Broken Auth</a></li>
    </ul>
    """

# --- 1. XSS ---
@app.route("/xss", methods=["GET", "POST"])
def xss():
    if request.method == "POST":
        comment = request.form["comment"]
        return render_template_string(f"<h2>Comment received:</h2><p>{comment}</p>")
    return """
        <form method="post">
            <input name="comment" placeholder="Enter comment">
            <input type="submit">
        </form>
    """

# --- 2. SQL Injection ---
@app.route("/sqli", methods=["GET", "POST"])
def sqli():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = conn.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        if cursor.fetchone():
            return "✅ Logged in!"
        return "❌ Login failed!"
    return """
        <form method="post">
            <input name="username" placeholder="Username"><br>
            <input name="password" placeholder="Password"><br>
            <input type="submit">
        </form>
    """

# --- 3. CSRF ---
@app.route("/csrf", methods=["GET", "POST"])
def csrf():
    if request.method == "POST":
        # Pretend this changes user email
        return f"Email changed to: {request.form['email']}"
    return """
        <form method="post">
            <input name="email" placeholder="New email">
            <input type="submit" value="Change Email">
        </form>
    """

# --- 4. Insecure File Upload ---
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join("uploads", file.filename)
        file.save(path)
        return f"File saved to {path}"
    return """
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
        </form>
    """

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('app/uploads', filename)

# --- 5. Broken Auth (no session checking) ---

# Fake user database (insecure, for demo only)
users = {
    "admin": "admin",
    "user": "user",
    "guest": "guest"
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username in users and users[username] == password:
            resp = make_response(f"✅ Logged in as {username}")
            resp.set_cookie("auth", username)
            return resp
        else:
            return "❌ Invalid username or password"

    return """
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="Username"><br>
            <input name="password" type="password" placeholder="Password"><br>
            <input type="submit" value="Login">
        </form>
    """

@app.route("/admin")
def admin():
    user = request.cookies.get("auth", "guest")
    if user != "admin":
        return "<h1>Access Denied</h1><p>You are not authorized to view this page.</p>", 403
    return f"<h1>Welcome, {user}</h1><p>This is the admin panel.</p>"

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5050)
