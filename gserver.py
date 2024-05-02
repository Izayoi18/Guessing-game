import socket
import random 

host = "0.0.0.0"
port = 7777
banner = """
== Guessing Game v1.0 ==
Enter your guess:"""

def generate_random_int(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "normal":
        return random.randint(1, 100)
    elif difficulty == "hard":
        return random.randint(1, 200)
    else:
        raise ValueError("Invalid difficulty level")

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")
guessme = 0
conn = None
while True:
    if conn is None:
        print("waiting for connection..")
        conn, addr = s.accept()
        difficulty = conn.recv(1024).decode().strip().lower()
        guessme = generate_random_int(difficulty)
        print(f"new client: {addr[0]}")
        # cheat_str = f"==== number to guess is {guessme} \n" + banner
        # conn.sendall(cheat_str.encode())
        conn.sendall(banner.encode())
    else:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            conn.sendall(b"Correct Answer!")
            conn.close()
            conn = None
            continue
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nenter guess: ")
            continue
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nenter guess:")
            continue
