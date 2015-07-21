from flask import Flask
from collections import Counter

app = Flask(__name__)


@app.route('/count/<key>')
def count(key, counter=Counter()):
    counter[key] += 1
    return str(counter[key])


@app.route('/fibonacci/<int:n>')
def fibonacci(n):
    if n == 0: return str(0)
    a, b = 1, 1
    for i in range(n-1):
        a, b = b, a + b
    return str(a)

app.run(port=8000)

'''
Running 30s test @ http://127.0.0.1:8000/count/key1
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    91.76ms   61.45ms   1.71s    94.69%
    Req/Sec   147.67    138.26   640.00     73.07%
  11901 requests in 30.04s, 1.78MB read
  Socket errors: connect 0, read 140, write 0, timeout 395
Requests/sec:    396.23
Transfer/sec:     60.78KB

Running 30s test @ http://127.0.0.1:8000/fibonacci/9
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   100.04ms  103.16ms   1.71s    94.72%
    Req/Sec   128.74    145.91   616.00     76.48%
  16626 requests in 30.03s, 2.46MB read
  Socket errors: connect 0, read 166, write 0, timeout 537
Requests/sec:    553.61
Transfer/sec:     83.80KB

Running 30s test @ http://127.0.0.1:8000/fibonacci/40
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   104.17ms  167.31ms   1.71s    94.51%
    Req/Sec   145.35    129.26   540.00     65.32%
  29591 requests in 30.10s, 4.57MB read
  Socket errors: connect 283, read 258, write 0, timeout 194
Requests/sec:    983.10
Transfer/sec:    155.53KB

Running 30s test @ http://127.0.0.1:8000/fibonacci/440
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    73.30ms   14.66ms 492.43ms   94.32%
    Req/Sec   271.76    171.25   580.00     59.20%
  5541 requests in 30.04s, 1.30MB read
  Socket errors: connect 0, read 0, write 0, timeout 260
Requests/sec:    184.48
Transfer/sec:     44.32KB
'''
