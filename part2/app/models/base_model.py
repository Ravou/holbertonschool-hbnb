import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, id=None, created_at=None, updated_at=None):
        self.__id = id or str(uuid.uuid4())
        self.__created_at = created_at or datetime.now()
        self.__updated_at = updated_at or datetime.now()

    def _save(self):
        self.updated_at = datetime.now()

    def __to_dict(self):
        return {
                "id": self.id,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
                }

    @classmethod
    def __from_dict(cls, data):
        return cls(
                id=data.get("id"),
                created_at=datetime.fromisoformat(data.get("created_at")) if "created_at" in data else None,
                updated_at=datetime.fromisoformat(data.get("updated_at")) if "updated_at" in data else None
                )

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"BaseModel(id='{self.id}', created_at='{self.created_at.isoformat()}', updated_at='{self.updated_at.isoformat()}')"

    def __str__(self):
        return self.__repr__()

