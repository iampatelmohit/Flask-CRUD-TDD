from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# DATABASE 
comments_db = [
    {'id': 1, 'task_id': 1, 'text': 'hello', 'author': 'boss'}
]

def get_next_id():
    if not comments_db:
        return 1
    return max(comment['id'] for comment in comments_db) + 1

# ROUTES 

# NEW Route to serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# API: Get Comments
@app.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    task_comments = [c for c in comments_db if c['task_id'] == task_id]
    return jsonify(task_comments), 200

# API: Add Comment
@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Comment text is required'}), 400

    new_comment = {
        'id': get_next_id(),
        'task_id': task_id,
        'text': data['text'],
        'author': data.get('author', 'Anonymous')
    }
    comments_db.append(new_comment)
    return jsonify(new_comment), 201

# API: Update Comment
@app.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.get_json()
    comment = next((c for c in comments_db if c['id'] == comment_id), None)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    if 'text' in data:
        comment['text'] = data['text']
    return jsonify(comment), 200

# API: Delete Comment
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments_db
    comments_db = [c for c in comments_db if c['id'] != comment_id]
    return jsonify({'message': 'Comment deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)