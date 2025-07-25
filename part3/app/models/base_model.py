from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def to_dict(self, seen=None):
        if seen is None:
            seen = set()

        if id(self) in seen:
            return f"<Recursion detected for object {self.id}>"
        seen.add(id(self))

        result = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            if isinstance(value, BaseModel):
                result[key] = value.to_dict(seen)
            elif isinstance(value, list):
                result[key] = [item.to_dict(seen) if isinstance(item, BaseModel) else item for item in value]
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data):
        obj = cls()

        for key, value in data.items():
            if hasattr(cls, key):
                if key in ('created_at', 'updated_at') and isinstance(value, str):
                    value = datetime.fromisoformat(value)
                setattr(obj, key, value)
        return obj

    def update(self, data):
        updated = False
        for key, value in data.items():
            if hasattr(self, "allowed_update_fields") and key in self.allowed_update_fields:
                setattr(self, key, value)
                updated = True
        if updated:
            self.save()


    def __repr__(self):
        return f"{self.__class__.__name}(id='{self.id}', created_at='{self.created_at}', updated_at='{self.updated_at}')"

    def __str__(self):
        return self.__repr__()

