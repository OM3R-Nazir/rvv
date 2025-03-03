class RVVExtension:
    def __init__(self, rvv):
        self.rvv = rvv  # Store the base RVV object
        self.add_extension()

    def add_extension(self):
        self.rvv._extensions.append(self.__class__.__name__)

        # Dynamically bind all methods of the extension to the base object
        for attr_name in dir(self):
            if not attr_name.startswith("__") and callable(getattr(self, attr_name)):
                method = getattr(self, attr_name)
                setattr(self.rvv, attr_name, method)