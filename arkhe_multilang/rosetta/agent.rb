class Agent
  attr_accessor :name, :counter
  def initialize(name)
    @name = name
    @counter = 0
  end
end

def send_message(sender, receiver)
  receiver.counter += 1
  puts "#{sender.name} -> #{receiver.name}: #{receiver.counter}"
end

alice = Agent.new("Alice")
bob = Agent.new("Bob")
send_message(alice, bob)
send_message(alice, bob)
