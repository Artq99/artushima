"""
The module containing constants for the error messages.
"""

# related to properties
ON_PROPERTY_MISSING: str = "The property '{}' not present."
ON_INVALID_PROPERTY_VALUE: str = "The value of the property '{}' is invalid."

# related to DAOs
ON_READING_DATA: str = "Error on reading data."
ON_PERSISTING_DATA: str = "Error on persisting data."

# related to argument validation
ON_NONE_ARGUMENT: str = "The argument '{}' cannot be None."
ON_INVALID_ARGUMENT: str = "The argument '{}' is invalid."

# related to authentication
ON_EXPIRED_SIGNATURE: str = "Authentication token signature has expired."
ON_INVALID_TOKEN: str = "The token is invalid."
