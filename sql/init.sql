


CREATE TABLE region (
    pk INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    name VARCHAR(64) NOT NULL
);

CREATE TABLE city (
    pk INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    name VARCHAR(128) NOT NULL,
    district VARCHAR(128) NOT NULL,
    district_id INT NOT NULL,
    region_pk INT NOT NULL,
    CONSTRAINT fk_region
        FOREIGN KEY (region_pk)
        REFERENCES region(pk)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
