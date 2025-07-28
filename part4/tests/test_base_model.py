from app.models.base_model import BaseModel
from datetime import datetime, timedelta
import time

def test_basemodel_creation():
    model = BaseModel()
    assert isinstance(model.id, str)
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)
    print("Création de BaseModel OK")

def test_basemodel_save_updates_updated_at():
    model = BaseModel()
    old_updated_at = model.updated_at
    time.sleep(0.01)  # Assure un changement de timestamp
    model.save()
    assert model.updated_at > old_updated_at
    print("Méthode save() OK")

def test_basemodel_to_dict_and_from_dict():
    model = BaseModel()
    d = model.to_dict()
    assert d["id"] == model.id
    assert d["created_at"] == model.created_at.isoformat()
    assert d["updated_at"] == model.updated_at.isoformat()

    # Teste la désérialisation
    new_model = BaseModel.from_dict(d)
    assert new_model.id == model.id
    assert new_model.created_at == model.created_at
    assert new_model.updated_at == model.updated_at
    print("Méthodes to_dict() et from_dict() OK")

def test_basemodel_update():
    model = BaseModel()
    old_updated_at = model.updated_at
    data = {"id": "new_id"}
    time.sleep(0.01)
    model.update(data)
    assert model.id == "new_id"
    assert model.updated_at > old_updated_at
    print("Méthode update() OK")

if __name__ == "__main__":
    test_basemodel_creation()
    test_basemodel_save_updates_updated_at()
    test_basemodel_to_dict_and_from_dict()
    test_basemodel_update()
    print("Tous les tests unitaires BaseModel sont passés !")

