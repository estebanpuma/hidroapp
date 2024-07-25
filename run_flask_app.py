import subprocess
import os


print("ingreso a script")
# Paths to your virtual environment and Flask application (adjust as needed)
venv_path = r'"C:\Users\estep\Transformación Digital\HidroApp\venv\Scripts\activate.bat"'
print(f"venv pass {venv_path}")
app_directory = r"C:\Users\estep\Transformación Digital\HidroApp"
print(f"app pass {app_directory}")
# Correct path to python.exe in your virtual environment
python_path = r'"C:\Users\estep\Transformación Digital\HidroApp\venv\Scripts\python.exe"'

# Load environment variables from .env file

# Get the Flask application file from .env
flask_app = os.getenv('FLASK_APP', 'run.py')

# Change to the app directory
os.chdir(str(app_directory))
print("pasamos change")
# Activate the virtual environment and run the Flask app
subprocess.Popen(f'cmd /c {venv_path} && {python_path} -m flask run', shell=True)