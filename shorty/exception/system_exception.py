INVALID_BODY_MESSAGE = "Please provide a valid JSON body with 'url' and 'provider' parameters"
class SystemException(Exception):

    def __init__(self, status: int, code: str, message=INVALID_BODY_MESSAGE):
        super().__init__(status, code, message)
        self.status = status
        self.code = code
        self.message = message

    def get_status(self):
        return self.status

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message