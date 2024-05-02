import socket
import random

host = "0.0.0.0"
port = 7777
banner = """
== Guessing Game =="""

def generate_random_int(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "normal":
        return random.randint(1, 100)
    elif difficulty == "hard":
        return random.randint(1, 200)
    else:
        raise ValueError("Invalid difficulty level")


def load_leaderboard():
    leaderboard = {}
    try:
        with open("leaderboard.txt", "r") as file:
            for line in file:
                name, score, difficulty = line.strip().split(",")
                leaderboard[name] = {"score": int(score), "difficulty": difficulty}
    except FileNotFoundError:
        pass
    return leaderboard


def save_leaderboard(leaderboard):
    with open("leaderboard.txt", "w") as file:
        for name, data in leaderboard.items():
            file.write(f"{name},{data['score']},{data['difficulty']}\n")


# Load leaderboard data at startup
leaderboard = load_leaderboard()

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")

while True:
    conn, addr = s.accept()
    print(f"New client: {addr[0]}")

    conn.sendall(banner.encode())
    difficulty = conn.recv(1024).decode().strip().lower()

    if addr[0] in leaderboard:
        score = leaderboard[addr[0]]["score"]
        leaderboard[addr[0]]["difficulty"] = difficulty
    else:
        score = 0
        leaderboard[addr[0]] = {"score": score, "difficulty": difficulty}

    guessme = generate_random_int(difficulty)
    print(f"Difficulty level selected: {difficulty}")

    attempts = 0  # Counter for the number of attempts

    while True:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        attempts += 1
        print(f"User guess attempt: {guess}")

        if guess == guessme:
            conn.sendall(b"Correct Answer!")
            # Score calculation: Less attempts = higher score
            score = 1000 // attempts  # Adjust as needed for scaling
            leaderboard[addr[0]]["score"] = score
            save_leaderboard(leaderboard)
            conn.close()
            print("User disconnected.")
            print("Leaderboard:")
            # Display leaderboard sorted by score
            sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["score"], reverse=True)
            for i, (name, data) in enumerate(sorted_leaderboard, start=1):
                print(f"{i}. {name}: {data['score']} (Difficulty: {data['difficulty']})")
            break

        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nenter guess: ")
            continue

        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nenter guess:")
            continue
