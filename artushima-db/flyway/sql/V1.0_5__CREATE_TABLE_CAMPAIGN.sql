CREATE TABLE campaign (
    id               INT UNSIGNED    AUTO_INCREMENT PRIMARY KEY,
    created_on       DATETIME        NOT NULL,
    modified_on      DATETIME        NOT NULL,
    opt_lock         INT UNSIGNED    NOT NULL,
    campaign_name    VARCHAR(255)    NOT NULL,
    begin_date       DATE            NOT NULL,
    passed_days      INT UNSIGNED    NOT NULL,
    game_master_id   INT UNSIGNED    NOT NULL,

    FOREIGN KEY (game_master_id) REFERENCES user(id)
);
