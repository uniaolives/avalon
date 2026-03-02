CREATE TABLE agents (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    counter INT DEFAULT 0
);

CREATE TABLE handovers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT,
    receiver_id INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES agents(id),
    FOREIGN KEY (receiver_id) REFERENCES agents(id)
);

-- Simulate a handover:
UPDATE agents SET counter = counter + 1 WHERE id = 2;  -- Bob
INSERT INTO handovers (sender_id, receiver_id) VALUES (1, 2);
