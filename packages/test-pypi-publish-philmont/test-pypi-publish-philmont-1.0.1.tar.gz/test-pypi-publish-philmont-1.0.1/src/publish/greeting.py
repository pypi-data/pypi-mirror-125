from publish import Configuration


class Setup:
    def __init__(self, configuration: Configuration, message: str):
        self.users_name = configuration.users_name
        self.message = message

    def say_hello(self):
        print(f'{self.message}, {self.users_name}')

