from models import Sessionlocal,Job

db = Sessionlocal()
db.add(Job(title="Backend Engineer", company="StartupXYZ", 
            role="engineer", location="remote"))
db.commit()
db.close()