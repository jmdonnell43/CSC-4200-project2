import socket
import struct

# === Server Configuration ===
SERVER_HOST = 'localhost'
SERVER_PORT = 5000

# === Header Format with Checksum ===
# Format: Source Port (2), Dest Port (2), Seq Num (4), ACK (1), SYN (1), FIN (1), Payload Size (2), Checksum (1)
HEADER_FORMAT = '!HHIBBBHB'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def compute_checksum(header_bytes_13):
    return sum(header_bytes_13) % 256


def build_header_with_checksum(src_port, dest_port, seq_num, ack, syn, fin, payload_size):
    # Pack the first 13 bytes (without checksum)
    partial_header = struct.pack('!HHIBBBH', src_port, dest_port, seq_num, ack, syn, fin, payload_size)
    checksum = compute_checksum(partial_header)
    full_header = partial_header + struct.pack('!B', checksum)
    return full_header


def main():
    src_port = 12345
    dest_port = SERVER_PORT
    seq_num = 1

    # === User Input ===
    ack_flag = int(input("ACK flag (0 or 1): "))
    syn_flag = int(input("SYN flag (0 or 1): "))
    fin_flag = int(input("FIN flag (0 or 1): "))
    payload = input("Enter payload: ").encode()
    payload_size = len(payload)

    # === Build Header and Message ===
    header = build_header_with_checksum(src_port, dest_port, seq_num, ack_flag, syn_flag, fin_flag, payload_size)
    message = header + payload

    # === Send Message ===
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.sendall(message)

        response = sock.recv(1024)
        print(f"Server response: {response.decode()}")


if __name__ == '__main__':
    main()
