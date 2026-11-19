from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Unidade

unidades = [
    {
        "nome": "Unidade Centro",
        "endereco": "Avenida Principal, Bairro Centro"
    },
    {
        "nome": "Unidade Norte",
        "endereco": "Rua Secundária, Bairro Norte"
    },
    {
        "nome": "Unidade Sul",
        "endereco": "Rua das Palmeiras, Bairro Sul"
    },
    {
        "nome": "Unidade Leste",
        "endereco": "Avenida Central, Bairro Leste"
    },
    {
        "nome": "Unidade Oeste",
        "endereco": "Rua das Flores, Bairro Oeste"
    }
]

db = SessionLocal()

try:
    for dados in unidades:
        unidade_existente = db.query(Unidade).filter(
            Unidade.nome == dados["nome"]
        ).first()

        if unidade_existente:
            print(f"Unidade {dados['nome']} já cadastrada.")
            continue

        nova_unidade = Unidade(
            nome=dados["nome"],
            endereco=dados["endereco"]
        )

        db.add(nova_unidade)
        print(f"Unidade {dados['nome']} adicionada.")

    db.commit()
    print("Processo de cadastro finalizado!")

except Exception as erro:
    db.rollback()
    print("Erro ao cadastrar unidades:", erro)

finally:
    db.close()