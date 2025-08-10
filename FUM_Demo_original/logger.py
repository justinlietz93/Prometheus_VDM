# logger.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import sys

class Logger:
    """
    A simple logging utility to write output to both the console and a file.
    """
    def __init__(self, log_file_path):
        """
        Initializes the logger.

        Args:
            log_file_path (str): The path to the file where logs will be saved.
        """
        self.terminal = sys.stdout
        # Open the log file in write mode, which will create it if it doesn't exist
        self.log_file = open(log_file_path, "w")

    def write(self, message):
        """
        Writes a message to both the console and the log file.
        """
        self.terminal.write(message)
        self.log_file.write(message)
        self.flush() # Ensure the message is written immediately

    def flush(self):
        """
        Flushes the output streams. This is necessary to ensure that text
        appears in the file in real-time.
        """
        self.terminal.flush()
        self.log_file.flush()

    def log_metrics(self, metrics: dict, header: str):
        """
        Writes a dictionary of metrics to the log in a structured format.
        """
        self.write(f"\n--- {header} ---\n")
        for key, value in metrics.items():
            self.write(f"  - {key}: {value}\n")
        self.write("--------------------\n")
        
    def close(self):
        """Closes the log file."""
        self.log_file.close()