from app import db
import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy import DateTime

class BaseModel(db.Model):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):

        for attr in ('created_at', 'updated_at'):
            val = getattr(self, attr)
            if isinstance(val, str):
                setattr(self, attr, datetime.fromisoformat(val))
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

        for key in ('created_at', 'updated_at'):
            if key in data and isinstance(data[key], str):
                try:
                    data[key] = datetime.fromisoformat(data[key])
                except ValueError:
                    # Valeurs par défaut si la conversion échoue
                    default_dates = {
                        'created_at': '2025-07-25T16:14:41.822619',
                        'updated_at': '2025-07-25T16:14:41.822623',
                    }
                    if key in default_dates:
                        data[key] = datetime.fromisoformat(default_dates[key])

        # Attribution des attributs uniquement s'ils existent dans la classe
        for key, value in data.items():
            if hasattr(obj, key):  # ici, on vérifie sur l'instance obj
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

