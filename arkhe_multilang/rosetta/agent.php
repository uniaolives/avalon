<?php

class Agent {
    public $name;
    public $counter = 0;
    function __construct($name) {
        $this->name = $name;
    }
}

function sendMessage($sender, $receiver) {
    $receiver->counter++;
    echo $sender->name . " -> " . $receiver->name . ": " . $receiver->counter . "\n";
}

$alice = new Agent("Alice");
$bob = new Agent("Bob");
sendMessage($alice, $bob);
sendMessage($alice, $bob);
?>
