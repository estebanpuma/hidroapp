import os
from app import create_app, socketio



settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)
#socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

