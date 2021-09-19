from app import app, routes
import threading
import os


if __name__ == '__main__':
    try:
        queue_thread = threading.Thread(target=routes.QueueHandler.queue_handler)
        queue_thread.daemon = True
        queue_thread.start()

        app.run(host='0.0.0.0', port=1337, debug=False)
    except KeyboardInterrupt:
        os._exit(0)
