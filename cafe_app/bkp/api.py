from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample data
users = []
tokens = []


@app.route('/api/login', methods=['POST'])
def login():
    data = request.form
    # Perform authentication (mocked)
    return jsonify({'status': 'success'})


@app.route('/api/book-seat', methods=['POST'])
def book_seat():
    user_id = request.form['user_id']
    seat_id = request.form['seat_id']
    expires_at = datetime.now() + timedelta(hours=1)
    token = {'id': 1, 'user_id': user_id, 'seat_id': seat_id, 'expires_at': expires_at}
    tokens.append(token)
    return jsonify(token)


@app.route('/api/books', methods=['GET'])
def get_books():
    # Mock list of books
    books = [{'title': 'Book 1'}, {'title': 'Book 2'}, {'title': 'Book 3'}]
    return jsonify(books)


@app.route('/api/token', methods=['GET'])
def get_token():
    user_id = request.args.get('user_id')
    # Find the token for the user
    token = next((t for t in tokens if t['user_id'] == user_id), None)
    if token:
        return jsonify(token)
    return jsonify({'error': 'No active token'}), 404


if __name__ == '__main__':
    app.run(debug=True)
