import os
import time
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to send reload command to Blender
def send_reload_command():
    host = '127.0.0.1'
    port = 5555
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            s.sendall(b'reload')
        except ConnectionRefusedError:
            print("Blender is not listening for connections.")
        finally:
            s.close()

# Define a file system event handler
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Only trigger reload if a Python script file is modified
        if event.src_path.endswith('.py'):
            print(f"{event.src_path} has been modified. Reloading script...")
            send_reload_command()

# Set up the Watchdog observer
def watch_scripts():
    path = './'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching directory: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Start watching for changes to Python script files
watch_scripts()
