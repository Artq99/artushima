CREATE TABLE `user` (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    created_on DATETIME NOT NULL,
    modified_on DATETIME NOT NULL,
    opt_lock INT UNSIGNED NOT NULL,
    password_hash VARCHAR(255),
	user_name VARCHAR(255) NOT NULL
);

CREATE TABLE user_history (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    created_on DATETIME NOT NULL,
    modified_on DATETIME NOT NULL,
    opt_lock INT UNSIGNED NOT NULL,
    editor_name VARCHAR(255) NOT NULL,
    message VARCHAR(255) NOT NULL,
    user_id INT UNSIGNED NOT NULL,
    CONSTRAINT fk_user_history_user_id
		FOREIGN KEY (user_id)
        REFERENCES `user`(id)
);

CREATE TABLE user_role (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    created_on DATETIME NOT NULL,
    modified_on DATETIME NOT NULL,
    opt_lock INT UNSIGNED NOT NULL,
    user_id INT UNSIGNED NOT NULL,
    role_name VARCHAR(255) NOT NULL,
    CONSTRAINT fk_user_role_user_id
		FOREIGN KEY (user_id)
        REFERENCES `user`(id)
);

INSERT INTO db_version (version) VALUES ('0001 - V1.0 CREATE TABLES');
