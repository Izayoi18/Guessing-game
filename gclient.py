import socket

host = "192.168.1.229"  # Change to the IP address of the server
port = 7777

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Send difficulty level to the server
    difficulty = input("Enter difficulty level (easy/normal/hard): ")
    s.sendall(difficulty.encode())

    # Receive and print the banner from the server
    data = s.recv(1024)
    print(data.decode().strip())

    while True:
        user_input = input("Enter your guess: ").strip()
        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()
        print(reply)
        if "Correct" in reply:
            break

except ConnectionError as e:
    print(f"Connection error: {e}")

finally:
    s.close()
