DROP DATABASE IF EXISTS todo;
CREATE DATABASE todo;
USE todo;
CREATE TABLE tasks (
    id int NOT NULL AUTO_INCREMENT,
    task varchar(255) NOT NULL,
    status char(30),
    priority char(30),
    duration int,
    PRIMARY KEY (id)
);
INSERT INTO tasks (task, status, priority, duration) 
VALUES ("task no.1", "Todo", "High", 120);
Select * from tasks;