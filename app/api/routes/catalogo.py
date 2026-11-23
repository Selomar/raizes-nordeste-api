from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Cliente, Unidade, Produto, Estoque, Usuario
from app.api.routes.auth import obter_usuario_atual

router = APIRouter(prefix="/catalogo", tags=["Catálogo"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/clientes")
def listar_clientes(
    db: Annotated[Session, Depends(get_db)],
    usuario: Annotated[Usuario, Depends(obter_usuario_atual)],
):
    clientes = db.query(Cliente).order_by(Cliente.nome).all()
    return [{"id": c.id, "nome": c.nome, "email": c.email} for c in clientes]


@router.get("/unidades")
def listar_unidades(
    db: Annotated[Session, Depends(get_db)],
    usuario: Annotated[Usuario, Depends(obter_usuario_atual)],
):
    unidades = db.query(Unidade).order_by(Unidade.nome).all()
    return [{"id": u.id, "nome": u.nome, "endereco": u.endereco} for u in unidades]


@router.get("/produtos")
def listar_produtos(
    db: Annotated[Session, Depends(get_db)],
    usuario: Annotated[Usuario, Depends(obter_usuario_atual)],
):
    produtos = db.query(Produto).order_by(Produto.nome).all()
    return [
        {"id": p.id, "nome": p.nome, "descricao": p.descricao, "preco": float(p.preco)}
        for p in produtos
    ]


@router.get("/estoques")
def consultar_estoque(
    db: Annotated[Session, Depends(get_db)],
    usuario: Annotated[Usuario, Depends(obter_usuario_atual)],
    produto_id: int = Query(..., ge=1),
    unidade_id: int = Query(..., ge=1),
):
    estoque = db.query(Estoque).filter(
        Estoque.produto_id == produto_id,
        Estoque.unidade_id == unidade_id,
    ).first()
    if estoque is None:
        return {"produto_id": produto_id, "unidade_id": unidade_id, "quantidade": 0}
    return {
        "produto_id": estoque.produto_id,
        "unidade_id": estoque.unidade_id,
        "quantidade": estoque.quantidade,
    }
