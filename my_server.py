import socket
import asyncio
import signal


class ExitException(SystemExit):
    pass

def exit_raise():
    raise ExitException

tasks = []

async def close_echo(tasks):
    waiters = [asyncio.wait_for(task, 2) for task in tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass

async def echo(connection, loop, address):
    while data := await loop.sock_recv(connection, 1024):
        print(f'Сообщение от {address}: {data}')
        await loop.sock_sendall(connection, data)

async def listening(server_socket, loop):
    while True:
        connection, client_address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Получен запрос на подключение {client_address}')
        task = asyncio.create_task(echo(connection, loop, client_address))
        tasks.append(task)


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    for item in ('SIGINT', 'SIGTERM'):
        main_loop.add_signal_handler(getattr(signal, item), exit_raise)

    await listening(server_socket, main_loop)


main_loop = asyncio.new_event_loop()
try:
    main_loop.run_until_complete(main())
except ExitException:
    main_loop.run_until_complete(close_echo(tasks))
finally:
    main_loop.close()