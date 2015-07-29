from flask import Flask
import requests
from fibonacci import fib

app = Flask(__name__)


@app.route('/count/<key>')
def count(key):
    req = requests.get('http://127.0.0.1:8000/count/' + key)
    return req.text


@app.route('/fibonacci/<int:n>')
def fibonacci(n):
    return str(fib(n))


if __name__ == '__main__':
    app.run(port=5000)

'''
Running 30s test @ http://127.0.0.1:4000/count/key5
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.05s   410.64ms   1.97s    40.48%
    Req/Sec     8.34     10.71    90.00     87.02%
  689 requests in 30.05s, 112.28KB read
  Socket errors: connect 0, read 0, write 0, timeout 605
Requests/sec:     22.93
Transfer/sec:      3.74KB

Running 30s test @ http://127.0.0.1:4000/fibonacci/9
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   232.65ms   90.43ms   1.95s    77.89%
    Req/Sec    94.90     45.98   353.00     71.22%
  22314 requests in 30.04s, 3.53MB read
  Socket errors: connect 0, read 0, write 0, timeout 175
Requests/sec:    742.88
Transfer/sec:    120.43KB

Running 30s test @ http://127.0.0.1:4000/fibonacci/33
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     0.00us    0.00us   0.00us    -nan%
    Req/Sec     0.30      0.67     2.00     80.00%
  11 requests in 30.05s, 1.84KB read
  Socket errors: connect 0, read 0, write 0, timeout 11
Requests/sec:      0.37
Transfer/sec:      62.59B
'''
