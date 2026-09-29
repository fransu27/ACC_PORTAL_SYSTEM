from app import create_app, db
from app.models import Scholarship

app = create_app()

with app.app_context():
    if Scholarship.query.count() == 0:
        db.session.add_all([
            Scholarship(
                name="ACC Academic Scholarship",
                description="For students who meet the academic scholarship criteria.",
            ),
            Scholarship(
                name="ACC Financial Assistance Scholarship",
                description="For qualified students who need financial assistance.",
            ),
        ])
        db.session.commit()
        print("Sample scholarships created.")
    else:
        print("Scholarships already exist.")
