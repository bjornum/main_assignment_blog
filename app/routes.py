from flask import Blueprint, render_template, request, redirect, url_for, flash

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
@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    db = get_db()

    post = db.execute("""
        SELECT p.id, p.title, p.content, p.pub_date,
               GROUP_CONCAT(t.name) AS tags
        FROM posts p
        LEFT JOIN post_tags pt ON p.id = pt.post_id
        LEFT JOIN tags t ON pt.tag_id = t.id
        WHERE p.id = ?
        GROUP BY p.id
    """, (post_id,)).fetchone()

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()

        if not title or not content:
            flash("Title and content are required.", "error")
        else:
            db.execute(
                "INSERT INTO comments (post_id, title, content, pub_date) VALUES (?, ?, ?, DATE('now'))",
                (post_id, title, content)
            )
            db.commit()
            flash("Comment added!", "success")
            return redirect(url_for('main.post_detail', post_id=post_id))

    comments = db.execute("""
        SELECT title, content, pub_date
        FROM comments
        WHERE post_id = ?
        ORDER BY pub_date DESC
    """, (post_id,)).fetchall()

    return render_template('post_detail.html', post=post, comments=comments)


# Tag page placeholder
@bp.route('/tags/<string:tag_name>')
def tag_page(tag_name):
    return f"Posts tagged with: {tag_name}"