from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import Functions
import QueryEngine
import socketio
from socket_manager import sio
import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = socketio.ASGIApp(sio, other_asgi_app=app)

@sio.event
async def connect(sid, environ):
    print('Connected', sid)

@sio.event
async def disconnect(sid):
    print('Disconnected', sid)

@sio.event
async def get_response(sid, conversation, func_sig=None):
    conv = jsonable_encoder(conversation)
    if (func_sig == None):
        func_sig = Functions.get_function(conv[-1]['content'])
    await sio.emit('get_response_option', {'function': func_sig})

    async def query_and_emit():
        response = await QueryEngine.query(func_sig, conv)
        await sio.emit('get_response_callback', response)
    asyncio.create_task(query_and_emit())

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8111)