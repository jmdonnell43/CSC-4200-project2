# Makefile for TCP Client-Server project with header simulation

# Variables
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: build run run-server run-client clean

# Create virtual environment and install dependencies (none required, but ready for future use)
build:
	@echo "Setting up the project..."
	python3 -m venv $(VENV)
	@echo "Project setup complete."

# Run both server and client
run: run-server run-client

# Run the server in the background
run-server:
	@echo "Starting server..."
	$(PYTHON) server.py &

# Run the client
run-client:
	@echo "Starting client..."
	$(PYTHON) client.py

# Clean up compiled files and virtual environment
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf *.log
	rm -rf $(VENV)
	@echo "Cleanup complete."
