CREATE TABLE user_role (
	  id            INT UNSIGNED   AUTO_INCREMENT PRIMARY KEY,
    created_on    DATETIME       NOT NULL,
    modified_on   DATETIME       NOT NULL,
    opt_lock      INT UNSIGNED   NOT NULL,
    user_id       INT UNSIGNED   NOT NULL,
    role_name     VARCHAR(255)   NOT NULL,

		FOREIGN KEY (user_id) REFERENCES user(id)
);
