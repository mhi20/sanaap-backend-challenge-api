class ServiceResult:
    def __init__(self, success: bool, data=None, errors=None, status_code=200):
        self.success = success
        self.data = data
        self.errors = errors
        self.status_code = status_code

    def get_error_messages(self) -> list[str]:
        messages = []

        if isinstance(self.errors, dict):
            for field, errors in self.errors.items():
                for err in errors:
                    messages.append(f"{field}: {str(err)}")
        elif isinstance(self.errors, list):
            for err in self.errors:
                messages.append(str(err))
        else:
            messages.append(str(self.errors))

        return messages
