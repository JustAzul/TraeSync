import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils import get_public_ip

class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, on_change_callback):
        self.on_change_callback = on_change_callback

    def on_modified(self, event):
        self.on_change_callback(event)

    def on_created(self, event):
        self.on_change_callback(event)

    def on_deleted(self, event):
        self.on_change_callback(event)

class Watcher:
    """
    Watches the configuration folder for file changes and monitors the public IP for changes.
    Triggers the provided sync_callback when a change is detected.
    """
    def __init__(self, config_folder, sync_callback, check_interval=60):
        self.config_folder = config_folder
        self.sync_callback = sync_callback
        self.check_interval = check_interval
        self.last_public_ip = get_public_ip()
        self.observer = Observer()

    def start(self):
        # Setup file system watcher
        event_handler = ConfigChangeHandler(self.on_file_change)
        self.observer.schedule(event_handler, self.config_folder, recursive=True)
        self.observer.start()

        # Start IP checking in a separate thread
        ip_thread = threading.Thread(target=self.check_ip_loop, daemon=True)
        ip_thread.start()

        print("Watcher started. Monitoring for changes...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def on_file_change(self, event):
        print("File change detected:", event.src_path)
        self.sync_callback()

    def check_ip_loop(self):
        while True:
            current_ip = get_public_ip()
            if current_ip != self.last_public_ip:
                print(f"Public IP change detected: {self.last_public_ip} -> {current_ip}")
                self.last_public_ip = current_ip
                self.sync_callback()
            time.sleep(self.check_interval)
