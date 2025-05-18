from flask import Blueprint, render_template
from .db import get_db

bp = Blueprint('main', __name__)

# Root page
@bp.route('/')
def home():
    db = get_db()
    posts = db.execute("""
        SELECT p.id, p.title, p.content, p.pub_date,
               GROUP_CONCAT(t.name) AS tags
        FROM posts p
        LEFT JOIN post_tags pt ON p.id = pt.post_id
        LEFT JOIN tags t ON pt.tag_id = t.id
        GROUP BY p.id
        ORDER BY p.pub_date DESC
    """).fetchall()

    return render_template('home.html', posts=posts)

# full blog post view placeholder
@bp.route('/post/<int:post_id>')
def post_detail(post_id):
    return f"Placeholder for post ID: {post_id}"

# Tag page placeholder
@bp.route('/tags/<string:tag_name>')
def tag_page(tag_name):
    return f"Posts tagged with: {tag_name}"