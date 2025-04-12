# Design Implementation – TCP Header Simulation Project

This document describes the design and implementation decisions for a TCP client-server simulation using a custom TCP-style header

---

## 1. Model of Client-Server Communication

This project uses a classic TCP socket model with a fixed-message format protocol.

### Flow of Communication

1. **Server Initialization**
   - The server creates a TCP socket and binds it to a host and port.
   - It listens for a single incoming connection (single-client model).
   - When a client connects, the server handles message reception and parsing.

2. **Client Connection**
   - The client creates a TCP socket and connects to the server's IP and port.
   - It constructs a message with a 14-byte binary header followed by a text payload.
   - The client sends this message to the server and displays the server's response.

3. **Message Handling**
   - The client manually sets control flags: SYN, ACK, FIN.
   - The payload is encoded to bytes and attached after the header.
   - The server reads and parses the header, checks the checksum, and then reads the payload.
   - Based on flags, the server sends a predefined response back to the client.

4. **Connection Termination**
   - The client or server can terminate the connection using the FIN flag.
   - The server gracefully closes the socket on FIN or disconnection.

---

## 2. Custom TCP-Like Header Format

A compact 14-byte header is defined with these fields:

| Field         | Size | Description                              |
|---------------|------|------------------------------------------|
| Source Port   | 2 B  | Arbitrary port from the client           |
| Dest Port     | 2 B  | Server listening port                    |
| Sequence No   | 4 B  | Packet ID or sequence number             |
| ACK Flag      | 1 B  | Acknowledges receipt                     |
| SYN Flag      | 1 B  | Starts communication                     |
| FIN Flag      | 1 B  | Terminates communication                 |
| Payload Size  | 2 B  | Size of the following message payload    |
| Checksum      | 1 B  | Sum of previous 13 bytes mod 256        |

The header is packed and unpacked using Python's `struct` module with format string: `!HHIBBBHB`

---

## 3. Header Checksum Mechanism

### Calculation
- The checksum is the **sum of the first 13 bytes of the header**, modulo 256.
- This byte is appended as the 14th byte during message construction on the client side.

### Validation
- The server re-computes the checksum from the received header.
- If the computed and received checksums match, the message is processed.
- If not, the server responds with a checksum error and drops the message.

### Rationale
- This is a lightweight way to detect corruption or tampering.
- Prevents the server from misinterpreting malformed headers.

---

## 4. Server Response Logic

The server inspects the header flags in this order:
1. If `SYN = 1`: responds with `"SYN received – connection initiated"`
2. If `ACK = 1`: responds with `"ACK received – message acknowledged"`
3. If `FIN = 1`: responds with `"FIN received – connection closing"`
4. If all flags are 0: responds with `"Data received – payload length: X"`

This structure mimics basic TCP control flow in a simplified form.

---

## 5. Error Handling

The server is designed to handle common runtime and protocol errors:

### Covered Errors
- Invalid or partial headers (less than 14 bytes)
- Checksum mismatch
- Disconnected clients
- Unexpected or malformed payloads

### Logging
- All header contents and responses are logged using the `logging` module.
- Errors are also logged to help with debugging and validation.

---

## 6. Project Structure and Modularity

The project is split into the following components:
- `server.py`: Handles listening, receiving, parsing, and responding.
- `client.py`: Constructs headers, sends messages, and handles responses.
- `Makefile`: Simplifies running and cleaning the project.
- `README.md`: Explains setup and usage.
- `design_explanation.md`: Describes architecture and rationale.

---

## 7. Design Highlights

- **Fixed Header Size**: Enables deterministic parsing and validation.
- **Checksum Validation**: Ensures message integrity without full encryption.
- **Interactive Client**: Lets the user set header flags and input messages.
- **No External Dependencies**: Pure Python 3 solution for portability and simplicity.
- **Educational Focus**: Prioritizes understanding of protocol structure over real-world scalability.

---

## 8. Possible Enhancements

1. Add multithreading to allow multiple simultaneous client connections.
2. Use a stronger hash function (e.g., CRC32 or HMAC) for header validation.
3. Add optional AES encryption for payloads.
4. Introduce argument parsing for host/port control on the command line.
5. Implement timeout or keep-alive logic for long connections.

---

## Conclusion

This project provides a hands-on experience with TCP-style communication, demonstrating how structured binary headers and basic control flags work in a socket-based environment. It lays a foundation for more advanced networking features like secure channels, multi-client support, and full protocol emulation.
