from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric, ForeignKey, CheckConstraint, Boolean, DateTime, func, UniqueConstraint

class Pedido(Base):
    __tablename__ = "pedidos"
    __table_args__ = (
        CheckConstraint(
            "canal_pedido IN ('APP', 'TOTEM', 'BALCAO', 'PICKUP', 'WEB')",
            name="ck_pedidos_canal"
        ),
        CheckConstraint(
            "status IN ('PENDENTE', 'PAGO', 'PAGAMENTO_RECUSADO', 'CANCELADO')",
            name="ck_pedidos_status"
        ),
        CheckConstraint(
            "valor_total >= 0",
            name="ck_pedidos_valor"
        ),
    )
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"),
        nullable=False
    )

    unidade_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=False
    )

    canal_pedido: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    valor_total: Mapped[float] = mapped_column(
        Numeric(10,2),
        nullable=False
    )

class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

class Unidade(Base):
    __tablename__ = "unidades"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    endereco: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

class Produto(Base):
    __tablename__ = "produtos"
    __table_args__ = (
        CheckConstraint("preco > 0"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descricao: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    preco: Mapped[float] = mapped_column(
        Numeric(10,2),
        nullable=False
    )

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    __table_args__ = (
        CheckConstraint("quantidade > 0"),
        CheckConstraint("preco_unitario >= 0"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    preco_unitario: Mapped[float] = mapped_column(
        Numeric(10,2),
        nullable=False
    )

class Pagamento(Base):
    __tablename__ = "pagamentos"
    __table_args__ = (
        CheckConstraint("valor >= 0"),
        CheckConstraint("status IN ('APROVADO', 'RECUSADO')"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False,
        unique=True
    )

    valor: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    identificador_externo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint("perfil IN ('ADMIN', 'OPERADOR')"),
        CheckConstraint(
            "(perfil = 'ADMIN') OR "
            "(perfil = 'OPERADOR' AND unidade_id IS NOT NULL)"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    unidade_id: Mapped[int | None] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    perfil: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True
    )

    acao: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entidade: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    entidade_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    resultado: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    data_hora: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

class Estoque(Base):
    __tablename__ = "estoques"
    __table_args__ = (
        CheckConstraint("quantidade >= 0"),
        UniqueConstraint(
            "produto_id",
            "unidade_id",
            name="uq_estoque_produto_unidade"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    produto_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )

    unidade_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("unidades.id"),
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )