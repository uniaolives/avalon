class Agent(val name: String, var counter: Int = 0)

def sendMessage(sender: Agent, receiver: Agent): Unit = {
    receiver.counter += 1
    println(s"${sender.name} -> ${receiver.name}: ${receiver.counter}")
}

object Main extends App {
    val alice = new Agent("Alice")
    val bob = new Agent("Bob")
    sendMessage(alice, bob)
    sendMessage(alice, bob)
}
