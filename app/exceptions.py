class AppError(Exception):
    """Base exception for the application"""
    pass

class ItemNotFoundError(AppError):
    """Item not found"""
    pass

# Aliases for different naming conventions used by tests
ItemNotFound = ItemNotFoundError

class InvalidCategoryError(AppError):
    """Invalid category"""
    pass

class ResourceNotFoundError(AppError):
    """Resource not found"""
    pass

class ValidationError(AppError):
    """Validation error"""
    pass

class DuplicateValueException(AppError):
    """Duplicate value"""
    pass

class CategoryAlreadyExists(AppError):
    """Category already exists"""
    pass

class CategoryNotExists(AppError):
    """Category does not exist"""
    pass

class CategoryNotFoundException(AppError):
    """Category not found"""
    pass

class ItemAlreadyExistsError(AppError):
    """Item already exists"""
    pass
