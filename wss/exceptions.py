class NoSomethingsError(Exception):
    pass


class NoMessagesError(NoSomethingsError):
    pass


class NoClientEventsError(NoSomethingsError):
    pass
