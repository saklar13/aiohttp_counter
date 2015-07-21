import asyncio
from aiohttp import web
from collections import Counter


@asyncio.coroutine
def count(request, counter=Counter()):
    key = request.match_info['key']
    counter[key] += 1
    asyncio.sleep(0.5)
    return web.Response(text=str(counter[key]))


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
f = loop.create_server(handler, '0.0.0.0', 8000)
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
Running 30s test @ http://127.0.0.1:8000/count/key1
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   112.23ms   84.96ms   1.97s    98.92%
    Req/Sec   299.01     77.80     0.90k    89.74%
  105928 requests in 30.10s, 18.20MB read
  Socket errors: connect 0, read 21, write 0, timeout 87
Requests/sec:   3519.54
Transfer/sec:    619.38KB

Running 30s test @ http://127.0.0.1:8000/fibonacci/9
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   103.88ms   73.52ms   1.99s    99.08%
    Req/Sec   328.06     62.65     0.92k    90.09%
  114137 requests in 30.10s, 19.29MB read
  Socket errors: connect 0, read 0, write 0, timeout 86
Requests/sec:   3792.08
Transfer/sec:    656.43KB

  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   103.58ms   73.17ms   1.99s    99.08%
    Req/Sec   325.68     77.80     0.86k    91.07%
  114469 requests in 30.10s, 20.12MB read
  Socket errors: connect 0, read 0, write 0, timeout 87
Requests/sec:   3803.06
Transfer/sec:    684.50KB

Running 30s test @ http://127.0.0.1:8000/fibonacci/440
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   113.05ms   72.26ms   1.98s    98.26%
    Req/Sec   289.35     76.50     0.87k    88.24%
  102406 requests in 30.01s, 26.19MB read
  Socket errors: connect 0, read 0, write 0, timeout 120
Requests/sec:   3411.97
Transfer/sec:      0.87MB
'''
