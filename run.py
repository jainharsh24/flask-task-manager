
from app import create_app , db, ensure_schema_updates

from app.models import Task,User

app = create_app()

with app.app_context():
    db.create_all()
    ensure_schema_updates(app)

if __name__ =="__main__":
    app.run(debug=True)
