from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Cliente

clientes = [
    {
        "nome": "João Silva",
        "email": "joao.silva@exemplo.com"
    },
    {
        "nome": "Maria Oliveira",
        "email": "maria.oliveira@exemplo.com"
    },
    {
        "nome": "Carlos Santos",
        "email": "carlos.santos@exemplo.com"
    },
    {
        "nome": "Ana Costa",
        "email": "ana.costa@exemplo.com"
    },
    {
        "nome": "Pedro Souza",
        "email": "pedro.souza@exemplo.com"
    }
]

db = SessionLocal()

try:
    for dados in clientes:
        cliente_existente = db.query(Cliente).filter(
            Cliente.email == dados["email"]
        ).first()

        if cliente_existente:
            print(f"Cliente {dados['nome']} já cadastrado.")
            continue

        novo_cliente = Cliente(
            nome=dados["nome"],
            email=dados["email"]
        )

        db.add(novo_cliente)
        print(f"Cliente {dados['nome']} adicionado.")

    db.commit()
    print("Cadastro de clientes finalizado!")

except Exception as erro:
    db.rollback()
    print("Erro ao cadastrar clientes:", erro)

finally:
    db.close()