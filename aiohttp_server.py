import asyncio
import aiohttp
from aiohttp import web
from fibonacci import fib


@asyncio.coroutine
def count(request):
    key = request.match_info['key']
    req = yield from aiohttp.request('get', 'http://127.0.0.1:8000/count/' + key)
    raw = yield from req.text()
    return web.Response(text=raw)


@asyncio.coroutine
def fibonacci(request):
    n = int(request.match_info['n'])
    return web.Response(text=str(fib(n)))


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
Running 30s test @ http://127.0.0.1:5050/count/key7
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.27s   312.81ms   2.00s    67.52%
    Req/Sec    38.21     45.27   300.00     88.77%
  7816 requests in 30.09s, 1.34MB read
  Socket errors: connect 0, read 13, write 0, timeout 892
Requests/sec:    259.73
Transfer/sec:     45.45KB

Running 30s test @ http://127.0.0.1:5050/fibonacci/9
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   210.29ms   96.85ms   1.98s    78.92%
    Req/Sec   136.79     71.67   710.00     72.12%
  47709 requests in 30.09s, 8.07MB read
  Socket errors: connect 0, read 45, write 0, timeout 202
Requests/sec:   1585.52
Transfer/sec:    274.53KB

Running 30s test @ http://127.0.0.1:5050/fibonacci/33
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.66s     0.00us   1.66s   100.00%
    Req/Sec     0.00      0.00     0.00    100.00%
  17 requests in 30.04s, 3.02KB read
  Socket errors: connect 0, read 0, write 0, timeout 16
Requests/sec:      0.57
Transfer/sec:     102.98B
'''
