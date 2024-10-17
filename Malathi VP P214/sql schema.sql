--Creating database

CREATE DATABASE OrderManagement;

USE OrderManagement;

--Creating tables and inserting values

-- Create Product Table
CREATE TABLE Product (
    productId INT PRIMARY KEY,
    productName VARCHAR(100),
    description VARCHAR(255),
    price DECIMAL(10, 2),
    quantityInStock INT,
    type VARCHAR(20) CHECK (type IN ('Electronics', 'Clothing'))
);

-- Insert 3 records into Product table
INSERT INTO Product (productId, productName, description, price, quantityInStock, type)
VALUES
(1, 'Laptop', 'High-performance laptop for gaming', 1299.99, 30, 'Electronics'),
(2, 'Smartphone', 'Latest model with AI features', 699.99, 50, 'Electronics'),
(3, 'Shirt', '100% cotton, comfortable wear', 19.99, 100, 'Clothing');

-- Create Electronics Table
CREATE TABLE Electronics (
    productId INT,
    brand VARCHAR(100),
    warrantyPeriod INT,
	FOREIGN KEY(productId) REFERENCES Product(productId)
);

-- Insert 3 records into Electronics table
INSERT INTO Electronics (productId, brand, warrantyPeriod)
VALUES
(1, 'BrandX', 24),
(2, 'BrandY', 12);

-- Create Clothing Table
CREATE TABLE Clothing (
    productId INT,
    size VARCHAR(10),
    color VARCHAR(20),
	FOREIGN KEY(productId) REFERENCES Product(productId)
);

-- Insert 3 records into Clothing table
INSERT INTO Clothing (productId, size, color)
VALUES
(3, 'M', 'Blue');

-- Create Users Table
CREATE TABLE Users (
    userId INT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(10) CHECK (role IN ('Admin', 'User'))
);

-- Insert 3 records into Users table
INSERT INTO Users (userId, username, password, role) 
VALUES 
(1, 'admin1', 'adminPass', 'Admin'),
(2, 'user1', 'userPass1', 'User'),
(3, 'user2', 'userPass2', 'User');

-- Create Orders Table
CREATE TABLE Orders (
    orderId INT PRIMARY KEY,
    userId INT,
    orderDate DATE,
	FOREIGN KEY(userId) REFERENCES Users(userId)
);

-- Insert 3 records into Orders table
INSERT INTO Orders (orderId, userId, orderDate)
VALUES
(1, 2, '2024-10-10'),
(2, 2, '2024-10-11'),
(3, 3, '2024-10-12');

-- Create OrderDetails Table
CREATE TABLE OrderDetails (
    orderDetailId INT PRIMARY KEY,
    orderId INT,
    productId INT,
    quantity INT,
	FOREIGN KEY(orderId) REFERENCES Orders(orderId),
	FOREIGN KEY(productId) REFERENCES Product(productId)
);

-- Insert 3 records into OrderDetails table
INSERT INTO OrderDetails (orderDetailId, orderId, productId, quantity)
VALUES
(1, 1, 1, 2),
(2, 2, 2, 1),
(3, 3, 3, 5);


select * from Product;
select * from Electronics;
select * from Clothing;
select * from Users;
select * from Orders;
select * from OrderDetails;
