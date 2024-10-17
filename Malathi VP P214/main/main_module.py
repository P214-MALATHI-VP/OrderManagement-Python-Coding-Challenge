from dao import order_processor
from dao.order_processor import OrderProcessor
from entity.Product import Product
from entity.User import User
from entity.Electronics import Electronics
from entity.Clothing import Clothing
from exception.exceptions import OrderNotFoundException, UserNotFoundException
from tabulate import tabulate

def main():
    processor = OrderProcessor()

    while True:
        print("\n1 - To Create User")
        print("2 - To Create Product")
        print("3 - To Create Order")
        print("4 - To Cancel Order")
        print("5 - To Get All Products")
        print("6 - To Get Orders by User")
        print("7 - To Exit")

        choice = int(input("Enter your choice: "))

# Initially there are 3 users in the database

        if choice == 1:
            try:
                # Collect user details
                userId = input("Enter user ID: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                role = input("Enter role(Admin/User): ")

                # Create a User object
                user = User(userId, username, password, role)

                # Call create_user method in OrderProcessor
                processor.create_user(user)

            except Exception as e:
                print(f"Error while processing user creation: {e}")

# Initially there are 3 products in the database

        elif choice == 2:

            userId = int(input("Enter Admin User ID: "))

            cursor = processor.connection.cursor()

            cursor.execute("SELECT * FROM Users WHERE userId = ?", (userId,))

            user_row = cursor.fetchone()

            if user_row is None:
                print("Admin user not found!")

                continue

            user = User(user_row[0], user_row[1], user_row[2], user_row[3])

            try:

                productId = int(input("Enter Product ID: "))

                productName = input("Enter Product Name: ")

                description = input("Enter Description: ")

                price = float(input("Enter Price: "))

                quantity = int(input("Enter Quantity in Stock: "))

                type = input("Enter Product Type (Electronics/Clothing): ")

                if type == 'Electronics':

                    brand = input("Enter Brand: ")

                    warrantyPeriod = int(input("Enter Warranty Period (months): "))  # Changed to warrantyPeriod

                    product = Electronics(productId, productName, description, price, quantity, type, brand,
                                          warrantyPeriod)


                elif type == 'Clothing':

                    size = input("Enter Size: ")

                    color = input("Enter Color: ")

                    product = Clothing(productId, productName, description, price, quantity, type, size, color)


                else:

                    print("Invalid product type!")

                    continue

                processor.create_product(user, product)


            except PermissionError as e:

                print(e)


            except Exception as e:

                print(f"An error occurred: {e}")

# Initially there are 3 orders in the database

        elif choice == 3:

            userId = int(input("Enter User ID: "))

            cursor = processor.connection.cursor()

            # Fetch the user details

            cursor.execute("SELECT userId, username, password, role FROM Users WHERE userId = ?", (userId,))

            user_row = cursor.fetchone()

            if user_row is None:  # Check if the user was found

                print("User not found!")

                continue

            # Create User object using fetched row

            user = User(user_row[0], user_row[1], user_row[2], user_row[3])

            products = []

            num_products = int(input("How many products to order? "))

            for _ in range(num_products):

                productId = int(input("Enter Product ID: "))

                quantity = int(input("Enter Quantity: "))

                # Fetch product details

                cursor.execute("SELECT * FROM Product WHERE productId = ?", (productId,))

                product_row = cursor.fetchone()

                if product_row is None:
                    print(f"Product with ID {productId} not found!")

                    continue

                # Create Product object with only productId and quantity (since only those are required)

                product = Product(productId, "", "", 0.0, quantity, "")

                products.append(product)

            # Call create_order with the User object and the list of products

            processor.create_order(user, products)

            cursor.close()

        elif choice == 4:

            userId = int(input("Enter User ID: "))

            orderId = int(input("Enter Order ID to cancel: "))

            try:

                processor.cancel_order(userId, orderId)

            except UserNotFoundException as e:

                print(e)

            except OrderNotFoundException as e:

                print(e)


        elif choice == 5:

            products = processor.get_all_products()

            if products:

                headers = ["Product ID", "Product Name", "Description", "Price", "Quantity in Stock", "Type"]

                print(tabulate(products, headers=headers, tablefmt="grid"))

            else:

                print("No products available.")


        elif choice == 6:

            userId = int(input("Enter User ID: "))

            cursor = processor.connection.cursor()

            cursor.execute("SELECT * FROM Users WHERE userId = ?", (userId,))

            user_row = cursor.fetchone()

            if user_row is None:  # Check if the user was found

                print("User not found!")

                continue

            # Create User object using fetched row

            user = User(user_row[0], user_row[1], user_row[2], user_row[3])

            orders = processor.get_order_by_user(user)

            print("Orders for User:")

            if not orders:

                print("No orders found for this user.")

            else:

                headers = ["Order ID", "Order Date", "Product ID", "Product Name", "Quantity"]

                print(tabulate(orders, headers=headers, tablefmt="grid"))


        elif choice == 7:
            print("!!! Thanks for using our service !!!")
            break


if __name__ == "__main__":
    main()