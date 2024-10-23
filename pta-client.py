import socket
import threading
import os

class PTAServer:
    def __init__(self, host, port, users_file, files_directory):
        self.host = host
        self.port = port
        self.valid_users = self.load_users(users_file)
        self.files_directory = files_directory

    def load_users(self, users_file):
        with open(users_file, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def handle_client(self, connection, address):
        print(f"Conexão estabelecida com {address}")
        seq_num = None
        authenticated = False
        try:
            while True:
                data = connection.recv(1024).decode('ascii')
                if not data:
                    break

                seq_num, command, args = self.parse_message(data)

                if not seq_num or not command:
                    connection.send(f"{seq_num if seq_num else '0'} NOK".encode('ascii'))
                    continue

                if command == 'CUMP':
                    authenticated = self.authenticate(args, connection, seq_num)
                    if not authenticated:
                        break
                elif command == 'LIST' and authenticated:
                    self.list_files(connection, seq_num)
                elif command == 'PEGA' and authenticated:
                    self.send_file(connection, args, seq_num)
                elif command == 'TERM' and authenticated:
                    self.terminate_connection(connection, seq_num)
                    break
                else:
                    connection.send(f"{seq_num} NOK".encode('ascii'))
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            connection.close()

    def parse_message(self, data):
        parts = data.strip().split(' ')
        seq_num = parts[0] if len(parts) > 0 else None
        command = parts[1] if len(parts) > 1 else None
        args = parts[2:] if len(parts) > 2 else None
        return seq_num, command, args

    def authenticate(self, args, connection, seq_num):
        if args and args[0] in self.valid_users:
            connection.send(f"{seq_num} OK".encode('ascii'))
            return True
        else:
            connection.send(f"{seq_num} NOK".encode('ascii'))
            return False

    def list_files(self, connection, seq_num):
        try:
            files = ','.join(os.listdir(self.files_directory))
            num_files = len(files.split(',')) if files else 0
            connection.send(f"{seq_num} ARQS {num_files} {files}".encode('ascii'))
        except Exception:
            connection.send(f"{seq_num} NOK".encode('ascii'))

    def send_file(self, connection, args, seq_num):
        if args:
            filename = args[0]
            filepath = os.path.join(self.files_directory, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'rb') as f:
                        file_content = f.read()
                    file_size = len(file_content)
                    connection.send(f"{seq_num} ARQ {file_size} ".encode('ascii') + file_content)
                except Exception:
                    connection.send(f"{seq_num} NOK".encode('ascii'))
            else:
                connection.send(f"{seq_num} NOK".encode('ascii'))
        else:
            connection.send(f"{seq_num} NOK".encode('ascii'))

    def terminate_connection(self, connection, seq_num):
        connection.send(f"{seq_num} OK".encode('ascii'))

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print("Servidor PTA aguardando conexões...")

        while True:
            connection, address = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(connection, address))
            client_thread.start()


def main():
    try:
        server = PTAServer(
            host='0.0.0.0',
            port=11550,
            users_file='pta-server/users.txt',
            files_directory='pta-server/files'
        )
        server.start_server()
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
        input("Pressione Enter para fechar...")


if __name__ == '__main__':
    main()
