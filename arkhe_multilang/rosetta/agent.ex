defmodule Agent do
  defstruct name: "", counter: 0
end

defmodule Handover do
  def send_message(sender, receiver) do
    %{receiver | counter: receiver.counter + 1}
  end
end

alice = %Agent{name: "Alice"}
bob = %Agent{name: "Bob"}
bob = Handover.send_message(alice, bob)
IO.inspect(bob.counter)
