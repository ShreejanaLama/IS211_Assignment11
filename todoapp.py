from flask import Flask, render_template, request, redirect
import os
import pickle
import re

app = Flask(__name__)

DATA_FILE = 'todo_data.pkl'

# Load saved list if file exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'rb') as f:
        todo_list = pickle.load(f)
else:
    todo_list = []

@app.route('/')
def index():
    return render_template('index.html', todos=todo_list)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task', '').strip()
    email = request.form.get('email', '').strip()
    priority = request.form.get('priority', '')

    # Validation
    if not task or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or priority not in ['Low', 'Medium', 'High']:
        return redirect('/')

    # Add new item
    todo_list.append({'task': task, 'email': email, 'priority': priority})
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    todo_list.clear()
    return redirect('/')

@app.route('/save', methods=['POST'])
def save():
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(todo_list, f)
    return redirect('/')

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if 0 <= index < len(todo_list):
        todo_list.pop(index)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
