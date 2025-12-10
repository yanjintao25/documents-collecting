-- SQLite 数据库建表脚本
-- 注意：SQLite 使用文件数据库，不需要 CREATE DATABASE 语句
-- 使用方式：sqlite3 documents_collecting.db < creatSql.sql

-- 启用外键约束
PRAGMA foreign_keys = ON;

-- 文章表
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 文章ID，主键
    title VARCHAR(255) NOT NULL,  -- 文章标题
    save_path VARCHAR(500) NOT NULL,  -- 文章内容保存路径
    pdf_save_path VARCHAR(500) DEFAULT NULL,  -- PDF文件保存路径
    introduction TEXT,  -- 文章简介
    write_time TEXT DEFAULT NULL,  -- 写作时间（SQLite 使用 TEXT 存储日期时间）
    create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 更新时间（通过触发器自动更新）
    status INTEGER NOT NULL DEFAULT 1,  -- 状态：0-草稿，1-已发布，2-隐藏
    upload_user_name VARCHAR(100) NOT NULL,  -- 上传用户
    upload_user_id VARCHAR(100) NOT NULL,  -- 上传用户ID
    update_user_name VARCHAR(100) DEFAULT NULL,  -- 最后更新用户
    update_user_id VARCHAR(100) DEFAULT NULL,  -- 最后更新用户ID
    category_id INTEGER DEFAULT NULL,  -- 分类ID
    category_name VARCHAR(100) DEFAULT NULL,  -- 分类名称
    delete_flag INTEGER NOT NULL DEFAULT 0  -- 删除标志：0-未删除，1-已删除
);

-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 用户ID，主键
    username VARCHAR(50) NOT NULL,  -- 用户名
    password VARCHAR(255) NOT NULL,  -- 密码（加密存储）
    email VARCHAR(100) NOT NULL,  -- 邮箱
    phone VARCHAR(20) DEFAULT NULL,  -- 手机号
    create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 更新时间（通过触发器自动更新）
    status INTEGER NOT NULL DEFAULT 1,  -- 状态：0-禁用，1-正常，2-未激活
    delete_flag INTEGER NOT NULL DEFAULT 0  -- 删除标志：0-未删除，1-已删除
);

-- 分类表
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 分类ID，主键
    name VARCHAR(100) NOT NULL,  -- 分类名称
    create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 更新时间（通过触发器自动更新）
    status INTEGER NOT NULL DEFAULT 1,  -- 状态：0-禁用，1-启用
    delete_flag INTEGER NOT NULL DEFAULT 0,  -- 删除标志：0-未删除，1-已删除
    UNIQUE (name, delete_flag)  -- 分类名称唯一索引（考虑删除状态）
);

-- 标签表
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 标签ID，主键
    name VARCHAR(50) NOT NULL,  -- 标签名称
    create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 更新时间（通过触发器自动更新）
    status INTEGER NOT NULL DEFAULT 1,  -- 状态：0-禁用，1-启用
    color VARCHAR(20) DEFAULT '#3B82F6',  -- 颜色标记，默认蓝色(#3B82F6)
    delete_flag INTEGER NOT NULL DEFAULT 0,  -- 删除标志：0-未删除，1-已删除
    UNIQUE (name, delete_flag)  -- 标签名称唯一索引（考虑删除状态）
);

-- 文章和标签的关联表
CREATE TABLE article_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 关联ID
    article_id INTEGER NOT NULL,  -- 文章ID
    tag_id INTEGER NOT NULL,  -- 标签ID
    create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    UNIQUE (article_id, tag_id),  -- 文章和标签组合唯一
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- ==================== 索引 ====================

-- 文章表索引
CREATE INDEX idx_articles_status ON articles(status);
CREATE INDEX idx_articles_category_id ON articles(category_id);
CREATE INDEX idx_articles_delete_flag ON articles(delete_flag);
CREATE INDEX idx_articles_create_time ON articles(create_time);
CREATE INDEX idx_articles_update_time ON articles(update_time);

-- 用户表索引
CREATE UNIQUE INDEX uk_users_phone ON users(phone) WHERE phone IS NOT NULL;  -- 手机号唯一索引（忽略 NULL）
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_delete_flag ON users(delete_flag);
CREATE INDEX idx_users_create_time ON users(create_time);
CREATE INDEX idx_users_update_time ON users(update_time);

-- 分类表索引
CREATE INDEX idx_categories_status ON categories(status);
CREATE INDEX idx_categories_delete_flag ON categories(delete_flag);
CREATE INDEX idx_categories_create_time ON categories(create_time);
CREATE INDEX idx_categories_update_time ON categories(update_time);

-- 标签表索引
CREATE INDEX idx_tags_status ON tags(status);
CREATE INDEX idx_tags_delete_flag ON tags(delete_flag);
CREATE INDEX idx_tags_color ON tags(color);
CREATE INDEX idx_tags_create_time ON tags(create_time);
CREATE INDEX idx_tags_update_time ON tags(update_time);

-- 文章-标签关联表索引
CREATE INDEX idx_article_tags_article_id ON article_tags(article_id);
CREATE INDEX idx_article_tags_tag_id ON article_tags(tag_id);

-- ==================== 触发器：自动更新 update_time ====================

-- 文章表更新触发器
CREATE TRIGGER update_articles_timestamp 
AFTER UPDATE ON articles
FOR EACH ROW
WHEN NEW.update_time = OLD.update_time
BEGIN
    UPDATE articles SET update_time = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- 用户表更新触发器
CREATE TRIGGER update_users_timestamp 
AFTER UPDATE ON users
FOR EACH ROW
WHEN NEW.update_time = OLD.update_time
BEGIN
    UPDATE users SET update_time = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- 分类表更新触发器
CREATE TRIGGER update_categories_timestamp 
AFTER UPDATE ON categories
FOR EACH ROW
WHEN NEW.update_time = OLD.update_time
BEGIN
    UPDATE categories SET update_time = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- 标签表更新触发器
CREATE TRIGGER update_tags_timestamp 
AFTER UPDATE ON tags
FOR EACH ROW
WHEN NEW.update_time = OLD.update_time
BEGIN
    UPDATE tags SET update_time = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;