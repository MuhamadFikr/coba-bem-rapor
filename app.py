
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

# Dummy user database
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"},
}

# Dummy grades
grades = {
    "user1": {"Triwulan 1": 80, "Triwulan 2": 85, "Triwulan 3": 90}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = users.get(username)

    if user and user["password"] == password:
        session['username'] = username
        session['role'] = user['role']
        return redirect(url_for('dashboard'))
    return "Invalid credentials", 401

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    role = session.get('role')
    username = session.get('username')
    if role == "admin":
        return render_template('admin.html', username=username)
    return render_template('user.html', username=username, grades=grades.get(username, {}))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
