from getpass import getpass

from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Usuario
from app.infrastructure.security import gerar_hash_senha

nome = input("Nome do administrador: ")
email = input("E-mail do administrador: ").strip().lower()
senha = getpass("Digite a nova senha: ")
confirmar_senha = getpass("Digite novamente a senha: ")

if senha != confirmar_senha:
    print("As senhas não coincidem. Execute novamente.")
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
        print("Já existe um usuário cadastrado com esse e-mail.")
    else:
        senha_hash = gerar_hash_senha(senha)

        novo_admin = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            perfil="ADMIN",
            unidade_id=None,
            ativo=True
        )

        db.add(novo_admin)
        db.commit()

        print("Administrador cadastrado com sucesso!")

except Exception as erro:
    db.rollback()
    print("Erro ao cadastrar administrador:", erro)

finally:
    db.close()