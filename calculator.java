import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

// -----------------------------
// Operation Interface
// -----------------------------
interface Operation {
    double execute(double a, double b);
}

// -----------------------------
// Basic Operations
// -----------------------------
class Add implements Operation {
    public double execute(double a, double b) { return a + b; }
}

class Subtract implements Operation {
    public double execute(double a, double b) { return a - b; }
}

class Multiply implements Operation {
    public double execute(double a, double b) { return a * b; }
}

class Divide implements Operation {
    public double execute(double a, double b) {
        if (b == 0) throw new ArithmeticException("Division by zero is not allowed.");
        return a / b;
    }
}

// -----------------------------
// Scientific Operations
// -----------------------------
class Power implements Operation {
    public double execute(double a, double b) { return Math.pow(a, b); }
}

class Modulus implements Operation {
    public double execute(double a, double b) { return a % b; }
}

// -----------------------------
// Calculator Engine
// -----------------------------
class Calculator {
    private final Map<String, Operation> operations = new HashMap<>();

    public Calculator() {
        // Registering operations
        operations.put("+", new Add());
        operations.put("-", new Subtract());
        operations.put("*", new Multiply());
        operations.put("/", new Divide());
        operations.put("^", new Power());
        operations.put("%", new Modulus());
    }

    public double calculate(double a, double b, String op) {
        Operation operation = operations.get(op);
        if (operation == null) {
            throw new IllegalArgumentException("Unsupported operator: " + op);
        }
        return operation.execute(a, b);
    }

    public void showSupportedOps() {
        System.out.println("Supported operators: " + operations.keySet());
    }
}

// -----------------------------
// Main Program
// -----------------------------
public class AdvancedCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Calculator calc = new Calculator();

        System.out.println("===== Advanced Java Calculator =====");
        calc.showSupportedOps();

        try {
            System.out.print("Enter first number: ");
            double num1 = Double.parseDouble(scanner.nextLine());

            System.out.print("Enter operator: ");
            String op = scanner.nextLine();

            System.out.print("Enter second number: ");
            double num2 = Double.parseDouble(scanner.nextLine());

            double result = calc.calculate(num1, num2, op);
            System.out.println("Result: " + result);

        } catch (NumberFormatException e) {
            System.out.println("Invalid number entered.");
        } catch (ArithmeticException e) {
            System.out.println("Math error: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Unexpected error: " + e.getMessage());
        }

        scanner.close();
    }
}
