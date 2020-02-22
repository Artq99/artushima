CREATE TABLE `user` (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    created_on DATETIME NOT NULL,
    modified_on DATETIME NOT NULL,
    opt_lock INT UNSIGNED NOT NULL,
    password_hash VARCHAR(255),
	user_name VARCHAR(255) NOT NULL,
    CONSTRAINT u_user_user_name UNIQUE (user_name)
);
