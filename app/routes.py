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

# full blog post view 
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
        SELECT id, title, content, pub_date
        FROM comments
        WHERE post_id = ?
        ORDER BY pub_date DESC
    """, (post_id,)).fetchall()

    return render_template('post_detail.html', post=post, comments=comments)


# Tag page
@bp.route('/tags/<string:tag_name>')
def tag_page(tag_name):
    db = get_db()
    posts = db.execute("""
        SELECT p.id, p.title, p.content, p.pub_date,
               GROUP_CONCAT(t.name) AS tags
        FROM posts p
        JOIN post_tags pt ON p.id = pt.post_id
        JOIN tags t ON pt.tag_id = t.id
        WHERE t.name = ?
        GROUP BY p.id
        ORDER BY p.pub_date DESC
    """, (tag_name,)).fetchall()

    return render_template('tag.html', posts=posts, tag_name=tag_name)

# Create a new post
@bp.route('/create', methods=['GET', 'POST'])
def create_post():
    db = get_db()

    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        tags_input = request.form['tags'].strip()

        if not title or not content:
            flash("Title and content are required.", "error")
        else:
            db.execute(
                "INSERT INTO posts (title, content, pub_date) VALUES (?, ?, DATE('now'))",
                (title, content)
            )
            post_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

            # Handle tags
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for name in tag_names:
                db.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (name,))
                tag_id = db.execute("SELECT id FROM tags WHERE name = ?", (name,)).fetchone()['id']
                db.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)", (post_id, tag_id))

            db.commit()
            flash("Post created!", "success")
            return redirect(url_for('main.post_detail', post_id=post_id))

    return render_template('create_post.html')

# Edit a post
@bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    db = get_db()

    # Get post data
    post = db.execute("""
        SELECT p.id, p.title, p.content,
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
        tags_input = request.form['tags'].strip()

        if not title or not content:
            flash("Title and content are required.", "error")
        else:
            db.execute(
                "UPDATE posts SET title = ?, content = ? WHERE id = ?",
                (title, content, post_id)
            )

            # Clear old tags and re-insert
            db.execute("DELETE FROM post_tags WHERE post_id = ?", (post_id,))
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for name in tag_names:
                db.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (name,))
                tag_id = db.execute("SELECT id FROM tags WHERE name = ?", (name,)).fetchone()['id']
                db.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)", (post_id, tag_id))

            db.commit()
            flash("Post updated!", "success")
            return redirect(url_for('main.post_detail', post_id=post_id))

    return render_template('edit_post.html', post=post)

# Delete a post
@bp.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    db = get_db()

    # Check if post exists
    post = db.execute("SELECT id FROM posts WHERE id = ?", (post_id,)).fetchone()
    if not post:
        return "Post not found", 404

    # Delete tags and comments first (foreign key cleanup)
    db.execute("DELETE FROM post_tags WHERE post_id = ?", (post_id,))
    db.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()

    flash("Post deleted.", "success")
    return redirect(url_for('main.home'))

# Delete a comment
@bp.route('/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    db = get_db()

    comment = db.execute("SELECT post_id FROM comments WHERE id = ?", (comment_id,)).fetchone()
    if not comment:
        return "Comment not found", 404

    db.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    db.commit()

    flash("Comment deleted.", "success")
    return redirect(url_for('main.post_detail', post_id=comment['post_id']))
