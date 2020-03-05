from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class DBHelper:
    """DB helper class"""

    @staticmethod
    def add(entity):
        """Add entity to db"""
        db.session.add(entity)
        db.session.commit()

    @staticmethod
    def delete(entity):
        """Delete entity from db"""
        db.session.delete(entity)
        db.session.commit()


class User(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), default='User')
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    stories = db.relationship('Story', backref='user', lazy=True)

    def set_password(self, password):
        """Set password on register"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify user password"""
        return check_password_hash(self.password, password)

    @staticmethod
    def register(password, **kwargs):
        """Register user"""
        user = User(**kwargs)
        user.set_password(password)
        DBHelper.add(user)
        return user

    @staticmethod
    def get_and_auth_user(email, password):
        """Get and authenticate user"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None


class Story(db.Model):
    """Story model"""
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    summary = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(255), nullable=False)
    complexity = db.Column(db.String(255), nullable=False)
    estimated_hrs = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255), default='Pending')

    @staticmethod
    def create(**kwargs):
        """Create story on db"""
        story = Story(**kwargs)
        DBHelper.add(story)
        return story

    def get_attributes(self):
        return {
            'id': self.id,
            'created_by': self.created_by,
            'summary': self.summary,
            'description': self.description,
            'type': self.type,
            'complexity': self.complexity,
            'estimated_hrs': self.estimated_hrs,
            'cost': self.cost,
            'status': self.status
        }


def seed_db():
    pass
