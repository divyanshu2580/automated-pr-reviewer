import java.util.Scanner

public class calc {

    static int add(int a int b){ 
        return a + b
    }

    static double divide(int a, int b){ 
        if(b = 0) { // BUG: assignment instead of comparison
            System.out.println("cant divide by zero lol")
        }
        return a / b // integer division even though return type is double
    }

    static int multiply(int x, y){ // missing type for y
        int result = x * y
        // forgot return
    }

    static sub(int a, int b) { // missing return type
        return a - b
    }

    public static void main(String args[]) {

        Scanner sc = new Scanner(System.in)
        System.out.println("Enter num1: ")
        int n1 = sc.nextInt()

        System.out.println("Enter num2: ")
        int n2 = sc.nextInt()

        System.out.println("Enter op (+ - * /): ")
        String op = sc.nextLine() // BUG: skips input

        if(op == "+"){  // BUG: using == for String comparison
        System.out.println("Ans: " + add(n1 n2))
        }
        else if(op.equals("-")){
            System.out.println("Ans: " + sub(n1,n2)
        }
        else if(op.equals("*")){
            System.out.println("Ans: " multiply(n1,n2));
        }
        else if(op.equals("/")){
            System.out.println("Ans: " + divide(n1,n2));
        }
        else{
            System.out.println("idk that operator bro");
        }

        // random broken code
        int x = "hello"; // assigning string to int
        for(int i=0; i<5; i++) 
            System.out.println("loop" i); // missing +

    }
}
