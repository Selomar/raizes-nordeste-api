import logging

from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import LogAuditoria

logger = logging.getLogger(__name__)

def registrar_log(
    usuario_id: int | None,
    acao: str,
    entidade: str,
    entidade_id: int | None,
    resultado: str
):
    db = SessionLocal()

    try:
        novo_log = LogAuditoria(
            usuario_id=usuario_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            resultado=resultado
        )

        db.add(novo_log)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Falha ao registrar evento de auditoria")

    finally:
        db.close()