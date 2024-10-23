# PTA Server - Protocolo de Transferência de Arquivos

Este repositório faz parte de uma atividade prática referente ao desenvolvimento de um servidor para o Protocolo de Transferência de Arquivos (PTA). Este protocolo didático visa a transferência de arquivos entre um cliente e um servidor de forma segura e eficiente.

## Estrutura do Projeto

- `pta-server/`
  - `users.txt`: Contém a lista de usuários autorizados a se conectar ao servidor.
  - `files/`: Diretório contendo os arquivos que podem ser solicitados pelos clientes.
  - `server.py`: Código do servidor PTA.

## Instruções para Executar o Servidor

### Requisitos

- Python 3.x
- Bibliotecas do Python: `socket`, `threading`, `os`

### Passos para Execução

1. **Clone o repositório**:
   ```bash
   git clone <URL do seu repositório>
   cd pta-server
   ```

2. **Certifique-se de que os arquivos estão no local correto**:
   - Verifique se o diretório `files/` contém os arquivos que serão servidos.
   - Verifique se o arquivo `users.txt` contém os nomes dos usuários autorizados, cada um em uma linha.

3. **Execute o Servidor**:
   
   Execute o servidor utilizando o seguinte comando:
   ```bash
   python server.py
   ```

   O servidor irá escutar na porta `11550` por padrão. Certifique-se de que esta porta está livre antes de executar o código.

4. **Conectando ao Servidor**:
   - Utilize um cliente compatível com o protocolo PTA (por exemplo, o `pta-client.py` fornecido).
   - O cliente deve se conectar ao servidor e seguir o protocolo descrito para autenticação, listagem e requisição de arquivos.

## Formato das Mensagens

O servidor responde aos seguintes comandos:

- **CUMP**: Apresentação do cliente. Se o cliente for válido, o servidor responde com `OK`, caso contrário, `NOK`.
- **LIST**: Lista os arquivos disponíveis no servidor.
- **PEGA [arquivo]**: Solicita um arquivo específico.
- **TERM**: Solicita o fechamento da conexão.

## Observações

- O servidor irá encerrar a conexão se o cliente não for autenticado corretamente.
- Todas as comunicações utilizam mensagens no formato ASCII.
- Para testar adequadamente, utilize o script `pta-client.py` que pode simular as requisições dos clientes.

## Referências
Este projeto é parte de uma atividade prática para estudo e desenvolvimento de protocolos de aplicação utilizando sockets. Mais informações podem ser encontradas no documento `pta.pdf` fornecido.

