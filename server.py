from flask import Flask, jsonify, send_file
import os

app = Flask(__name__)

# Folder where the software to be distributed is stored
SOFTWARE_DIR = "software"

# Make sure the folder exists
if not os.path.exists(SOFTWARE_DIR):
    os.makedirs(SOFTWARE_DIR)

@app.route('/list')
def list_software():
    """Returns the list of available software."""
    try:
        files = [f for f in os.listdir(SOFTWARE_DIR) if f.endswith('.py')]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>')
def download_software(filename):
    """Allows downloading specific software."""
    try:
        file_path = os.path.join(SOFTWARE_DIR, filename)
        if os.path.exists(file_path) and filename.endswith('.py'):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Example test software
@app.route('/add_test_software')
def add_test_software():
    """Adds some test software for demonstration."""
    test_files = {
        "hello.py": """
# Simple Hello World program
from time import sleep
display.fill(0)
display.text("Hello World!", 0, 0, 1)
display.text("ESP32-S3", 0, 10, 1)
display.text("Test App", 0, 20, 1)
display.show()
sleep(5)  # Display for 5 seconds
""",
        "counter.py": """
# Simple counter program
from time import sleep
count = 0
while count < 10:  # Count to 10 then exit
    display.fill(0)
    display.text("Counter:", 0, 0, 1)
    display.text(str(count), 0, 10, 1)
    display.text("Press home", 0, 20, 1)
    display.show()
    count += 1
    sleep(1)
"""
    }
    
    for filename, content in test_files.items():
        with open(os.path.join(SOFTWARE_DIR, filename), 'w') as f:
            f.write(content)
    
    return jsonify({"status": "Test software added"})

def add_test_software_on_startup():
    """Adds test software on server startup"""
    for route in app.url_map.iter_rules():
        if route.endpoint == 'add_test_software':
            with app.test_client() as client:
                client.get('/add_test_software')
            break

if __name__ == '__main__':
    # Add test software on startup
    add_test_software_on_startup()
    
    # Start the server
    app.run(host='0.0.0.0', port=8000, debug=True)
