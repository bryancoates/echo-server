""" Creates a server to received and echo a message back to a client """

import socket
import sys
import traceback

def server(log_buffer=sys.stderr):
    """ Create the server, listen, and echo back message """

    # Define the server address and port
    address = ('127.0.0.1', 10000)

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Bind the socket and begin listening
    sock.bind(address)
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # Create a connection to accept sent data
            conn, addr = sock.accept()
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # Set the buffer size and receive the data
                    buffer_size = 16
                    data = conn.recv(buffer_size)
                    print('received "{0}"'.format(data.decode('utf8')))

                    # Send the received data back to the client
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))

                    # Check the length of the data and exit if less than 
                    # buffer size, indicating end of sent data
                    if len(data) < buffer_size:
                        conn.close()
                        break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                # Close the connection
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        # Close the socket
        print('quitting echo server', file=log_buffer)
        sock.close()
        return

if __name__ == '__main__':
    server()
    sys.exit(0)
