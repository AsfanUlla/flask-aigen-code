from flask import Blueprint, render_template, request, jsonify
from db import db, Comment

views = Blueprint('views', __name__)


@views.route('/')
def home():
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return render_template('index.html', name="Name", comments=comments)


@views.route('/add_comment', methods=['POST'])
def add_comment():
    try:
        author = request.form.get('author')
        content = request.form.get('content')

        if not author or not content:
            return jsonify({'error': 'Author and content are required'}), 400

        new_comment = Comment(author=author, content=content)
        db.session.add(new_comment)
        db.session.commit()

        return jsonify({
            'id': new_comment.id,
            'author': new_comment.author,
            'content': new_comment.content,
            'timestamp': new_comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'upvotes': new_comment.upvotes
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@views.route('/upvote/<int:comment_id>', methods=['POST'])
def upvote(comment_id):
    try:
        comment = Comment.query.get_or_404(comment_id)
        comment.upvotes += 1
        db.session.commit()
        return jsonify({'upvotes': comment.upvotes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
