import os
from aiohttp import web
from livekit import api

LK_URL = "wss://chatgptme-sp76gr03.livekit.cloud"
LK_API_KEY = "APIRBVfLnF2B2WF"
LK_API_SECRET = "cEqJAr8wQHkRSZrM7o8oHY2HSguTn54gC5XBIxAs3pF"
ROOM_NAME = "helios-dedicated-stream"

async def handle_index(request):
    token = api.AccessToken(LK_API_KEY, LK_API_SECRET) \
        .with_identity("viewer-" + os.urandom(4).hex()) \
        .with_name("Viewer") \
        .with_grants(api.VideoGrants(room_join=True, room=ROOM_NAME)) \
        .to_jwt()
        
    with open('index.html', 'r') as f:
        html = f.read()
        
    html = html.replace('__TOKEN__', token)
    html = html.replace('__URL__', LK_URL)
    
    return web.Response(text=html, content_type='text/html')

app = web.Application()
app.router.add_get('/', handle_index)

if __name__ == '__main__':
    web.run_app(app, port=8080)
