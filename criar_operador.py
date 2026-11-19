from getpass import getpass

from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Usuario, Unidade
from app.infrastructure.security import gerar_hash_senha

nome = input("Nome do operador: ")
email = input("E-mail do operador: ").strip().lower()

unidade_id = int(input("ID da unidade: "))

senha = getpass("Digite a senha: ")
confirmar_senha = getpass("Digite novamente a senha: ")

if senha != confirmar_senha:
    print("As senhas não coincidem.")
    exit()

if not senha:
    print("A senha não pode ficar vazia.")
    exit()

db = SessionLocal()

try:
    usuario_existente = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if usuario_existente:
        print("Já existe um usuário com esse e-mail.")
        exit()

    unidade = db.query(Unidade).filter(
        Unidade.id == unidade_id
    ).first()

    if unidade is None:
        print("Unidade não encontrada.")
        exit()

    senha_hash = gerar_hash_senha(senha)

    novo_operador = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        perfil="OPERADOR",
        unidade_id=unidade_id,
        ativo=True
    )

    db.add(novo_operador)
    db.commit()

    print("Operador cadastrado com sucesso!")

finally:
    db.close()