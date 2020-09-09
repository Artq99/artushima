CREATE TABLE campaign_timeline (
    id             INT UNSIGNED   AUTO_INCREMENT PRIMARY KEY,
    created_on     DATETIME       NOT NULL,
    modified_on    DATETIME       NOT NULL,
    opt_lock       INT UNSIGNED   NOT NULL,
    title          TINYTEXT       NOT NULL,
    session_date   DATE           NOT NULL,
    summary_text   TEXT,
    campaign_id    INT UNSIGNED   NOT NULL,

    FOREIGN KEY (campaign_id) REFERENCES campaign(id)
)