CREATE TABLE campaign_history (
    id            INT UNSIGNED   AUTO_INCREMENT PRIMARY KEY,
    created_on    DATETIME       NOT NULL,
    modified_on   DATETIME       NOT NULL,
    opt_lock      INT UNSIGNED   NOT NULL,
    editor_name   VARCHAR(255)   NOT NULL,
    message       VARCHAR(255)   NOT NULL,
    campaign_id   INT UNSIGNED   NOT NULL,

    FOREIGN KEY (campaign_id) REFERENCES campaign(id)
)