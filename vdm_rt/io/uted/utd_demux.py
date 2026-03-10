class UTDDemux:
    def __init__(self):
        self.handlers = {}

    def register(self, port: str, fn):
        self.handlers[port] = fn

    def dispatch(self, frame):
        fn = self.handlers.get(frame.port)
        if fn is not None:
            fn(frame)
