from app.models import Complaint

print(list(Complaint.__table__.columns.keys()))
