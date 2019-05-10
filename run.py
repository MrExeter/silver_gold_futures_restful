from app import create_app
from app.future.models import *
from app.future.initializer import initialize_futures

if __name__ == '__main__':
    flask_app = create_app('dev')

    with flask_app.app_context():
        # Create database if not already
        db.create_all()

        # Retrieve and populate the futures data
        initialize_futures()

    flask_app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)

