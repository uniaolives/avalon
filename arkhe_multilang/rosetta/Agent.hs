data Agent = Agent { name :: String, counter :: Int } deriving (Show)

sendMessage :: Agent -> Agent -> Agent
sendMessage sender receiver = receiver { counter = counter receiver + 1 }

main :: IO ()
main = do
    let alice = Agent "Alice" 0
        bob = Agent "Bob" 0
        bob1 = sendMessage alice bob
        bob2 = sendMessage alice bob1
    print bob2
