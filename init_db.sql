USE aroma_alley_cafe;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE menu_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(5,2) NOT NULL
);

CREATE TABLE `order` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total DECIMAL(7,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES user(id)
);

INSERT INTO menu_item (name, price) VALUES
('Espresso', 3.50),
('Latte', 4.00),
('Croissant', 2.50);

INSERT INTO user (username, password_hash, is_admin) VALUES
('admin', 'sha256:600000$DHmD8tfZqW2jQ8TY$a82e071dfa9302c2b3a4c8975f1527f42c2fb543771e6076ae825c9dde03d68e', TRUE);  -- Hashed password
