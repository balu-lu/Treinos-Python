import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

# importação do modelo de usuários do database.py
from database import get_db, UsuarioDB

security = HTTPBasic()


def verificar_auth(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    # busca o usuário no banco pelo username
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.username == credentials.username).first()

    # se o user não existir
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário incorreto ou não encontrado",
            headers={"WWW-Authenticate": "Basic"},
        )

    # verifica a senha
    is_pass_ok = secrets.compare_digest(credentials.password, usuario.password)

    if not is_pass_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Retorna o nome do usuário validado
    return usuario.username
