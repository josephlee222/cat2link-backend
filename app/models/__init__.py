from app.extensions import db
from app.models import User, Category, Media, Project

# Explicitly exposing them makes it clear to linters and the app
__all__ = ['db', 'User', 'Category', 'Media', 'Project']