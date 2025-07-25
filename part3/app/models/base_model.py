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

        for key, value in data.items():
            if not hasattr(obj, key):
                continue

            expected_type = cls.__annotations__.get(key, None)

        # Si le champ attendu est un datetime, et que la valeur est une chaîne
            if expected_type and isinstance(value, expected_type):
                setattr(obj, key, value)
                continue


            # Cas spécial des datetime: convertir la chaîne en datetime si possible
            if expected_type is datetime and isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    print(f"[WARN] Mauvais format pour '{key}': {value}")
                    continue  # on ignore la conversion ratée

        # Cas des str: convertir les int, bool, etc., en str
            elif expected_type is str and value is not None:
                value = str(value)

        # On injecte la valeur (convertie ou non)
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

