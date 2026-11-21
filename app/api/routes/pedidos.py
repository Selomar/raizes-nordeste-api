from decimal import Decimal
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4

from app.infrastructure.database import SessionLocal
from app.infrastructure.models import (
    Pedido as PedidoModel,
    Produto as ProdutoModel,
    ItemPedido as ItemPedidoModel,
    Cliente as ClienteModel,
    Unidade as UnidadeModel,
    Pagamento as PagamentoModel,
    Usuario
)
from app.schemas.pedido import (
    PedidoCriacao,
    PedidoResposta,
    PagamentoCriacao
)
from app.api.routes.auth import obter_usuario_atual
from app.infrastructure.audit import registrar_log

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_pedidos(
        db: Annotated[Session, Depends(get_db)],
        usuario: Annotated[Usuario, Depends(obter_usuario_atual)],
        canal_pedido: str = None
):
    consulta = db.query(PedidoModel)

    if usuario.perfil == "OPERADOR":
        consulta = consulta.filter(
            PedidoModel.unidade_id == usuario.unidade_id
        )

    if canal_pedido is not None:
        consulta = consulta.filter(
            PedidoModel.canal_pedido == canal_pedido
        )

    pedidos = consulta.all()

    return pedidos

@router.post("/", response_model=PedidoResposta, status_code=201)
def criar_pedido(
        dados: PedidoCriacao,
        db: Annotated[Session, Depends(get_db)],
        usuario: Annotated[Usuario, Depends(obter_usuario_atual)]
):
    if (
            usuario.perfil == "OPERADOR"
            and usuario.unidade_id != dados.unidade_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para criar pedidos nesta unidade"
        )

    total = Decimal("0.00")
    itens_pedido = []

    cliente = db.query(ClienteModel).filter(
        ClienteModel.id == dados.cliente_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    unidade = db.query(UnidadeModel).filter(
        UnidadeModel.id == dados.unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    for item in dados.itens:
        produto = db.query(ProdutoModel).filter(
            ProdutoModel.id == item.produto_id
        ).first()

        if produto is None:
            raise HTTPException(
                status_code=404,
                detail=f"Produto ID {item.produto_id} não encontrado"
            )
        subtotal = produto.preco * item.quantidade
        total += subtotal
        itens_pedido.append((item, produto))

    novo_pedido = PedidoModel(
        cliente_id=dados.cliente_id,
        unidade_id=dados.unidade_id,
        canal_pedido=dados.canal_pedido,
        status="PENDENTE",
        valor_total=total
    )
    try:
        db.add(novo_pedido)
        db.flush()

        for item, produto in itens_pedido:
            novo_item = ItemPedidoModel(
                pedido_id=novo_pedido.id,
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=produto.preco
            )
            db.add(novo_item)
        db.commit()
        db.refresh(novo_pedido)

        registrar_log(
            usuario_id=usuario.id,
            acao="CRIAR_PEDIDO",
            entidade="PEDIDO",
            entidade_id=novo_pedido.id,
            resultado="SUCESSO"
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao salvar o pedido no banco de dados"
        )

    return {
        "id": novo_pedido.id,
        "cliente_id": novo_pedido.cliente_id,
        "unidade_id": novo_pedido.unidade_id,
        "canal_pedido": novo_pedido.canal_pedido,
        "status": novo_pedido.status,
        "valor_total": float(novo_pedido.valor_total)
    }

@router.post("/{pedido_id}/pagamento", status_code=200)
def processar_pagamento(
        pedido_id: int,
        dados: PagamentoCriacao,
        db: Annotated[Session, Depends(get_db)],
        usuario: Annotated[Usuario, Depends(obter_usuario_atual)]
):
    pedido = db.query(PedidoModel).filter(
        PedidoModel.id == pedido_id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if (
            usuario.perfil == "OPERADOR"
            and usuario.unidade_id != pedido.unidade_id
    ):
        registrar_log(
            usuario_id=usuario.id,
            acao="ACESSO_NEGADO",
            entidade="PEDIDO",
            entidade_id=pedido.id,
            resultado="FALHA"
        )

        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para processar pagamentos desta unidade"
        )

    if pedido.status != "PENDENTE":
        raise HTTPException(
            status_code=409,
            detail="Este pedido não está pendente de pagamento"
        )

    if dados.aprovado:
        status_pagamento = "APROVADO"
        status_pedido = "PAGO"
    else:
        status_pagamento = "RECUSADO"
        status_pedido = "PAGAMENTO_RECUSADO"

    novo_pagamento = PagamentoModel(
        pedido_id=pedido.id,
        valor=pedido.valor_total,
        status=status_pagamento,
        identificador_externo=str(uuid4())
    )

    try:
        pedido.status = status_pedido
        db.add(novo_pagamento)
        db.commit()
        db.refresh(pedido)

        registrar_log(
            usuario_id=usuario.id,
            acao="PROCESSAR_PAGAMENTO",
            entidade="PAGAMENTO",
            entidade_id=novo_pagamento.id,
            resultado=status_pagamento
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao processar o pagamento"
        )

    return {
        "pedido_id": pedido.id,
        "status_pedido": pedido.status,
        "status_pagamento": status_pagamento,
        "valor": float(pedido.valor_total),
        "identificador_externo": novo_pagamento.identificador_externo
    }