from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routes.pedidos import router as pedidos_router
from app.api.routes.auth import router as auth_router

app = FastAPI()

@app.exception_handler(HTTPException)
async def tratar_erro_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": {
                "codigo": exc.status_code,
                "mensagem": exc.detail
            }
        },
        headers=exc.headers
    )

@app.exception_handler(RequestValidationError)
async def tratar_erro_validacao(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "erro": {
                "codigo": 422,
                "mensagem": "Os dados enviados são inválidos",
                "detalhes": exc.errors()
            }
        }
    )

app.include_router(pedidos_router)
app.include_router(auth_router)

@app.get("/")
def inicio():
    return {"mensagem": "API Rede Raízes do Nordeste funcionando!"}