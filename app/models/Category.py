from app.database import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    # Links back to the category property in Project
    projects = db.relationship('Project', back_populates='category')

    def __repr__(self):
        return f"<Category {self.name}>"