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

@bp.route('/', defaults={'page': 1})
@bp.route('/page/<int:page>')
def index(page):
    db = get_db()
    per_page = 10  # Số bài viết mỗi trang
    offset = (page - 1) * per_page  # Tính toán offset

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, u.is_admin'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
        ' LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()

    total_posts = db.execute('SELECT COUNT(*) FROM post').fetchone()[0]  # Tổng số bài viết
    total_pages = (total_posts + per_page - 1) // per_page  # Tính số trang

    return render_template('blog/index.html', posts=posts, page=page, total_pages=total_pages)

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

@bp.route('/admin/posts')
@login_required
def admin_posts():
    if g.user is None or g.user['is_admin'] == 0:  # Kiểm tra quyền admin
        abort(403)
    posts = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, is_admin'  # Thêm cột is_admin
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('admin_posts.html', posts=posts)  # Đảm bảo rằng trang này hiển thị các bài viết

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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

@bp.route('/delete_multiple', methods=('POST',))
@login_required
def delete_multiple_posts():
    post_ids = request.form.getlist('post_ids')  # Lấy danh sách ID bài viết từ form
    if not post_ids:
        flash('No posts selected for deletion.', 'warning')
        return redirect(url_for('blog.my_posts'))  # Chuyển hướng về trang quản lý bài viết của người dùng

    # Kiểm tra quyền xóa bài viết
    for post_id in post_ids:
        post = get_post(post_id, check_author=False)
        if g.user is None or (g.user['is_admin'] == 0 and post['author_id'] != g.user['id']):
            abort(403)  # Nếu không có quyền, trả về lỗi 403

    db = get_db()
    db.execute('DELETE FROM post WHERE id IN ({})'.format(','.join('?' * len(post_ids))), post_ids)
    db.commit()
    flash('Selected posts have been deleted.', 'success')
    return redirect(url_for('blog.my_posts'))  # Chuyển hướng về trang quản lý bài viết của người dùng

@bp.route('/my_posts', defaults={'page': 1})
@bp.route('/my_posts/page/<int:page>')
@login_required
def my_posts(page):
    db = get_db()
    per_page = 10  # Số bài viết mỗi trang
    offset = (page - 1) * per_page  # Tính toán offset

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.author_id = ?'
        ' ORDER BY created DESC'
        ' LIMIT ? OFFSET ?',
        (g.user['id'], per_page, offset)
    ).fetchall()

    total_posts = db.execute('SELECT COUNT(*) FROM post WHERE author_id = ?', (g.user['id'],)).fetchone()[0]  # Tổng số bài viết của người dùng
    total_pages = (total_posts + per_page - 1) // per_page  # Tính số trang

    return render_template('blog/my_posts.html', posts=posts, page=page, total_pages=total_pages)

@bp.route('/admin/my_posts', defaults={'page': 1})
@bp.route('/admin/my_posts/page/<int:page>')
@login_required
def admin_my_posts(page):
    if g.user is None or g.user['is_admin'] == 0:  # Kiểm tra quyền admin
        abort(403)
    db = get_db()
    per_page = 10  # Số bài viết mỗi trang
    offset = (page - 1) * per_page  # Tính toán offset

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?'
        ' ORDER BY created DESC'
        ' LIMIT ? OFFSET ?',
        (g.user['id'], per_page, offset)
    ).fetchall()

    total_posts = db.execute('SELECT COUNT(*) FROM post WHERE author_id = ?', (g.user['id'],)).fetchone()[0]  # Tổng số bài viết của người dùng
    total_pages = (total_posts + per_page - 1) // per_page  # Tính số trang

    return render_template('blog/admin_my_posts.html', posts=posts, page=page, total_pages=total_pages)
