""" Creates a client to send data to a server """

import socket
import sys
import traceback

def client(msg, log_buffer=sys.stderr):
    """ Creates client and sends provided message to server """

    server_address = ('localhost', 10000)

    # Create a socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    sock.connect(server_address)

    # Variable to store received message
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)

        # Send message to server
        sock.sendall(msg.encode('utf-8'))

        # Loop until we receive all data back from server
        while True:
            chunk = sock.recv(16)
            received_message += chunk.decode('utf8')
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            if len(chunk) < 16:
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

    finally:
        # Close the socket
        print('closing socket', file=log_buffer)
        sock.close()

        # Return the entire received message
        return received_message

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
