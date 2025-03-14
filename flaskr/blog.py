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
import os  # Thêm import os

bp = Blueprint('blog', __name__)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        text_content = request.form.get('text_content', '')
        error = None

        if not title:
            error = 'Tiêu đề là bắt buộc.'

        # Kiểm tra xem có ít nhất một loại nội dung nào đó
        has_content = False
        if text_content.strip():
            has_content = True
        
        # Kiểm tra có hình ảnh không
        images = request.files.getlist('images[]')
        has_images = any(img.filename for img in images)
        if has_images:
            has_content = True
        
        # Kiểm tra có liên kết không
        links = request.form.getlist('links[]')
        has_links = any(link.strip() for link in links)
        if has_links:
            has_content = True
        
        if not has_content:
            error = 'Bài viết phải có ít nhất một loại nội dung: văn bản, hình ảnh hoặc liên kết.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            
            # Tạo bài viết mới với nội dung văn bản
            cursor = db.execute(
                'INSERT INTO post (title, text_content, author_id)'
                ' VALUES (?, ?, ?)',
                (title, text_content, g.user['id'])
            )
            post_id = cursor.lastrowid
            
            # Xử lý hình ảnh
            display_order = 0
            for image in images:
                if image.filename:
                    # Đảm bảo thư mục tồn tại
                    os.makedirs('flaskr/static/images', exist_ok=True)
                    # Tạo tên file duy nhất để tránh trùng lặp
                    filename = f"{post_id}_{display_order}_{image.filename}"
                    image_path = os.path.join('flaskr/static/images', filename)
                    image.save(image_path)
                    
                    # Lưu đường dẫn web (không phải đường dẫn hệ thống tệp)
                    web_path = f"/static/images/{filename}"
                    
                    # Lưu thông tin hình ảnh vào bảng post_content
                    db.execute(
                        'INSERT INTO post_content (post_id, content_type, content, display_order)'
                        ' VALUES (?, ?, ?, ?)',
                        (post_id, 'image', web_path, display_order)
                    )
                    display_order += 1
            
            # Xử lý liên kết
            for link in links:
                if link.strip():
                    # Đảm bảo link bắt đầu bằng http:// hoặc https://
                    if not link.startswith(('http://', 'https://')):
                        link = 'https://' + link
                    
                    # Lưu thông tin liên kết vào bảng post_content
                    db.execute(
                        'INSERT INTO post_content (post_id, content_type, content, display_order)'
                        ' VALUES (?, ?, ?, ?)',
                        (post_id, 'link', link, display_order)
                    )
                    display_order += 1
            
            db.commit()
            return redirect(url_for('blog.blog_index'))

    return render_template('blog/create.html')

@bp.route('/index')
def blog_index():
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Lấy bài viết với phân trang
    posts_rows = db.execute(
        'SELECT p.id, p.title, p.text_content, p.created, u.username, u.id as author_id'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY p.created DESC LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    
    # Chuyển đổi sqlite3.Row thành list của dictionaries
    posts = []
    for post_row in posts_rows:
        # Chuyển đổi Row thành dict
        post = dict(post_row)
        
        # Lấy nội dung đa phương tiện cho bài viết
        contents = db.execute(
            'SELECT content_type, content, display_order'
            ' FROM post_content'
            ' WHERE post_id = ?'
            ' ORDER BY display_order',
            (post['id'],)
        ).fetchall()
        
        # Thêm danh sách hình ảnh và liên kết vào post
        post['images'] = [c['content'] for c in contents if c['content_type'] == 'image']
        post['links'] = [c['content'] for c in contents if c['content_type'] == 'link']
        
        posts.append(post)

    # Đếm tổng số bài viết
    total_posts = db.execute('SELECT COUNT(*) FROM post').fetchone()[0]
    total_pages = (total_posts + per_page - 1) // per_page

    return render_template('blog/index.html', posts=posts, page=page, total_pages=total_pages)

@bp.route('/my_posts')
@login_required
def my_posts():
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Lấy bài viết của người dùng hiện tại với phân trang
    posts_rows = db.execute(
        'SELECT p.id, p.title, p.text_content, p.created, u.username, u.id as author_id'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.author_id = ? ORDER BY p.created DESC LIMIT ? OFFSET ?',
        (g.user['id'], per_page, offset)
    ).fetchall()
    
    # Chuyển đổi sqlite3.Row thành list của dictionaries
    posts = []
    for post_row in posts_rows:
        post = dict(post_row)
        
        # Lấy nội dung đa phương tiện cho bài viết
        contents = db.execute(
            'SELECT content_type, content, display_order'
            ' FROM post_content'
            ' WHERE post_id = ?'
            ' ORDER BY display_order',
            (post['id'],)
        ).fetchall()
        
        post['images'] = [c['content'] for c in contents if c['content_type'] == 'image']
        post['links'] = [c['content'] for c in contents if c['content_type'] == 'link']
        
        posts.append(post)
    
    # Đếm tổng số bài viết để tính số trang
    total_posts = db.execute(
        'SELECT COUNT(*) FROM post WHERE author_id = ?', 
        (g.user['id'],)
    ).fetchone()[0]
    
    total_pages = (total_posts + per_page - 1) // per_page
    
    return render_template('blog/my_posts.html', posts=posts, page=page, total_pages=total_pages)

@bp.route('/admin')
@login_required
def admin():
    # Kiểm tra xem người dùng có phải là admin không
    if not g.user['is_admin']:
        return redirect(url_for('blog.blog_index'))
    
    # Lấy danh sách người dùng
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    
    return render_template('admin.html', users=users)

@bp.route('/admin/posts')
@login_required
def admin_posts():
    # Kiểm tra xem người dùng có phải là admin không
    if not g.user['is_admin']:
        return redirect(url_for('blog.blog_index'))
    
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Lấy tất cả bài viết với phân trang
    posts_rows = db.execute(
        'SELECT p.id, p.title, p.text_content, p.created, u.username, u.id as author_id'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY p.created DESC LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    
    # Chuyển đổi sqlite3.Row thành list của dictionaries
    posts = []
    for post_row in posts_rows:
        post = dict(post_row)
        
        # Lấy nội dung đa phương tiện cho bài viết
        contents = db.execute(
            'SELECT content_type, content, display_order'
            ' FROM post_content'
            ' WHERE post_id = ?'
            ' ORDER BY display_order',
            (post['id'],)
        ).fetchall()
        
        post['images'] = [c['content'] for c in contents if c['content_type'] == 'image']
        post['links'] = [c['content'] for c in contents if c['content_type'] == 'link']
        
        posts.append(post)
    
    # Đếm tổng số bài viết để tính số trang
    total_posts = db.execute('SELECT COUNT(*) FROM post').fetchone()[0]
    total_pages = (total_posts + per_page - 1) // per_page
    
    return render_template('admin_posts.html', posts=posts, page=page, total_pages=total_pages)

@bp.route('/admin/my_posts')
@login_required
def admin_my_posts():
    # Kiểm tra xem người dùng có phải là admin không
    if not g.user['is_admin']:
        return redirect(url_for('blog.blog_index'))
    
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Lấy bài viết của admin với phân trang
    posts_rows = db.execute(
        'SELECT p.id, p.title, p.text_content, p.created, u.username, u.id as author_id'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.author_id = ? ORDER BY p.created DESC LIMIT ? OFFSET ?',
        (g.user['id'], per_page, offset)
    ).fetchall()
    
    # Chuyển đổi sqlite3.Row thành list của dictionaries
    posts = []
    for post_row in posts_rows:
        post = dict(post_row)
        
        # Lấy nội dung đa phương tiện cho bài viết
        contents = db.execute(
            'SELECT content_type, content, display_order'
            ' FROM post_content'
            ' WHERE post_id = ?'
            ' ORDER BY display_order',
            (post['id'],)
        ).fetchall()
        
        post['images'] = [c['content'] for c in contents if c['content_type'] == 'image']
        post['links'] = [c['content'] for c in contents if c['content_type'] == 'link']
        
        posts.append(post)
    
    # Đếm tổng số bài viết để tính số trang
    total_posts = db.execute(
        'SELECT COUNT(*) FROM post WHERE author_id = ?', 
        (g.user['id'],)
    ).fetchone()[0]
    
    total_pages = (total_posts + per_page - 1) // per_page
    
    return render_template('blog/admin_my_posts.html', posts=posts, page=page, total_pages=total_pages)

@bp.route('/block_user/<int:user_id>', methods=('POST',))
@login_required
def block_user(user_id):
    # Kiểm tra xem người dùng có phải là admin không
    if not g.user['is_admin']:
        return redirect(url_for('blog.blog_index'))
    
    db = get_db()
    
    # Kiểm tra xem người dùng cần block có phải là admin không
    user_to_block = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    if user_to_block['is_admin']:
        flash('Không thể block tài khoản admin')
        return redirect(url_for('blog.admin'))
    
    db.execute('UPDATE user SET is_blocked = 1 WHERE id = ?', (user_id,))
    db.commit()
    
    return redirect(url_for('blog.admin'))

@bp.route('/unblock_user/<int:user_id>', methods=('POST',))
@login_required
def unblock_user(user_id):
    # Kiểm tra xem người dùng có phải là admin không
    if not g.user['is_admin']:
        return redirect(url_for('blog.blog_index'))
    
    db = get_db()
    db.execute('UPDATE user SET is_blocked = 0 WHERE id = ?', (user_id,))
    db.commit()
    
    return redirect(url_for('blog.admin'))

@bp.route('/reset_password/<int:user_id>', methods=('POST',))
@login_required
def reset_password(user_id):
    # Kiểm tra xem người dùng có phải là admin không
    if not g.user['is_admin']:
        return redirect(url_for('blog.blog_index'))
    
    # Tạo mật khẩu ngẫu nhiên
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    db = get_db()
    db.execute('UPDATE user SET password = ? WHERE id = ?', (generate_password_hash(new_password), user_id))
    db.commit()
    
    flash(f'Mật khẩu mới: {new_password}')
    return redirect(url_for('blog.admin'))

def get_post(id, check_author=True):
    db = get_db()
    # Lấy thông tin cơ bản của bài viết
    post_row = db.execute(
        'SELECT p.id, title, text_content, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post_row is None:
        abort(404, f"Bài viết có ID {id} không tồn tại.")

    # Chuyển đổi sqlite3.Row thành dict
    post = dict(post_row)
    
    # Lấy nội dung đa phương tiện
    contents = db.execute(
        'SELECT content_type, content, display_order'
        ' FROM post_content'
        ' WHERE post_id = ?'
        ' ORDER BY display_order',
        (id,)
    ).fetchall()
    
    # Thêm danh sách hình ảnh và liên kết vào post
    post['images'] = [c['content'] for c in contents if c['content_type'] == 'image']
    post['links'] = [c['content'] for c in contents if c['content_type'] == 'link']

    if check_author and post['author_id'] != g.user['id'] and not g.user['is_admin']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        text_content = request.form.get('text_content', '')
        keep_text = request.form.get('keep_text') == 'on'
        keep_images = request.form.get('keep_images') == 'on'
        keep_links = request.form.get('keep_links') == 'on'
        error = None

        if not title:
            error = 'Tiêu đề là bắt buộc.'

        # Kiểm tra xem có ít nhất một loại nội dung nào đó
        has_content = False
        if text_content.strip() or (keep_text and post['text_content']):
            has_content = True
        
        # Kiểm tra có hình ảnh không
        images = request.files.getlist('images[]')
        has_images = any(img.filename for img in images)
        if has_images or (keep_images and post['images']):
            has_content = True
        
        # Kiểm tra có liên kết không
        links = request.form.getlist('links[]')
        has_links = any(link.strip() for link in links)
        if has_links or (keep_links and post['links']):
            has_content = True
        
        if not has_content:
            error = 'Bài viết phải có ít nhất một loại nội dung: văn bản, hình ảnh hoặc liên kết.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            
            # Cập nhật nội dung văn bản
            if not keep_text:
                db.execute(
                    'UPDATE post SET title = ?, text_content = ?'
                    ' WHERE id = ?',
                    (title, text_content, id)
                )
            else:
                db.execute(
                    'UPDATE post SET title = ?'
                    ' WHERE id = ?',
                    (title, id)
                )
            
            # Xóa nội dung đa phương tiện cũ nếu không giữ lại
            if not keep_images:
                db.execute('DELETE FROM post_content WHERE post_id = ? AND content_type = ?', (id, 'image'))
            
            if not keep_links:
                db.execute('DELETE FROM post_content WHERE post_id = ? AND content_type = ?', (id, 'link'))
            
            # Xử lý hình ảnh mới
            if images and any(img.filename for img in images):
                # Lấy display_order lớn nhất hiện tại cho hình ảnh
                max_order = db.execute(
                    'SELECT COALESCE(MAX(display_order), -1) FROM post_content WHERE post_id = ? AND content_type = ?', 
                    (id, 'image')
                ).fetchone()[0]
                
                display_order = max_order + 1
                
                for image in images:
                    if image.filename:
                        # Đảm bảo thư mục tồn tại
                        os.makedirs('flaskr/static/images', exist_ok=True)
                        # Tạo tên file duy nhất
                        filename = f"{id}_{display_order}_{image.filename}"
                        image_path = os.path.join('flaskr/static/images', filename)
                        image.save(image_path)
                        
                        # Lưu đường dẫn web
                        web_path = f"/static/images/{filename}"
                        
                        # Lưu thông tin hình ảnh vào bảng post_content
                        db.execute(
                            'INSERT INTO post_content (post_id, content_type, content, display_order)'
                            ' VALUES (?, ?, ?, ?)',
                            (id, 'image', web_path, display_order)
                        )
                        display_order += 1
            
            # Xử lý liên kết mới
            if links and any(link.strip() for link in links):
                # Lấy display_order lớn nhất hiện tại cho liên kết
                max_order = db.execute(
                    'SELECT COALESCE(MAX(display_order), -1) FROM post_content WHERE post_id = ? AND content_type = ?', 
                    (id, 'link')
                ).fetchone()[0]
                
                display_order = max_order + 1
                
                for link in links:
                    if link.strip():
                        # Đảm bảo link bắt đầu bằng http:// hoặc https://
                        if not link.startswith(('http://', 'https://')):
                            link = 'https://' + link
                        
                        # Lưu thông tin liên kết vào bảng post_content
                        db.execute(
                            'INSERT INTO post_content (post_id, content_type, content, display_order)'
                            ' VALUES (?, ?, ?, ?)',
                            (id, 'link', link, display_order)
                        )
                        display_order += 1
            
            db.commit()
            flash('Bài viết đã được cập nhật thành công')
            return redirect(url_for('blog.blog_index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_post(id):
    post = get_post(id)
    db = get_db()
    
    # Xóa nội dung đa phương tiện
    db.execute('DELETE FROM post_content WHERE post_id = ?', (id,))
    
    # Xóa bài viết
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    
    flash('Bài viết đã được xóa thành công')
    return redirect(url_for('blog.blog_index'))

@bp.route('/delete_multiple_posts', methods=('POST',))
@login_required
def delete_multiple_posts():
    post_ids = request.form.getlist('post_ids')
    
    if not post_ids:
        flash('Không có bài viết nào được chọn')
        return redirect(url_for('blog.blog_index'))
    
    db = get_db()
    
    # Kiểm tra quyền xóa
    for post_id in post_ids:
        post = db.execute('SELECT author_id FROM post WHERE id = ?', (post_id,)).fetchone()
        if post is None:
            continue
        
        # Nếu không phải admin và không phải tác giả, bỏ qua
        if not g.user['is_admin'] and post['author_id'] != g.user['id']:
            flash(f'Bạn không có quyền xóa bài viết có ID {post_id}')
            continue
        
        # Xóa nội dung đa phương tiện
        db.execute('DELETE FROM post_content WHERE post_id = ?', (post_id,))
        
        # Xóa bài viết
        db.execute('DELETE FROM post WHERE id = ?', (post_id,))
    
    db.commit()
    flash('Đã xóa các bài viết đã chọn')
    
    # Xác định trang để quay lại
    referer = request.referrer
    if 'admin_posts' in referer:
        return redirect(url_for('blog.admin_posts'))
    elif 'admin_my_posts' in referer:
        return redirect(url_for('blog.admin_my_posts'))
    elif 'my_posts' in referer:
        return redirect(url_for('blog.my_posts'))
    else:
        return redirect(url_for('blog.blog_index'))
