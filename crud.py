from sqlalchemy import create_engine, String, Boolean, Select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

dir_atual = Path(__file__).parent
PATH_TO_BD = dir_atual / 'bd_usuarios.sqlite'

class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True)
    nm_usuario : Mapped[str] = mapped_column(String(30))
    senha : Mapped[str] = mapped_column(String(128))
    email : Mapped[str] = mapped_column(String(30))
    acesso_gestor: Mapped[bool] = mapped_column(Boolean(), default= False)

    def __repr__(self):
        return f'Usuário({self.id}), Nome: {self.nm_usuario}'

    def define_password(self, password):
        self.senha = generate_password_hash(password)

    def verifica_password(self, password):
        return check_password_hash(self.senha, password)


engine = create_engine(f'sqlite:///{PATH_TO_BD}')
Base.metadata.create_all(bind=engine)


##CRUD DO BD

#Session conecta com o bd para modificações


def create_usuario(nm_usuario,senha, email,**kargs):
    
    with Session(bind=engine) as session:
        usuario = Usuario(
            nm_usuario = nm_usuario,
            email =email,
            **kargs
        )
        usuario.define_password(senha)
        session.add(usuario)
        session.commit()


def read_usuarios():
    with Session(bind=engine) as session:

        select_usuarios = Select(Usuario)
        usuarios = session.execute(select_usuarios).fetchall()
        usuarios = [user[0] for user in usuarios] #descompressao de lista
        return usuarios


def get_by_id(id):

    with Session(bind = engine) as session:
        get_id = Select(Usuario).filter_by(id=id)
        usuario = session.execute(get_id).fetchall()
        return usuario



def mod_usuario(id, **kargs):

    with Session(bind = engine) as session:
        get_usuario = Select(Usuario).filter_by(id=id)
        usuarios = session.execute(get_usuario).fetchall()
        for user in usuarios:
            for key, value in kargs.items():
                if key == 'senha':
                    user[0].define_password(value)
                else:
                    setattr(user[0], key, value)

        session.commit()


def delete_usuario(id):
    with Session(bind = engine) as session:
        delete_usuario = Select(Usuario).filter_by(id=id)
        usuarios = session.execute(delete_usuario).fetchall()
        for user in usuarios:
            session.delete(user[0])

        session.commit()


if __name__ == '__main__':
    mod_usuario(id=1, senha='senha111')