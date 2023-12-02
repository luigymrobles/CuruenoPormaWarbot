
class PersonNotFound(Exception):
    """Exception raised whenever the PersonManager
     could not find a Person."""
    def __init__(self, message):
        message = "Person:%s not found" % message
        super().__init__(message)
