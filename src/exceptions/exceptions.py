class CustomError(Exception):
    """ CustomError to be aware it's from the implementation """
    pass


class DriveError(CustomError):
    """ Raised when there is an issue reading the drives from the mounted image """
    def __init__(self, message="An error occured when reading the drives from the mounted image."):
        self.message = message
        super().__init__(self.message)


class APIKeyVTError(CustomError):
    """Raised when the api key for Vt is missing """
    def __init__(self, message="There is no API key for VirusTotal, please make sure the api key exists."):
        self.message = message
        super().__init__(self.message)

    