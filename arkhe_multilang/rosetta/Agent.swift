import Foundation

class Agent {
    let name: String
    var counter: Int = 0
    init(name: String) {
        self.name = name
    }
}

func sendMessage(sender: Agent, receiver: Agent) {
    receiver.counter += 1
    print("\(sender.name) -> \(receiver.name): \(receiver.counter)")
}

let alice = Agent(name: "Alice")
let bob = Agent(name: "Bob")
sendMessage(sender: alice, receiver: bob)
sendMessage(sender: alice, receiver: bob)
