from app.database import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='projects')
    media = db.relationship('Media', back_populates='projects')

    def __repr__(self):
        return f"<Project {self.name}>"