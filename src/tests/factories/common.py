from sqlalchemy.orm import scoped_session, sessionmaker
from leaf.database import engine

Session = scoped_session(sessionmaker(autoflush=False, bind=engine))
