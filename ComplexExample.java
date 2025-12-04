
public class ComplexExample {

    // Nested class
    static class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    // Generic method
    public static <T> void printArray(T[] array) {
        for (T element : array) {
            System.out.println(element);
        }
    }

    // Recursive function
    public static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    // Linked List utility
    public static Node buildLinkedList(int... values) {
        Node head = null;
        Node current = null;
        for (int v : values) {
            if (head == null) {
                head = new Node(v);
                current = head;
            } else {
                current.next = new Node(v);
                current = current.next;
            }
        }
        return head;
    }

    // Multi-threading example
    static class Worker extends Thread {
        private final int id;
        Worker(int id) { this.id = id; }

        @Override
        public void run() {
            System.out.println("Thread " + id + " starting work...");
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                System.out.println("Interrupted!");
            }
            System.out.println("Thread " + id + " finished work.");
        }
    }

    // Main method
    public static void main(String[] args) {
        System.out.println("Factorial of 5 = " + factorial(5));

        String[] items = { "apple", "banana", "carrot" };
        printArray(items);

        Node list = buildLinkedList(1, 2, 3, 4, 5);
        System.out.println("Linked list created.");

        // Start multiple threads
        for (int i = 1; i <= 3; i++) {
            new Worker(i).start();
        }
    }
}
