from pydantic import BaseModel, Field

class ItemPedidoCriacao(BaseModel):
    produto_id: int = Field(gt=0)
    quantidade: int = Field(gt=0)

class PedidoCriacao(BaseModel):
    cliente_id: int = Field(gt=0)
    unidade_id: int = Field(gt=0)
    canal_pedido: str = Field(
        pattern="^(APP|TOTEM|BALCAO|PICKUP|WEB)$"
    )
    itens: list[ItemPedidoCriacao] = Field(min_length=1)

class PedidoResposta(BaseModel):
    id: int
    cliente_id: int
    unidade_id: int
    canal_pedido: str
    status: str
    valor_total: float

class PagamentoCriacao(BaseModel):
    aprovado: bool