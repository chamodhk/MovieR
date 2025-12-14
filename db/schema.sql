CREATE database MOVIER;
USE MOVIER;

CREATE TABLE movies (
parent_id VARCHAR(15) NOT NULL,
movie_name VARCHAR(50),
primary key(parent_id, movie_name));


PRIMARYCREATE INDEX idx_parent ON movies(parent_id);

