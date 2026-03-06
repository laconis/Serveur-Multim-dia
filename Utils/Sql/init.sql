CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    hash_sha256 VARCHAR(64) NULL,
    cover_path VARCHAR(500) NULL,
    size_bytes BIGINT NOT NULL,
    duration_sec INT NOT NULL,
    resolution VARCHAR(50) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    is_published TINYINT(1) NOT NULL DEFAULT 1,
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    views BIGINT NOT NULL DEFAULT 0,
    category_id INT NOT NULL,
    uploaded_by VARCHAR(100) NULL,
    CONSTRAINT fk_videos_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
);
