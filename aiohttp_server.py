import asyncio
from aiohttp import web
import requests


@asyncio.coroutine
def count(request):
    key = request.match_info['key']
    req = requests.get('http://127.0.0.1:8000/count/' + key)
    return web.Response(text=req.text)


@asyncio.coroutine
def fibonacci(request):
    n = int(request.match_info['n'])
    if n == 0: return web.Response(text=str(0))
    a, b = 1, 1
    for i in range(n-1):
        a, b = b, a + b
    return web.Response(text=str(a))


app = web.Application()
app.router.add_route('GET', '/count/{key}', count)
app.router.add_route('GET', '/fibonacci/{n}', fibonacci)


loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, '0.0.0.0', 5050)
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(handler.finish_connections(1.0))
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.finish())
loop.close()

'''
Running 30s test @ http://127.0.0.1:5050/count/key3
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.01s   505.59ms   1.52s    66.67%
    Req/Sec     1.47      0.50     2.00     52.54%
  59 requests in 30.05s, 10.19KB read
  Socket errors: connect 0, read 58, write 0, timeout 56
Requests/sec:      1.96
Transfer/sec:     347.23B

Running 30s test @ http://127.0.0.1:5050/fibonacci/9
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   108.64ms   91.61ms   1.99s    98.70%
    Req/Sec   321.54     70.42   840.00     90.56%
  111949 requests in 30.01s, 18.92MB read
  Socket errors: connect 0, read 0, write 0, timeout 42
Requests/sec:   3730.35
Transfer/sec:    645.58KB

Running 30s test @ http://127.0.0.1:5050/fibonacci/500
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   117.27ms   71.46ms   1.99s    96.81%
    Req/Sec   283.71     70.26     0.88k    87.47%
  98579 requests in 30.02s, 26.53MB read
  Socket errors: connect 0, read 0, write 0, timeout 117
Requests/sec:   3283.79
Transfer/sec:      0.88MB
'''
