import hashlib
import random


users = {
    "A": 1000,
    "B": 500
}

def send_money(sender, receiver, amount):
    print("\n--- Transaction Request ---")

   
    if users[sender] < amount:
        print("Transaction Failed ❌ (Insufficient Balance)")
        return


    nonce = str(random.randint(1000, 9999))
    data = sender + receiver + str(amount) + nonce
    commitment = hashlib.sha256(data.encode()).hexdigest()

    print("Commitment Generated ✔")
    print("Commitment (Proof Part 1):", commitment[:10], "...")  # shortened
    

   
    challenge = random.randint(1, 100)
    print("Challenge Generated:", challenge)
    
    
   
    response = hashlib.sha256((commitment + str(challenge)).encode()).hexdigest()
    print("Response (Proof Part 2):", response[:10], "...")


    verify = hashlib.sha256((commitment + str(challenge)).encode()).hexdigest()

    if response == verify:
      
        users[sender] -= amount
        users[receiver] += amount

        print("Transaction Verified ✔")
        print("Details Hidden 🔒")
    else:
        print("Verification Failed ❌")


while True:
    sender = input("\nEnter Sender (A/B): ")
    receiver = input("Enter Receiver (A/B): ")
    amount = int(input("Enter Amount: "))

    send_money(sender, receiver, amount)

    print("Updated Balances:", users)

    cont = input("Do another transaction? (y/n): ")
    if cont.lower() != 'y':
        break