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

# Initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")
guessme = 0
conn = None
leaderboard = {}  # Dictionary to store username and score

while True:
    if conn is None:
        print("Waiting for connection..")
        conn, addr = s.accept()
        print(f"New client: {addr[0]}")
        conn.sendall(banner.encode())
        difficulty = conn.recv(1024).decode().strip().lower()
        guessme = generate_random_int(difficulty)
        print(f"Difficulty level selected: {difficulty}")
        attempts = 0  # Counter for the number of attempts
    else:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        attempts += 1
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            conn.sendall(b"Correct Answer!")
            # Score calculation: Less attempts = higher score
            score = 1000 // attempts  # Adjust as needed for scaling
            username = addr[0]  # You can prompt for username if needed
            leaderboard[username] = score
            conn.close()
            conn = None
            print("User disconnected.")
            print("Leaderboard:")
            # Display leaderboard sorted by score
            sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
            for i, (name, score) in enumerate(sorted_leaderboard, start=1):
                print(f"{i}. {name}: {score}")
            continue
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nenter guess: ")
            continue
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nenter guess:")
            continue
