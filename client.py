from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    def on_open(self, event):
        print(f"File opened: {event.src_path}")
        # Send a trigger to the server

# Monitor a directory
path_to_watch = "/path/to/monitor"
event_handler = FileEventHandler()
observer = Observer()
observer.schedule(event_handler, path=path_to_watch, recursive=True)
observer.start()
