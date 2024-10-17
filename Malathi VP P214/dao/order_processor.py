import pyodbc
from dao.i_order_management_repository import IOrderManagementRepository
from entity.Electronics import Electronics
from entity.Clothing import Clothing
from entity.Product import Product
from entity.User import User
from entity.Order import Order
from entity.OrderDetail import OrderDetail
from exception.exceptions import UserNotFoundException, OrderNotFoundException, ProductNotFoundException
from util.db_conn_util import DBConnUtil
from tabulate import tabulate

class OrderProcessor(IOrderManagementRepository):
    def __init__(self):
        self.connection = DBConnUtil.get_db_connection()

    def create_user(self, user: User):
        cursor = self.connection.cursor()
        try:
            # Check if the user ID already exists
            cursor.execute("SELECT * FROM Users WHERE userId = ?", (user.userId,))
            existing_user = cursor.fetchone()

            if existing_user:
                print(f"Error: User with ID {user.userId} already exists.")
                return

            # If user doesn't exist, proceed with insertion
            cursor.execute(
                "INSERT INTO Users (userId, username, password, role) VALUES (?, ?, ?, ?)",
                user.userId, user.username, user.password, user.role
            )
            self.connection.commit()
            print("User created successfully.")
        except Exception as e:
            print(f"Error while creating user: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def create_product(self, user: User, product: Product):
        # Check if the user is an Admin
        if user.role.lower() != 'admin':
            raise PermissionError("Only Admins can create products.")

        cursor = self.connection.cursor()
        try:
            # Check if the product ID already exists
            cursor.execute("SELECT * FROM Product WHERE productId = ?", (product.productId,))
            existing_product = cursor.fetchone()

            if existing_product:
                print(f"Error: Product with ID {product.productId} already exists.")
                return

            # If product doesn't exist, proceed with insertion
            cursor.execute(
                "INSERT INTO Product (productId, productName, description, price, quantityInStock, type) VALUES (?, ?, ?, ?, ?, ?)",
                (product.productId, product.productName, product.description, product.price, product.quantityInStock,
                 product.type)
            )

            # Insert into the specific table based on product type
            if isinstance(product, Electronics):  # Check if product is an instance of Electronics
                cursor.execute(
                    "INSERT INTO Electronics (productId, brand, warrantyPeriod) VALUES (?, ?, ?)",
                    (product.productId, product.brand, product.warrantyPeriod)
                )
            elif isinstance(product, Clothing):  # Check if product is an instance of Clothing
                cursor.execute(
                    "INSERT INTO Clothing (productId, size, color) VALUES (?, ?, ?)",
                    (product.productId, product.size, product.color)
                )

            self.connection.commit()
            print("Product created successfully.")
        except Exception as e:
            print(f"Error while creating product: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def create_order(self, user: User, products: list):
        cursor = self.connection.cursor()
        try:
            order_id = self.get_new_order_id()  # Generate a new unique order ID

            # Insert into Orders table
            cursor.execute(
                "INSERT INTO Orders (orderId, userId, orderDate) VALUES (?, ?, GETDATE())",
                (order_id, user.userId)
            )

            for product in products:
                # Fetch product details before adding to order
                product_cursor = self.connection.cursor()
                product_cursor.execute("SELECT * FROM Product WHERE productId = ?", (product.productId,))
                product_row = product_cursor.fetchone()

                if product_row is None:
                    raise ProductNotFoundException(f"Product with ID {product.productId} not found.")

                # Insert into OrderDetails table
                cursor.execute(
                    "INSERT INTO OrderDetails (orderDetailId, orderId, productId, quantity) VALUES (?, ?, ?, ?)",
                    (self.get_new_order_detail_id(), order_id, product.productId, product.quantityInStock)
                )

                product_cursor.close()

            # Commit the transaction
            self.connection.commit()
            print("Order created successfully.")
        except Exception as e:
            print(f"Error creating order: {e}")
            self.connection.rollback()  # Rollback in case of error
        finally:
            cursor.close()

    def cancel_order(self, userId: int, orderId: int):
        cursor = self.connection.cursor()
        try:
            # Check if the user exists
            cursor.execute("SELECT * FROM Users WHERE userId = ?", (userId,))
            user_row = cursor.fetchone()

            if user_row is None:  # User not found
                raise UserNotFoundException("User not found.")

            # First, delete the corresponding records from OrderDetails
            cursor.execute("DELETE FROM OrderDetails WHERE orderId = ?", (orderId,))

            # Now, delete the order from Orders
            cursor.execute("DELETE FROM Orders WHERE orderId = ? AND userId = ?", (orderId, userId))
            if cursor.rowcount == 0:  # No order found for the user
                raise OrderNotFoundException("Order not found for the specified user.")

            self.connection.commit()
            print("Order cancelled successfully.")
        except Exception as e:
            print(f"Error cancelling order: {e}")
            self.connection.rollback()  # Rollback in case of error
        finally:
            cursor.close()

    def get_all_products(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Product")
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_order_by_user(self, user: User):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT O.orderId, O.orderDate, OD.productId, P.productName, OD.quantity
                FROM Orders O
                JOIN OrderDetails OD ON O.orderId = OD.orderId
                JOIN Product P ON OD.productId = P.productId
                WHERE O.userId = ?
            """, (user.userId,))

            return cursor.fetchall()
        finally:
            cursor.close()

    def get_new_order_id(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT MAX(orderId) FROM Orders")
            max_id = cursor.fetchone()[0]
            return max_id + 1 if max_id is not None else 1  # Start from 1 if no orders exist
        finally:
            cursor.close()

    def get_new_order_detail_id(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT MAX(orderDetailId) FROM OrderDetails")
            max_detail_id = cursor.fetchone()[0]
            return max_detail_id + 1 if max_detail_id is not None else 1  # Start from 1 if no order details exist
        finally:
            cursor.close()
