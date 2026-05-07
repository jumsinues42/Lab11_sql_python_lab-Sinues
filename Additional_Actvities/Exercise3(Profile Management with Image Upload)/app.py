from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret_key_for_session"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create directory if missing
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db_connection():
    conn = sqlite3.connect('attendance_system.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db_connection()
    # Fetching the updated name and profile picture (Requirement)
    users = conn.execute('SELECT * FROM user_profiles').fetchall()
    conn.close()
    return render_template('dashboard.html', users=users)

@app.route('/update', methods=['POST'])
def update_profile():
    user_id = request.form['user_id']
    new_name = request.form['name']
    file = request.files['file']

    # CALCULATIONS: Extension Validation (Requirement)
    if file and file.filename.endswith(('.png', '.jpg', '.jpeg')):
        filename = f"user_{user_id}_{file.filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db_connection()
        conn.execute('INSERT OR REPLACE INTO user_profiles (id, name, image_filename) VALUES (?, ?, ?)',
                     (user_id, new_name, filename))
        conn.commit()
        conn.close()
        
        flash(f"Profile updated successfully for {new_name}!") # Flash Requirement
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)