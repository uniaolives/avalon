Agent = {name = "", counter = 0}
function Agent:new(name)
    local obj = {name = name, counter = 0}
    setmetatable(obj, self)
    self.__index = self
    return obj
end

function sendMessage(sender, receiver)
    receiver.counter = receiver.counter + 1
    print(sender.name .. " -> " .. receiver.name .. ": " .. receiver.counter)
end

local alice = Agent:new("Alice")
local bob = Agent:new("Bob")
sendMessage(alice, bob)
sendMessage(alice, bob)
