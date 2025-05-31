-- ================================
-- Database Schema for Blog Application
-- ================================

-- Removes existing tables if they exist
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS post_tags;
DROP TABLE IF EXISTS users;


-- ================================
-- Table: Posts
    -- Unique ID for each post
    -- Title of the post
    -- Description of the post
    -- Content of the post
    -- Publication date of the post
-- ================================

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    pub_date TEXT NOT NULL
);


-- ================================
-- Table: Comments
    -- Unique ID for each comment
    -- Foreign key to the related post
    -- Title of the comment
    -- Body of the comment
    -- Date when the comment was published
    -- Linking comment to post
-- ================================

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    pub_date TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);


-- ================================
-- Table: Tags
    -- Unique ID for each tag
    -- Tag name, which must be unique
-- ================================

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);


-- ================================
-- Table: Post-Tag Mapping (Many-to-Many)
    -- Foreign key to post and tags
    -- This table allows a post to have multiple tags and a tag to be associated with multiple posts
-- ================================

CREATE TABLE post_tags (
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);


-- ================================
-- Table: Users
    -- Unique ID for each user
    -- Username (must be unique)
    -- Hashed password
    -- Role of the user (User, Admin and so on)
-- ================================

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);