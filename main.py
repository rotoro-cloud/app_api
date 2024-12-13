import time, random
from flask import Flask, request
from prometheus_client import start_http_server, Counter, Histogram, Summary

# Заготовка для отдельного порта метрик
### from prometheus_client import make_wsgi_app
### from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

REQUESTS = Counter(
    "http_requests_total",
    "Total number of requests",
    labelnames=["path", "method"],
)

DURATION = Histogram(
    "http_requests_duration_seconds",
    "Requests duration in seconds histogram",
    labelnames=["method", "path"],
    buckets=(0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.5, 1),
)

SIZE = Summary(
    "http_uploaded_files_size_bytes",
    "Uploaded file size in bytes summary",
    labelnames=["path"],
)


# Для длинных запросов
@app.get("/wait")
def get_wait():

    REQUESTS.labels("/wait", "GET").inc()
    return "Get cars list"

@app.post("/wait")
def post_wait():
    time.sleep(0.8)

    REQUESTS.labels("/wait", "POST").inc()
    return "Get cars list"


# Обычные обработчики
@app.get("/cars")
def get_car_list():
    process_request(50)
    REQUESTS.labels("/cars", "GET").inc()
    return "Get cars list"

@app.get("/cars/<int:id>")
def get_single_car(id):
    process_request(100)
    REQUESTS.labels("/cars", "GET").inc()
    return "Get single car " + str(id)

@app.post("/cars")
def create_new_car():
    process_request(500)
    size = len(request.files["photo"].read())
    SIZE.labels(request.path).observe(size)
    REQUESTS.labels("/cars", "POST").inc()
    return "New car"

@app.patch("/cars/<int:id>")
def update_single_car(id):
    process_request(75)
    REQUESTS.labels("/cars", "PATCH").inc()
    return "Update single car " + str(id)

@app.delete("/cars/<int:id>")
def remove_car(id):
    process_request(100)
    REQUESTS.labels("/cars", "DELETE").inc()
    return "Delete single car " + str(id)

@app.get("/boats")
def get_boat_list():
    process_request(50)
    REQUESTS.labels("/boats", "GET").inc()
    return "Get boats list"

@app.get("/boats/<int:id>")
def get_single_boat(id):
    process_request(100)
    REQUESTS.labels("/boats", "GET").inc()
    return "Get single boat " + str(id)

@app.post("/boats")
def create_new_boat():
    process_request(500)
    size = len(request.files["photo"].read())
    SIZE.labels(request.path).observe(size)
    REQUESTS.labels("/boats", "POST").inc()
    return "New boat"

@app.patch("/boats/<int:id>")
def update_single_boat(id):
    process_request(75)
    REQUESTS.labels("/boats", "PATCH").inc()
    return "Update single boat " + str(id)

@app.delete("/boats/<int:id>")
def remove_boat(id):
    process_request(100)
    REQUESTS.labels("/boats", "DELETE").inc()
    return "Delete single boat " + str(id)


### Логика подсчёта задержки
def before_request():
    request.start_time = time.time()

def after_request(response):
    request_latency = time.time() - request.start_time
    DURATION.labels(request.method, request.path).observe(request_latency)
    return response


# Заготовка для отдельного порта 
### app.wsgi_app = DispatcherMiddleware(app.wsgi_app, { '/metrics': make_wsgi_app() })


# dummy computing
def process_request(max_delay=100):
    time_to_sleep = random.randint(5, max_delay) / 1000
    print(time_to_sleep)
    time.sleep(time_to_sleep)


# Запуск 
if __name__ == "__main__":
    app.before_request(before_request)
    app.after_request(after_request)

    start_http_server(5003)
    app.run(port="5001", debug=True, use_reloader=False)
# Обход ошибки с перезапуском фласк
###    app.run(port='5001', debug=True)
