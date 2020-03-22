


CREATE TABLE region (
    pk INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    name VARCHAR(64) NOT NULL
);

-- CREATE TABLE district (
--     pk INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     id INT NOT NULL,
--     name VARCHAR(64) NOT NULL,
--     region_id INT NOT NULL
-- );

CREATE TABLE city (
    pk INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    name VARCHAR(128) NOT NULL,
    region_id INT NOT NULL,
    district_id INT NOT NULL
);

CREATE TABLE street (
    pk INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    name VARCHAR(128) NOT NULL,
    region_id INT NOT NULL,
    district_id INT NOT NULL,
    city_id INT NOT NULL,
    city_part_id INT NOT NULL
);

CREATE TABLE address (
    pk INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    name VARCHAR(128) NOT NULL,
    region_id INT NOT NULL,
    district_id INT NOT NULL,
    city_id INT NOT NULL,
    city_part_id INT NOT NULL,
    street_id INT DEFAULT NULL
)
