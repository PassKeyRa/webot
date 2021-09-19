from app import app, routes
import threading
import os


if __name__ == '__main__':
    try:
        queue_thread = threading.Thread(target=routes.QueueHandler.queue_handler)
        queue_thread.daemon = True
        queue_thread.start()

        app.run(debug=True)
   except KeyboardInterrupt:
        os._exit(0)
