CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

INSERT INTO users (name, email, hashed_password) VALUES 
('John Doe', 'john@example.com', 'hashedpassword123'),
('Jane Doe', 'jane@example.com', 'hashedpassword456');
