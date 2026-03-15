import os
import json
from aiohttp import web
from livekit import api
from super_project_engine import SuperProjectEngine

LK_URL = "wss://chatgptme-sp76gr03.livekit.cloud"
LK_API_KEY = "APIRBVfLnF2B2WF"
LK_API_SECRET = "cEqJAr8wQHkRSZrM7o8oHY2HSguTn54gC5XBIxAs3pF"
ROOM_NAME = "helios-dedicated-stream"

engine = SuperProjectEngine()

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

async def handle_expand_prompt(request):
    data = await request.json()
    seed = data.get('seed', '')
    if not seed:
        return web.json_response({"error": "No seed provided"}, status=400)
    try:
        result = await engine.expand_prompt(seed)
        return web.json_response(result)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

app = web.Application()
app.router.add_get('/', handle_index)
app.router.add_post('/api/expand', handle_expand_prompt)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    web.run_app(app, host='0.0.0.0', port=port)
