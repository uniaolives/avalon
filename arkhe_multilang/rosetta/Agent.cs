using System;

class Agent {
    public string Name { get; set; }
    public int Counter { get; set; }
    public Agent(string name) {
        Name = name;
        Counter = 0;
    }
}

class Program {
    static void SendMessage(Agent sender, Agent receiver) {
        receiver.Counter++;
        Console.WriteLine($"{sender.Name} -> {receiver.Name}: {receiver.Counter}");
    }

    static void Main() {
        Agent alice = new Agent("Alice");
        Agent bob = new Agent("Bob");
        SendMessage(alice, bob);
        SendMessage(alice, bob);
    }
}
