CREATE DATABASE gym_management;
USE gym_management;

CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL,
    name VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_member_id (member_id) -- Add this line for the index
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

select * from members;
select * from attendance;
