from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Usuario
from app.infrastructure.security import (
    verificar_senha,
    criar_token_acesso,
    obter_id_usuario
)
from app.schemas.auth import LoginRequest, TokenResposta
from app.infrastructure.audit import registrar_log


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=TokenResposta)
def login(
    dados: LoginRequest,
    db: Annotated[Session, Depends(get_db)]
):
    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario or not verificar_senha(
            dados.senha,
            usuario.senha_hash
    ):
        registrar_log(
            usuario_id=usuario.id if usuario else None,
            acao="LOGIN",
            entidade="USUARIO",
            entidade_id=usuario.id if usuario else None,
            resultado="FALHA"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )

    if not usuario.ativo:
        registrar_log(
            usuario_id=usuario.id,
            acao="LOGIN",
            entidade="USUARIO",
            entidade_id=usuario.id,
            resultado="FALHA"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    token = criar_token_acesso(usuario.id)

    registrar_log(
        usuario_id=usuario.id,
        acao="LOGIN",
        entidade="USUARIO",
        entidade_id=usuario.id,
        resultado="SUCESSO"
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def obter_usuario_atual(
    usuario_id: Annotated[int, Depends(obter_id_usuario)],
    db: Annotated[Session, Depends(get_db)]
):
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario or not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo"
        )

    return usuario

@router.get("/me")
def usuario_logado(
    usuario: Annotated[Usuario, Depends(obter_usuario_atual)]
):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil,
        "unidade_id": usuario.unidade_id
    }