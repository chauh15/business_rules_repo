# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/api/greet')
def greet():
    return 'Greetings from Flask API!'

if __name__ == '__main__':
    app.run(debug=True)

