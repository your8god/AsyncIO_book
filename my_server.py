import socket
import asyncio


async def echo(connection, loop, address):
    while data := await loop.sock_recv(connection, 1024):
        print(f'Сообщение от {address}: {data}')
        await loop.sock_sendall(connection, data)


async def listening(server_socket, loop):
    while True:
        connection, client_address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Получен запрос на подключение {client_address}')
        asyncio.create_task(echo(connection, loop, client_address))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listening(server_socket, asyncio.get_event_loop())


asyncio.run(main())