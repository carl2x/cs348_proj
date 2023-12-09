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

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);

CREATE TABLE reports (
    id int NOT NULL AUTO_INCREMENT,
    total_todos int,
    total_completed int,
    total_in_progress int,
    completion_rate float,
    avg_duration float,
    priority char(30),
    PRIMARY KEY (id)
);

Select * from tasks;