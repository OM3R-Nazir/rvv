class BasicRVVClass:
    def __init__(self):
        self.features = []

    def execute(self):
        return "Executing basic RVV functionality."

class RVVExtension:
    def __init__(self, rvv):
        self.rvv = rvv  # Store the base RVV object
        self.add_extension()

    def add_extension(self):
        self.rvv.features.append(self.__class__.__name__)

        # Dynamically bind all methods of the extension to the base object
        for attr_name in dir(self):
            if not attr_name.startswith("__") and callable(getattr(self, attr_name)):
                method = getattr(self, attr_name)
                setattr(self.rvv, attr_name, method)

# Example: Extension that adds a multiply function
class MultiplyExtension(RVVExtension):
    def add_extension(self):
        super().add_extension()

    def multiply(self, a, b):
        return a * b

# Example: Extension that adds a division function
class DivisionExtension(RVVExtension):
    def add_extension(self):
        super().add_extension()

    def divide(self, a, b):
        if b == 0:
            return "Error: Division by zero"
        return a / b

# Usage
rvv = BasicRVVClass()
print(rvv.execute())  # Output: Executing basic RVV functionality.

# Add Multiply Extension
rvv = MultiplyExtension(rvv).rvv
print(rvv.features)  # Output: ['MultiplyExtension']
print(rvv.multiply(4, 5))  # Output: 20

# Add Division Extension
rvv = DivisionExtension(rvv).rvv
print(rvv.features)  # Output: ['MultiplyExtension', 'DivisionExtension']
print(rvv.divide(10, 2))  # Output: 5.0
print(rvv.multiply(3, 7))  # Output: 21
