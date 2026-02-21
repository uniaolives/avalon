// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AgentProtocol {
    struct Agent {
        string name;
        uint256 counter;
    }

    mapping(address => Agent) public agents;

    event Handover(address indexed from, address indexed to, uint256 newCounter);

    function register(string memory _name) public {
        agents[msg.sender] = Agent(_name, 0);
    }

    function sendMessage(address to) public {
        agents[to].counter++;
        emit Handover(msg.sender, to, agents[to].counter);
    }
}
