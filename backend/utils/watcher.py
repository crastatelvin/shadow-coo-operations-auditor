import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

class LogWatcher:
    def __init__(self, watch_dir, callback):
        self.watch_dir = watch_dir
        self.callback = callback
        self.event_handler = self.Handler(self.callback)
        self.observer = Observer()

    class Handler(FileSystemEventHandler):
        def __init__(self, callback):
            self.callback = callback

        def on_modified(self, event):
            if not event.is_directory and event.src_path.endswith('.csv'):
                print(f"Log change detected: {event.src_path}")
                # Debounce: wait a second to ensure file is fully written
                time.sleep(1)
                self.callback(event.src_path)

    def start(self):
        self.observer.schedule(self.event_handler, self.watch_dir, recursive=False)
        self.observer.start()
        print(f"Shadow COO Watcher started on: {self.watch_dir}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
