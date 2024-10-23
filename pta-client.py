import socket
import threading

def handle_client(connection, address, valid_users, files_directory):
    print(f"Conexão estabelecida com {address}")
    seq_num = None
    authenticated = False
    try:
        while True:
            data = connection.recv(1024).decode('ascii')
            if not data:
                break
            parts = data.strip().split(' ')
            if len(parts) < 2:
                connection.send(f"{seq_num if seq_num else '0'} NOK".encode('ascii'))
                continue

            seq_num = parts[0]
            command = parts[1]
            args = parts[2:] if len(parts) > 2 else None
          
            if command == 'CUMP':
                if args and args[0] in valid_users:
                    authenticated = True
                    connection.send(f"{seq_num} OK".encode('ascii'))
                else:
                    connection.send(f"{seq_num} NOK".encode('ascii'))
                    break
            elif command == 'LIST' and authenticated:
                try:
                    files = ','.join(os.listdir(files_directory))
                    num_files = len(files.split(','))
                    connection.send(f"{seq_num} ARQS {num_files} {files}".encode('ascii'))
                except Exception as e:
                    connection.send(f"{seq_num} NOK".encode('ascii'))

            elif command == 'PEGA' and authenticated:
                if args:
                    filename = args[0]
                    filepath = f"{files_directory}/{filename}"
                    if os.path.isfile(filepath):
                        with open(filepath, 'rb') as f:
                            file_content = f.read()
                        file_size = len(file_content)
                        connection.send(f"{seq_num} ARQ {file_size} ".encode('ascii') + file_content)
                    else:
                        connection.send(f"{seq_num} NOK".encode('ascii'))
                else:
                    connection.send(f"{seq_num} NOK".encode('ascii'))

            elif command == 'TERM' and authenticated:
                connection.send(f"{seq_num} OK".encode('ascii'))
                break

            else:
                connection.send(f"{seq_num} NOK".encode('ascii'))
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        connection.close()

def main():
    with open('pta-server/users.txt', 'r') as f:
        valid_users = [line.strip() for line in f.readlines()]

    files_directory = 'pta-server/files'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 11550))
    server_socket.listen(5)
    print("Servidor PTA aguardando conexões...")

    while True:
        connection, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, address, valid_users, files_directory))
        client_thread.start()

if __name__ == '__main__':
    import os
    main()
