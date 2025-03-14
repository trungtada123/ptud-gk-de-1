# flask-tiny-app/flaskr/auth.py
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Mặc định người dùng đăng ký không phải là admin
        is_admin = False
        
        db = get_db()
        error = None

        if not username:
            error = 'Tên đăng nhập là bắt buộc.'
        elif not password:
            error = 'Mật khẩu là bắt buộc.'
        elif len(username) < 3:
            error = 'Tên đăng nhập phải có ít nhất 3 ký tự.'
        elif len(password) < 8:
            error = 'Mật khẩu phải có ít nhất 8 ký tự.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"Người dùng {username} đã tồn tại."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), is_admin)
            )
            db.commit()
            flash(f'Tài khoản "{username}" đã được tạo thành công!')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Tên đăng nhập không chính xác.'
        elif not check_password_hash(user['password'], password):
            error = 'Mật khẩu không chính xác.'
        elif user['is_blocked']:
            error = 'Tài khoản này đã bị chặn. Vui lòng liên hệ quản trị viên.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            
            # Đăng nhập thành công, hiển thị thông báo và chuyển hướng
            flash(f'Chào mừng, {username}!')
            if user['is_admin']:
                flash('Bạn đã đăng nhập với tư cách quản trị viên.')
            return redirect(url_for('blog.blog_index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()  # fetchone() trả về một sqlite3.Row

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view