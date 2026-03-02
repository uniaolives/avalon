data class Agent(val name: String, var counter: Int = 0)

fun sendMessage(sender: Agent, receiver: Agent) {
    receiver.counter++
    println("${sender.name} -> ${receiver.name}: ${receiver.counter}")
}

fun main() {
    val alice = Agent("Alice")
    val bob = Agent("Bob")
    sendMessage(alice, bob)
    sendMessage(alice, bob)
}
