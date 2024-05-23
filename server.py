import socket
import threading
import time

# Глобальна змінна для відстеження змін
last_update = {"line_number": None, "new_value": None}

# Функція для зміни або додавання рядка у файлі
def update_file_line(line_number, new_value):
    global last_update
    with open("server_file.txt", "r+") as file:
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
        last_update = {"line_number": line_number, "new_value": new_value}

# Функція для отримання останнього оновлення
def get_last_update():
    if last_update["line_number"] is None:
        return "No updates"
    update = f'{last_update["line_number"]};{last_update["new_value"]}'
    return update

# Функція для скидання останнього оновлення
def clear_last_update():
    global last_update
    last_update = {"line_number": None, "new_value": None}

def handle_client(client_socket):
    while True:
        try:
            header = client_socket.recv(1)
            if not header:
                break
            
            header_length = int.from_bytes(header, byteorder='big')
            command = client_socket.recv(header_length).decode()
            response = ''

            if command == 'Who':
                response = 'Author: Your Name, Variant: \n'
            elif command == 'GetUpdate':
                response = get_last_update() + '\n'
                clear_last_update()
            elif command.startswith('Update'):
                _, line_number, new_value = command.split(',')
                line_number = int(line_number)
                update_file_line(line_number, new_value)
                response = f'Updated line {line_number}\n'
            else:
                response = 'Unknown command\n'
            
            client_socket.send(response.encode())
            log_message(f'Sent: {response}')
        
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

def log_message(message):
    with open("server_log.txt", "a") as log_file:
        log_file.write(f"{time.ctime()} - {message}\n")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("ip adress", 1039))
    server.listen(5)
    print("Server listening on port 1039")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
