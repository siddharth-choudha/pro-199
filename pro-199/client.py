import socket
import threading
import random


questions = [
    {"question": "What is the capital of rajasthan?", "answer": "jaipur"},
    {"question": "Which planet is known as the lake city of india?", "answer": "udaipur"},
  
]


clients = []

def handle_client(client_socket):
    client_name = client_socket.recv(1024).decode('utf-8')
    print(f"{client_name} connected")

    clients.append({"name": client_name, "socket": client_socket, "score": 0})

    for q in questions:
        question = q["question"]
        answer = q["answer"]

        client_socket.send(question.encode('utf-8'))
        user_answer = client_socket.recv(1024).decode('utf-8')

        if user_answer.lower() == answer.lower():
            index = next((i for i, client in enumerate(clients) if client["socket"] == client_socket), None)
            if index is not None:
                clients[index]["score"] += 1
                client_socket.send("Correct!".encode('utf-8'))
            else:
                client_socket.send("Error updating score".encode('utf-8'))
        else:
            client_socket.send("Incorrect!".encode('utf-8'))

    client_socket.send("Quiz finished. Your final score will be displayed.".encode('utf-8'))

    client_socket.close()
    print(f"{client_name} disconnected")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8888))
    server.listen(5)

    print("Waiting for clients to connect...")

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    main()
