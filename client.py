import socket
import time

# Функція для отримання оновленого рядка з сервера
def get_update_from_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("ip adress", 1039))
        command = "GetUpdate"
        header = len(command).to_bytes(1, byteorder='big')
        sock.send(header + command.encode())

        response = sock.recv(1024).decode().strip()
        print(response)
        if response != "No updates":
            line_number, new_value = response.split(';')
            line_number = int(line_number)
            update_local_file(line_number, new_value)
        log_message(f"Received update: {response}")

def update_local_file(line_number, new_value):
    with open("client_file.txt", "r+") as file:
        lines = file.readlines()
        if line_number <= len(lines):
            lines[line_number - 1] = new_value + '\n'
        else:
            while len(lines) < line_number - 1:
                lines.append('\n')
            lines.append(new_value + '\n')
        file.seek(0)
        file.writelines(lines)
        file.truncate()

def log_message(message):
    with open("client_log.txt", "a") as log_file:
        log_file.write(f"{time.ctime()} - {message}\n")

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("ip adress", 1039))
        header = len(command).to_bytes(1, byteorder='big')
        sock.send(header + command.encode())

        response = sock.recv(1024).decode().strip()
        print(response)
        log_message(f"Sent: {command}, Received: {response}")

if __name__ == "__main__":
    while True:
        command = input("Enter command (Who, GetUpdate, Update,<line_number>,<new_value>): ")
        if command == "Who" or command.startswith("Update"):
            send_command(command)
        elif command == "GetUpdate":
            get_update_from_server()
        else:
            print("Unknown command")
