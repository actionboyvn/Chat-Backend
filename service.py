from fastapi import Body, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from typing import List
import QueryEngine
import ImageAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"error_details": exc.errors(), "example_request": {
            "conversation": [
                {"role": "system", "content": "You an a helpful assistant."},
                {"role": "assistant", "content": "How can I help today?"},
                {"role": "user", "content": "What is a PESEL number?"}
            ]
        }}),
    )

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]

class ImagePrompt(BaseModel):
    content: str

@app.post("/assistant_service/get_response")
async def get_response(conversation: Conversation = Body(...)):
    return await QueryEngine.query(jsonable_encoder(conversation))

@app.post("/assistant_service/generate_image")
async def get_response(prompt: ImagePrompt = Body(...)):
    return await ImageAgent.generate(jsonable_encoder(prompt))

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8085)