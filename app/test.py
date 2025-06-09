from app import create_app
from app.models import db, Student, Staff

app = create_app()

with app.app_context():
    # Create tables if they do not exist
    db.create_all()

    print("Connected to DB.")
    print("Tables:", db.inspect(db.engine).get_table_names())

    # Now this query will work only if some data is inserted
    try:
        print("Total students:", Student.query.count())
    except Exception as e:
        print("Error during query:", e)
