from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Produto

produtos = [
    {"nome": "Cuscuz nordestino", "descricao": "Cuscuz tradicional nordestino", "preco": 12.00},
    {"nome": "Tapioca de queijo", "descricao": "Tapioca recheada com queijo", "preco": 10.00},
    {"nome": "Bolo de milho", "descricao": "Fatia de bolo de milho", "preco": 6.00},
    {"nome": "Baião de dois", "descricao": "Prato tradicional nordestino", "preco": 18.00},
    {"nome": "Pão de queijo", "descricao": "Pão de queijo tradicional", "preco": 5.00},
    {"nome": "Café regional", "descricao": "Café tradicional", "preco": 5.00},
    {"nome": "Misto", "descricao": "Sanduíche misto quente", "preco": 9.00},
    {"nome": "Pingado", "descricao": "Café com leite", "preco": 6.00}
]

db = SessionLocal()

try:
    for dados in produtos:
        produto_existente = db.query(Produto).filter(
            Produto.nome == dados["nome"]
        ).first()

        if produto_existente:
            print(f"Produto {dados['nome']} já cadastrado.")
            continue

        novo_produto = Produto(
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"]
        )

        db.add(novo_produto)
        print(f"Produto {dados['nome']} adicionado.")
    db.commit()
    print("Cadastro de produtos finalizado!")

except Exception as erro:
    db.rollback()
    print("Erro ao cadastrar produtos:", erro)

finally:
    db.close()