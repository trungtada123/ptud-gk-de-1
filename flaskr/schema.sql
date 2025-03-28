DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS post_content;
DROP TABLE IF EXISTS post_followers;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  is_blocked BOOLEAN NOT NULL DEFAULT 0,
  is_admin BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  text_content TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE post_content (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER NOT NULL,
  content_type TEXT NOT NULL,  -- 'image' hoặc 'link'
  content TEXT NOT NULL,       -- đường dẫn hình ảnh hoặc URL
  display_order INTEGER NOT NULL,
  FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE
);

CREATE TABLE post_followers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE,
  UNIQUE(user_id, post_id)
);