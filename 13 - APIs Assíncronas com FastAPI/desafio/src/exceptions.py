class AccountNotFoundError(Exception):
    
    def __init__(self, message: str = "Account not found"):
        super().__init__(message)
        self.message = message


class BusinessError(Exception):
    
    def __init__(self, message: str = "Business rule violation"):
        super().__init__(message)
        self.message = message
