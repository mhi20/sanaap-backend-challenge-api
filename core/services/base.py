import traceback

class BaseServiceObject:
    def __init__(self):
        self.errors = []

    def add_error(self, message):
        if not isinstance(message, str):
            message = str(message)
        self.errors.append(message)

    def add_errors(self, messages):
        self.errors.extend(messages)

    @property
    def is_valid(self):
        return len(self.errors) == 0

    def service_step(fn):
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            except Exception as e:
                if isinstance(e, (SystemExit, KeyboardInterrupt)):
                    raise

                error_message = f'{self.__class__.__name__}: {e} - description: {traceback.format_exc()}'
                self.add_error(error_message)
        return wrapper