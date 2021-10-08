from app import app, QueueHandler

import threading
import os

if __name__ == '__main__':
    try:
        queue_thread = threading.Thread(target=QueueHandler.QueueHandler.queue_handler)
        queue_thread.daemon = True
        queue_thread.start()

        app.run(host='0.0.0.0', port=80, debug=False)
    except KeyboardInterrupt:
        os._exit(0)
