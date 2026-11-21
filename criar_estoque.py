
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Estoque, Produto, Unidade


db = SessionLocal()

try:
    produtos = db.query(Produto).all()
    unidades = db.query(Unidade).all()

    for unidade in unidades:
        for produto in produtos:

            estoque_existente = db.query(Estoque).filter(
                Estoque.produto_id == produto.id,
                Estoque.unidade_id == unidade.id
            ).first()

            if estoque_existente:
                print(
                    f"Estoque de {produto.nome} na "
                    f"{unidade.nome} já cadastrado."
                )
                continue

            novo_estoque = Estoque(
                produto_id=produto.id,
                unidade_id=unidade.id,
                quantidade=20
            )

            db.add(novo_estoque)

            print(
                f"Estoque de {produto.nome} na "
                f"{unidade.nome} adicionado: 20 unidades."
            )

    db.commit()
    print("Cadastro de estoque finalizado!")

except Exception as erro:
    db.rollback()
    print("Erro ao cadastrar estoque:", erro)

finally:
    db.close()
