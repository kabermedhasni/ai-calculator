import math
import datetime

class AdvancedCalculator:
    def __init__(self):
        self.memory = 0
        self.history = []
        self.ans = 0  # Store last answer

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y

    def power(self, x, y):
        return x ** y

    def square_root(self, x):
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)

    def factorial(self, x):
        if x < 0 or not float(x).is_integer():
            raise ValueError("Factorial only defined for non-negative integers")
        return math.factorial(int(x))

    def sin(self, x):
        return math.sin(math.radians(x))

    def cos(self, x):
        return math.cos(math.radians(x))

    def tan(self, x):
        return math.tan(math.radians(x))

    def log(self, x):
        if x <= 0:
            raise ValueError("Cannot calculate logarithm of non-positive number")
        return math.log10(x)

    def ln(self, x):
        if x <= 0:
            raise ValueError("Cannot calculate natural logarithm of non-positive number")
        return math.log(x)

    def add_to_memory(self):
        self.memory += self.ans

    def subtract_from_memory(self):
        self.memory -= self.ans

    def clear_memory(self):
        self.memory = 0

    def recall_memory(self):
        return self.memory

    def add_to_history(self, operation, inputs, result):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            'timestamp': timestamp,
            'operation': operation,
            'inputs': inputs,
            'result': result
        })

    def show_history(self):
        if not self.history:
            print("\nNo calculations in history.")
            return
        
        print("\nCalculation History:")
        for entry in self.history[-5:]:  # Show last 5 entries
            print(f"[{entry['timestamp']}] {entry['operation']}: {entry['inputs']} = {entry['result']}")

def calculator():
    calc = AdvancedCalculator()
    
    while True:
        print("\nAdvanced Calculator")
        print("Basic Operations:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("\nAdvanced Operations:")
        print("5. Power")
        print("6. Square Root")
        print("7. Factorial")
        print("8. Sin (degrees)")
        print("9. Cos (degrees)")
        print("10. Tan (degrees)")
        print("11. Log (base 10)")
        print("12. Natural Log")
        print("\nMemory Operations:")
        print("13. Add to Memory (M+)")
        print("14. Subtract from Memory (M-)")
        print("15. Recall Memory (MR)")
        print("16. Clear Memory (MC)")
        print("\nOther Operations:")
        print("17. Show History")
        print("18. Use Previous Answer (ANS)")
        print("19. Exit")

        try:
            choice = input("\nEnter choice (1-19): ")

            if choice == '19':
                print("Thank you for using the advanced calculator!")
                break

            # Memory operations
            if choice in ['13', '14', '15', '16']:
                if choice == '13':
                    calc.add_to_memory()
                    print(f"Added {calc.ans} to memory")
                elif choice == '14':
                    calc.subtract_from_memory()
                    print(f"Subtracted {calc.ans} from memory")
                elif choice == '15':
                    print(f"Memory value: {calc.recall_memory()}")
                elif choice == '16':
                    calc.clear_memory()
                    print("Memory cleared")
                continue

            # History
            if choice == '17':
                calc.show_history()
                continue

            # Previous answer
            if choice == '18':
                print(f"Previous answer: {calc.ans}")
                continue

            # Single operand operations
            if choice in ['6', '7', '8', '9', '10', '11', '12']:
                try:
                    if calc.ans != 0 and input("Use previous answer? (y/n): ").lower() == 'y':
                        x = calc.ans
                    else:
                        x = float(input("Enter number: "))

                    if choice == '6':
                        result = calc.square_root(x)
                        operation = "√"
                        inputs = f"{x}"
                    elif choice == '7':
                        result = calc.factorial(x)
                        operation = "factorial"
                        inputs = f"{x}"
                    elif choice == '8':
                        result = calc.sin(x)
                        operation = "sin"
                        inputs = f"{x}°"
                    elif choice == '9':
                        result = calc.cos(x)
                        operation = "cos"
                        inputs = f"{x}°"
                    elif choice == '10':
                        result = calc.tan(x)
                        operation = "tan"
                        inputs = f"{x}°"
                    elif choice == '11':
                        result = calc.log(x)
                        operation = "log"
                        inputs = f"{x}"
                    elif choice == '12':
                        result = calc.ln(x)
                        operation = "ln"
                        inputs = f"{x}"

                except ValueError as e:
                    print(f"Error: {str(e)}")
                    continue

            # Double operand operations
            else:
                try:
                    if calc.ans != 0 and input("Use previous answer as first number? (y/n): ").lower() == 'y':
                        num1 = calc.ans
                    else:
                        num1 = float(input("Enter first number: "))
                    
                    num2 = float(input("Enter second number: "))

                    if choice == '1':
                        result = calc.add(num1, num2)
                        operation = "+"
                    elif choice == '2':
                        result = calc.subtract(num1, num2)
                        operation = "-"
                    elif choice == '3':
                        result = calc.multiply(num1, num2)
                        operation = "*"
                    elif choice == '4':
                        result = calc.divide(num1, num2)
                        operation = "/"
                    elif choice == '5':
                        result = calc.power(num1, num2)
                        operation = "^"
                    
                    inputs = f"{num1} {operation} {num2}"

                except ValueError as e:
                    print(f"Error: {str(e)}")
                    continue

            calc.ans = result
            calc.add_to_history(operation, inputs, result)
            print(f"Result: {result}")

        except ValueError:
            print("Invalid input! Please try again.")
            continue

if __name__ == "__main__":
    calculator()
