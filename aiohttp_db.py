import asyncio
from aiohttp import web
from collections import Counter


@asyncio.coroutine
def count(request, counter=Counter()):
    key = request.match_info['key']
    counter[key] += 1
    yield from asyncio.sleep(0.5)
    return web.Response(text=str(counter[key]))


app = web.Application()
app.router.add_route('GET', '/count/{key}', count)


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