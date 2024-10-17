class DBPropertyUtil:
    @staticmethod
    def get_connection_string():
        server = "DESKTOP-44FIQAE\\SQLEXPRESS"
        database = "OrderManagement"

        connection_string = (
            f'DRIVER={{SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;'
            f'MARS_Connection=True;'
        )
        return connection_string

