"""
Скрипт для заполнения БД тестовыми данными
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy.orm import sessionmaker
from src.infrastructure.database import engine, Base
from src.infrastructure.models import Building, Activity, Organization, OrganizationPhone, OrganizationActivity

# Создаем таблицы
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # === Здания ===
    buildings = [
        Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.751244, longitude=37.618423),
        Building(address="г. Москва, ул. Тверская 15", latitude=55.760244, longitude=37.608423),
        Building(address="г. Москва, ул. Блюхера, 32/1", latitude=55.820244, longitude=37.658423),
        Building(address="г. Санкт-Петербург, Невский проспект 10", latitude=59.934244, longitude=30.335423),
        Building(address="г. Екатеринбург, ул. Малышева 51", latitude=56.838244, longitude=60.605423),
    ]
    db.add_all(buildings)
    db.commit()
    
    # === Деятельности (дерево) ===
    # Уровень 1
    food = Activity(name="Еда", level=1, parent_id=None)
    auto = Activity(name="Автомобили", level=1, parent_id=None)
    db.add_all([food, auto])
    db.commit()
    
    # Уровень 2
    meat = Activity(name="Мясная продукция", level=2, parent_id=food.id)
    dairy = Activity(name="Молочная продукция", level=2, parent_id=food.id)
    trucks = Activity(name="Грузовые", level=2, parent_id=auto.id)
    cars = Activity(name="Легковые", level=2, parent_id=auto.id)
    db.add_all([meat, dairy, trucks, cars])
    db.commit()
    
    # Уровень 3
    parts = Activity(name="Запчасти", level=3, parent_id=cars.id)
    accessories = Activity(name="Аксессуары", level=3, parent_id=cars.id)
    db.add_all([parts, accessories])
    db.commit()
    
    # === Организации ===
    organizations = [
        Organization(name="ООО 'Рога и Копыта'", building_id=buildings[0].id),
        Organization(name="АО 'Молочный комбинат'", building_id=buildings[1].id),
        Organization(name="ИП 'Мясник'", building_id=buildings[2].id),
        Organization(name="ООО 'Автозапчасти'", building_id=buildings[3].id),
        Organization(name="ООО 'Грузовичкоф'", building_id=buildings[4].id),
        Organization(name="Магазин 'Продукты'", building_id=buildings[0].id),
    ]
    db.add_all(organizations)
    db.commit()
    
    # === Телефоны организаций ===
    phones = [
        OrganizationPhone(organization_id=organizations[0].id, phone="2-222-222"),
        OrganizationPhone(organization_id=organizations[0].id, phone="8-923-666-13-13"),
        OrganizationPhone(organization_id=organizations[1].id, phone="3-333-333"),
        OrganizationPhone(organization_id=organizations[2].id, phone="8-900-555-35-35"),
        OrganizationPhone(organization_id=organizations[3].id, phone="8-812-123-45-67"),
        OrganizationPhone(organization_id=organizations[4].id, phone="8-343-987-65-43"),
        OrganizationPhone(organization_id=organizations[5].id, phone="2-111-111"),
    ]
    db.add_all(phones)
    db.commit()
    
    # === Связь организаций с деятельностями ===
    org_activities = [
        OrganizationActivity(organization_id=organizations[0].id, activity_id=meat.id),
        OrganizationActivity(organization_id=organizations[0].id, activity_id=dairy.id),
        OrganizationActivity(organization_id=organizations[1].id, activity_id=dairy.id),
        OrganizationActivity(organization_id=organizations[2].id, activity_id=meat.id),
        OrganizationActivity(organization_id=organizations[3].id, activity_id=parts.id),
        OrganizationActivity(organization_id=organizations[3].id, activity_id=accessories.id),
        OrganizationActivity(organization_id=organizations[4].id, activity_id=trucks.id),
        OrganizationActivity(organization_id=organizations[5].id, activity_id=food.id),
    ]
    db.add_all(org_activities)
    db.commit()
    
    print("✓ База данных успешно заполнена тестовыми данными!")
    print(f"  - Зданий: {len(buildings)}")
    print(f"  - Деятельностей: {len([food, auto, meat, dairy, trucks, cars, parts, accessories])}")
    print(f"  - Организаций: {len(organizations)}")
    print(f"  - Телефонов: {len(phones)}")

finally:
    db.close()
