from flask import Flask, render_template
import subprocess
import os
import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the htop display app. Go to /htop to see system information."

@app.route('/htop')
def htop():
    name = "Pujari Mukthi Prasanna" 
    
    username = os.getenv('USER', os.getenv('ASUS', 'codespace'))
    
    # Get server time in IST
    ist_timezone = pytz.timezone('Asia/Kolkata')
    server_time_ist = datetime.datetime.now(ist_timezone)
    server_time_str = server_time_ist.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    try:
        top_output = subprocess.check_output(
            ['top', '-b', '-n', '1'], 
            text=True, 
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        top_output = f"Error running top command: {e.output}"
    except FileNotFoundError:
        top_output = "top command not found"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Information</title>
        <style>
            body {{ font-family: monospace; padding: 20px; }}
            pre {{ background-color: #f4f4f4; padding: 10px; overflow: auto; }}
        </style>
    </head>
    <body>
        <h2>System Information</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>User:</strong> {username}</p>
        <p><strong>Server Time (IST):</strong> {server_time_str}</p>
        <h3>TOP output:</h3>
        <pre>{top_output}</pre>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)