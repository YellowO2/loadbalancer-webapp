import socket
import time
import psutil
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Track metrics
request_count = 0
start_time = time.time()

@app.route('/')
def show_hostname():
    global request_count
    request_count += 1
    
    hostname = socket.gethostname()
    uptime = time.time() - start_time
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    # Select animal based on hostname hash
    animals = ['cat', 'dog', 'bear', 'bunny', 'fox', 'panda', 'koala', 'pig', 'owl', 'penguin']
    animal = animals[hash(hostname) % len(animals)]
    
    return render_template(
        'index.html',
        hostname=hostname,
        animal=animal,
        requests=request_count,
        uptime=int(uptime),
        cpu=cpu_percent,
        memory=memory.percent
    )

@app.route('/health')
def health():
    """Health check endpoint for load balancer"""
    return jsonify({
        'status': 'healthy',
        'hostname': socket.gethostname(),
        'uptime': time.time() - start_time,
        'requests': request_count
    }), 200

@app.route('/metrics')
def metrics():
    """Prometheus-style metrics endpoint"""
    return f"""# HELP requests_total Total requests served
# TYPE requests_total counter
requests_total{{hostname="{socket.gethostname()}"}} {request_count}

# HELP uptime_seconds Server uptime in seconds
# TYPE uptime_seconds gauge
uptime_seconds{{hostname="{socket.gethostname()}"}} {time.time() - start_time}
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)