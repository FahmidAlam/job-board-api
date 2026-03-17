
import models

db = models.Sessionlocal()
db.add(models.Job(title="Backend Engineer", company="StartupXYZ", 
            role="engineer", location="remote"))
db.commit()
db.close()