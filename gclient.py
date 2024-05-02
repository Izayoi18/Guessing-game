import socket

host = "192.168.1.229"
port = 7777

while True:
    s = socket.socket()
    try:
        s.connect((host, port))

        # received the banner
        data = s.recv(1024)
        # print banner
        print(data.decode().strip())

        while True:
            # Input from the user
            user_input = input("").strip()

            s.sendall(user_input.encode())
            reply = s.recv(1024).decode().strip()

            if not reply:
                print("Server disconnected.")
                break

            if "Correct" in reply:
                print(reply)
                break

            print(reply)

        # Ask the user if they want to play again or quit
        print("\n")
        print("Do you want to play(1) or quit(2):")

        choice = input("Enter corresponding number: ")
        if choice != "1":
            print("Thank you for playing the Game.")
            break

    except ConnectionAbortedError:
        print("Connection was aborted by the software in your host machine. Please try again.")
    except ConnectionResetError:
        print("Connection was reset by the server. Please try again.")
    finally:
        s.close()