package main

import "fmt"

type Agent struct {
    Name    string
    Counter int
}

func sendMessage(sender Agent, receiver *Agent) {
    receiver.Counter++
    fmt.Printf("%s -> %s: %d\n", sender.Name, receiver.Name, receiver.Counter)
}

func main() {
    alice := Agent{Name: "Alice"}
    bob := &Agent{Name: "Bob"}
    sendMessage(alice, bob)
    sendMessage(alice, bob)
}
