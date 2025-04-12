import socket
import struct
import logging

# === Server Configuration ===
HOST = 'localhost'
PORT = 5000
HEADER_FORMAT = '!HHIBBBHB'  # Header fields + checksum
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

# === Logging Setup ===
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')


def validate_checksum(header_bytes):
    header_13 = header_bytes[:-1]
    received_checksum = header_bytes[-1]
    computed_checksum = sum(header_13) % 256
    return received_checksum == computed_checksum


def parse_header(header_bytes):
    try:
        return struct.unpack(HEADER_FORMAT, header_bytes)
    except struct.error:
        raise ValueError("Malformed header")


def handle_client(conn, addr):
    logging.info(f"Connection from {addr}")

    while True:
        try:
            header = conn.recv(HEADER_SIZE)
            if not header:
                logging.info("Client disconnected.")
                break

            if len(header) < HEADER_SIZE:
                raise ValueError("Incomplete header received")

            if not validate_checksum(header):
                raise ValueError("Checksum mismatch – header corrupted")

            # Unpack header
            src_port, dest_port, seq_num, ack_flag, syn_flag, fin_flag, payload_size, _ = parse_header(header)

            # Receive payload
            payload = b""
            while len(payload) < payload_size:
                chunk = conn.recv(payload_size - len(payload))
                if not chunk:
                    break
                payload += chunk

            logging.info(f"Header: SrcPort={src_port}, DestPort={dest_port}, Seq={seq_num}, "
                         f"ACK={ack_flag}, SYN={syn_flag}, FIN={fin_flag}, PayloadSize={payload_size}")

            # Determine Response
            if syn_flag == 1:
                response = "SYN received – connection initiated"
            elif ack_flag == 1:
                response = "ACK received – message acknowledged"
            elif fin_flag == 1:
                response = "FIN received – connection closing"
            else:
                response = f"Data received – payload length: {payload_size}"

            logging.info(f"Server Response: {response}")
            conn.sendall(response.encode())

            if fin_flag == 1:
                logging.info("Connection closing due to FIN flag.")
                break

        except ValueError as ve:
            logging.warning(f"Error: {ve}")
            conn.sendall(f"Error: {ve}".encode())
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            break

    conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        logging.info(f"Server listening on {HOST}:{PORT}")

        conn, addr = server_sock.accept()
        with conn:
            handle_client(conn, addr)


if __name__ == '__main__':
    start_server()
