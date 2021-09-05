from app import app, routes
import threading


if __name__ == '__main__':
    queue_thread = threading.Thread(target=routes.QueueHandler.queue_handler)
    queue_thread.daemon = True
    queue_thread.start()

    app.run(debug=True)
