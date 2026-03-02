public class Agent {
    String name;
    int counter;

    public Agent(String name) {
        this.name = name;
        this.counter = 0;
    }

    public static void sendMessage(Agent sender, Agent receiver) {
        receiver.counter++;
        System.out.println(sender.name + " -> " + receiver.name + ": " + receiver.counter);
    }

    public static void main(String[] args) {
        Agent alice = new Agent("Alice");
        Agent bob = new Agent("Bob");
        sendMessage(alice, bob);
        sendMessage(alice, bob);
    }
}
