# CSC-4200-Assignment2
This Python 3 project uses TCP sockets to implement a simple client-server model simulating TCP headers with checksum validation.

## Features

- A TCP server that handles a single client connection
- Conditional server responses based on TCP-style control flags (SYN, ACK, FIN)
- Custom binary header parsing using `struct`
- Secure message format verification with header checksum
- Appropriate error management for malformed headers or invalid checksums

## Requirements

- Python 3.6 or later
- No external libraries required (uses built-in `socket`, `struct`, `logging`)

## Project Structure

```
├── server.py              # Server implementation
├── client.py              # Client implementation
├── Makefile               # Build and run commands
├── README.md              # This file
└── design_explanation.md  # Design documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build the project:
   ```
   make build
   ```

## TCP Header Simulation

A custom 14-byte TCP-style header is used with the following structure:

| Field         | Size | Description                        |
|---------------|------|------------------------------------|
| Source Port   | 2 B  | Arbitrary client port              |
| Dest Port     | 2 B  | Server's listening port            |
| Sequence No   | 4 B  | Sequence number                    |
| ACK Flag      | 1 B  | Acknowledgment (0 or 1)            |
| SYN Flag      | 1 B  | Synchronize/Start (0 or 1)         |
| FIN Flag      | 1 B  | Terminate connection (0 or 1)      |
| Payload Size  | 2 B  | Size of payload                    |
| Checksum      | 1 B  | Sum of previous 13 bytes mod 256   |

This header is followed by a payload of variable length.

## Usage

### Running the Server and Client Together

To run both the server and client:
```
make run-server
make run-client
```

### Command Line Arguments

By default, both programs connect to:
- `--host`: 127.0.0.1
- `--port`: 5000

You may modify these in the Python files manually or add argparse support.

### Client Interaction

1. Start the server (`make run-server`)
2. Start the client (`make run-client`)
3. Enter TCP flags and a payload at the prompts
4. The server will respond based on header flags and log the interaction

## Cleanup

To remove logs and cache files:
```
make clean
```

## Security Notes

- Checksum ensures header integrity but does not secure payload content.
- No encryption or TLS is used in this assignment.
- Designed for educational purposes only.
