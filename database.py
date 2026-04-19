from models import Sessionlocal

def get_db():
    db= Sessionlocal()
    try :
        yield db     #! yield = “give resource now, clean it up later”
    finally:
        db.close()