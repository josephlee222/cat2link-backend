from app.extensions import db

class Media(db.Model):
    __tablename__ = "multimedia"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    url = db.Column(db.String(1024), nullable=False)

    # 1 = Image
    # 2 = Video
    # Extendable to accomodate more types of media
    media_type = db.Column(db.Integer, nullable=False, default=1)
    alt_text = db.Column(db.String(512), nullable=False)

    # Links back to the category property in Project
    projects = db.relationship('Project', back_populates='media')

    def get_summary(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "url": self.url,
            "media_type": self.media_type,
            "alt_text": self.alt_text
        }

    def __repr__(self):
            return f"<Media {self.alt_text}>"