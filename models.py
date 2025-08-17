from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    preferred_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(200), nullable=False)
    health_goals = db.Column(db.Text)  # JSON string
    chronic_conditions = db.Column(db.Text)  # JSON string
    wearables = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    conversations = db.relationship('Conversation', backref='member', lazy=True)
    timeline_events = db.relationship('TimelineEvent', backref='member', lazy=True)
    health_metrics = db.relationship('HealthMetric', backref='member', lazy=True)
    decisions = db.relationship('Decision', backref='member', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'preferred_name': self.preferred_name,
            'age': self.age,
            'gender': self.gender,
            'location': self.location,
            'occupation': self.occupation,
            'health_goals': json.loads(self.health_goals) if self.health_goals else [],
            'chronic_conditions': json.loads(self.chronic_conditions) if self.chronic_conditions else [],
            'wearables': json.loads(self.wearables) if self.wearables else [],
            'created_at': self.created_at.isoformat()
        }

class TeamMember(db.Model):
    __tablename__ = 'team_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(200), nullable=False)
    communication_style = db.Column(db.Text, nullable=False)

    # Relationships
    conversations = db.relationship('Conversation', backref='team_member', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'specialty': self.specialty,
            'communication_style': self.communication_style
        }

class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    team_member_id = db.Column(db.Integer, db.ForeignKey('team_members.id'), nullable=True)
    sender = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    month = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'team_member_id': self.team_member_id,
            'sender': self.sender,
            'message': self.message,
            'category': self.category,
            'timestamp': self.timestamp.isoformat(),
            'month': self.month
        }

class TimelineEvent(db.Model):
    __tablename__ = 'timeline_events'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    outcome = db.Column(db.Text, nullable=False)
    team_members = db.Column(db.Text)  # JSON string
    response_time = db.Column(db.String(100))
    time_to_resolution = db.Column(db.String(100))
    friction_points = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'date': self.date.isoformat(),
            'title': self.title,
            'category': self.category,
            'status': self.status,
            'description': self.description,
            'outcome': self.outcome,
            'team_members': json.loads(self.team_members) if self.team_members else [],
            'response_time': self.response_time,
            'time_to_resolution': self.time_to_resolution,
            'friction_points': self.friction_points
        }

class HealthMetric(db.Model):
    __tablename__ = 'health_metrics'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)  # hrv, recovery_score, resting_heart_rate
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'metric_type': self.metric_type,
            'value': self.value,
            'date': self.date.isoformat()
        }

class Decision(db.Model):
    __tablename__ = 'decisions'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    decision_type = db.Column(db.String(50), nullable=False)
    decision = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    triggered_by = db.Column(db.Text, nullable=False)
    outcome = db.Column(db.Text, nullable=False)
    evidence = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'date': self.date.isoformat(),
            'type': self.decision_type,
            'decision': self.decision,
            'reason': self.reason,
            'triggered_by': self.triggered_by,
            'outcome': self.outcome,
            'evidence': self.evidence
        }

class TeamMetric(db.Model):
    __tablename__ = 'team_metrics'

    id = db.Column(db.Integer, primary_key=True)
    team_member_id = db.Column(db.Integer, db.ForeignKey('team_members.id'), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    metric_type = db.Column(db.String(50), nullable=False, default='consultation_hours')

    def to_dict(self):
        return {
            'id': self.id,
            'team_member_id': self.team_member_id,
            'hours': self.hours,
            'metric_type': self.metric_type
        }
