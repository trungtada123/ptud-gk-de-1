# flask-tiny-app/flaskr/blog.py
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.security import generate_password_hash
import random
import string

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_post(id):
    post = get_post(id, check_author=False)  # Kiểm tra quyền tác giả
    # Kiểm tra xem người dùng có quyền xóa bài viết
    if g.user is None or (g.user['is_admin'] == 0 and post['author_id'] != g.user['id']):
        abort(403)  # Nếu không có quyền, trả về lỗi 403
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    flash('Post has been deleted.', 'success')
    return redirect(url_for('blog.index'))  # Chuyển hướng đến trang blog chính

@bp.route('/admin')
@login_required
def admin():
    if g.user is None or g.user['is_admin'] == 0:  # Kiểm tra quyền admin
        abort(403)
    users = get_db().execute('SELECT * FROM user').fetchall()
    return render_template('admin.html', users=users)

@bp.route('/admin/block/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    if g.user is None or g.user['is_admin'] == 0:  # Kiểm tra quyền admin
        abort(403)
    db = get_db()
    db.execute('UPDATE user SET is_blocked = 1 WHERE id = ?', (user_id,))
    db.commit()
    flash('User has been blocked.', 'success')
    return redirect(url_for('blog.admin'))

@bp.route('/admin/unblock/<int:user_id>', methods=['POST'])
@login_required
def unblock_user(user_id):
    if g.user is None or g.user['is_admin'] == 0:  # Kiểm tra quyền admin
        abort(403)
    db = get_db()
    db.execute('UPDATE user SET is_blocked = 0 WHERE id = ?', (user_id,))
    db.commit()
    flash('User has been unblocked.', 'success')
    return redirect(url_for('blog.admin'))

# flask-tiny-app/flaskr/blog.py
@bp.route('/admin/posts')
@login_required
def admin_posts():
    if g.user is None or g.user['is_admin'] == 0:  # Kiểm tra quyền admin
        abort(403)
    posts = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('admin_posts.html', posts=posts)  # Đảm bảo rằng trang này hiển thị các bài viết

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# flask-tiny-app/flaskr/blog.py
@bp.route('/admin/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if g.user is None or g.user['is_admin'] == 0:  # Kiểm tra quyền admin
        abort(403)
    new_password = generate_random_password()  # Tạo mật khẩu mới
    db = get_db()
    db.execute('UPDATE user SET password = ? WHERE id = ?', (generate_password_hash(new_password), user_id))
    db.commit()
    flash('Password has been reset. New password: ' + new_password, 'success')
    return redirect(url_for('blog.admin'))