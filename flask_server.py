from flask import Flask
import requests

app = Flask(__name__)


@app.route('/count/<key>')
def count(key):
    req = requests.get('http://127.0.0.1:8000/count/' + key)
    return req.text


@app.route('/fibonacci/<int:n>')
def fibonacci(n):
    if n == 0: return str(0)
    a, b = 1, 1
    for i in range(n-1):
        a, b = b, a + b
    return str(a)

if __name__ == '__main__':
    app.run(port=5000)

'''
Running 30s test @ http://127.0.0.1:4000/count/key6
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.01s   506.89ms   1.52s    66.67%
    Req/Sec     0.31      0.59     2.00     76.27%
  59 requests in 30.04s, 9.27KB read
  Socket errors: connect 0, read 0, write 0, timeout 56
Requests/sec:      1.96
Transfer/sec:     315.94B

Running 30s test @ http://127.0.0.1:4000/fibonacci/9
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    59.74ms   60.91ms   1.69s    98.20%
    Req/Sec   187.97    175.84   646.00     72.04%
  18898 requests in 30.04s, 2.90MB read
  Socket errors: connect 0, read 81, write 0, timeout 403
Requests/sec:    629.16
Transfer/sec:     98.92K

Running 30s test @ http://127.0.0.1:4000/fibonacci/500
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    67.61ms   77.37ms   1.70s    97.67%
    Req/Sec   200.08    159.17   626.00     55.79%
  20846 requests in 30.04s, 5.29MB read
  Socket errors: connect 0, read 99, write 0, timeout 532
Requests/sec:    693.95
Transfer/sec:    180.26KB
'''
