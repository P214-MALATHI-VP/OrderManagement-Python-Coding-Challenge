class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

class OrderNotFoundException(Exception):
    """Exception raised when an order is not found in the database."""
    def __init__(self, message="Order not found"):
        self.message = message
        super().__init__(self.message)

class ProductNotFoundException(Exception):
    """Exception raised when a product is not found in the database."""
    def __init__(self, message="Product not found"):
        self.message = message
        super().__init__(self.message)
