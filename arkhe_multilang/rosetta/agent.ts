class Agent {
    name: string;
    counter: number;
    constructor(name: string) {
        this.name = name;
        this.counter = 0;
    }
}

function sendMessage(sender: Agent, receiver: Agent): void {
    receiver.counter++;
    console.log(`${sender.name} -> ${receiver.name}: ${receiver.counter}`);
}

const alice = new Agent("Alice");
const bob = new Agent("Bob");
sendMessage(alice, bob);
sendMessage(alice, bob);
