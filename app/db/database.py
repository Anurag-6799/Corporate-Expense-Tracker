from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# The Engine: The actual communication pipeline to PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# autocommit=False ensures transactions aren't saved until we explicitly call db.commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The Base Class: All our future database models will inherit from this
class Base(DeclarativeBase):
    pass

# The Dependency (The Yield Pattern)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # This guarantees the connection returns to the pool