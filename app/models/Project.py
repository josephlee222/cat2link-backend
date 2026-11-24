from app.extensions import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    short_description = db.Column(db.Text(), nullable=False, default="Project short description")
    url = db.Column(db.String(1024), nullable=False)
    year = db.Column(db.Integer, nullable=False, default=2024)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='projects')
    media = db.relationship('Media', back_populates='projects')

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "short_description": self.short_description,
            "url": self.url,
            "year": self.year,
            "category_id": self.category_id,
            "category": self.category.get_summary() if self.category else None,
            "media": [m.get_summary() for m in self.media]
        }

    def get_summary(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "short_description": self.short_description,
            "url": self.url,
            "year": self.year,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None
        }

    def __repr__(self):
        return f"<Project {self.name}>"