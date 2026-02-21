#include <iostream>
#include <string>

struct Agent {
    std::string name;
    int counter = 0;
    Agent(const std::string& n) : name(n) {}
};

void sendMessage(const Agent& sender, Agent& receiver) {
    receiver.counter++;
    std::cout << sender.name << " -> " << receiver.name << ": " << receiver.counter << std::endl;
}

int main() {
    Agent alice("Alice");
    Agent bob("Bob");
    sendMessage(alice, bob);
    sendMessage(alice, bob);
    return 0;
}
