"""
Скрипт для заполнения БД тестовыми данными (1000 организаций)
Async версия
"""
import asyncio
import json
import random
from pathlib import Path
import sys

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select

sys.path.append(str(Path(__file__).parent.parent))
from src.infrastructure.models import Building, Activity, Organization, OrganizationPhone, OrganizationActivity

DATABASE_URL = "sqlite+aiosqlite:///./luna.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_activities_from_json():
    """Создает деятельности из JSON файла"""
    with open(Path(__file__).parent / 'activities.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    activities_tree = data['деятельности']
    activity_ids = {}
    
    async def create_activities_recursive(tree, parent_id=None, level=1):
        for name, children in tree.items():
            activity = Activity(name=name, level=level, parent_id=parent_id)
            async with AsyncSessionLocal() as session:
                session.add(activity)
                await session.commit()
                activity_ids[name] = activity.id
                
                if children:
                    await create_activities_recursive(children, parent_id=activity.id, level=level + 1)
    
    await create_activities_recursive(activities_tree)
    return activity_ids


def generate_phone():
    phone_codes = ["2", "3", "4", "5", "6", "7", "8-900", "8-901", "8-902", "8-903", "8-904", 
                   "8-905", "8-906", "8-907", "8-908", "8-909", "8-912", "8-913", "8-914", 
                   "8-915", "8-916", "8-917", "8-918", "8-919", "8-920", "8-921", "8-922", 
                   "8-923", "8-924", "8-925", "8-926", "8-927", "8-928", "8-929"]
    code = random.choice(phone_codes)
    return f"{code}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"


def generate_company_name():
    prefixes = ["ООО", "АО", "ИП", "ООО 'Торговый дом'", "ЗАО", "ПАО", "Группа компаний", "Холдинг"]
    roots = ["Вектор", "Прогресс", "Технологии", "Сервис", "Торг", "Снаб", "Строй", "Альфа", 
             "Бета", "Омега", "Лидер", "Профи", "Эксперт", "Гарант", "Урал", "Сибирь", 
             "Инвест", "Капитал", "Финанс", "Трейд", "Импэкс"]
    suffixes = ["", " Плюс", " Групп", " М", " Пром", " Агро", " Фарм", " Мед", " Строй"]
    
    return f"{random.choice(prefixes)} '{random.choice(roots)}{random.choice(suffixes)}'"


def generate_address():
    cities = ["г. Москва", "г. Санкт-Петербург", "г. Екатеринбург", "г. Казань", 
              "г. Новосибирск", "г. Нижний Новгород", "г. Челябинск", "г. Самара"]
    streets = ["ул. Ленина", "ул. Пушкина", "ул. Кирова", "ул. Гагарина", "ул. Мира",
               "пр. Ленина", "пр. Мира", "ул. Советская", "ул. Комсомольская"]
    
    city = random.choice(cities)
    street = random.choice(streets)
    building = random.randint(1, 200)
    office = f"офис {random.randint(1, 500)}"
    
    return f"{city}, {street} {building}, {office}"


def generate_coordinates(address):
    city_coords = {
        "г. Москва": (55.75, 37.61, 0.5),
        "г. Санкт-Петербург": (59.93, 30.33, 0.4),
        "г. Екатеринбург": (56.84, 60.61, 0.3),
        "г. Казань": (55.79, 49.12, 0.3),
        "г. Новосибирск": (55.01, 82.93, 0.3),
        "г. Нижний Новгород": (56.33, 44.00, 0.3),
        "г. Челябинск": (55.16, 61.43, 0.3),
        "г. Самара": (53.20, 50.15, 0.3),
    }
    
    city = address.split(",")[0]
    base_lat, base_lon, delta = city_coords.get(city, (55.75, 37.61, 0.5))
    
    lat = base_lat + random.uniform(-delta, delta)
    lon = base_lon + random.uniform(-delta, delta)
    
    return round(lat, 6), round(lon, 6)


async def seed_organizations(activity_ids):
    """Создает 1000 организаций"""
    all_activity_ids = list(activity_ids.values())
    level1_names = list(activity_ids.keys())[:20]  # Первые 20 - это в основном level 1
    level1_activity_ids = [activity_ids[name] for name in level1_names if name in activity_ids]
    
    async with AsyncSessionLocal() as session:
        for i in range(1000):
            address = generate_address()
            lat, lon = generate_coordinates(address)
            
            # Проверяем существование здания
            result = await session.execute(select(Building).where(Building.address == address))
            building = result.scalar_one_or_none()
            
            if not building:
                building = Building(address=address, latitude=lat, longitude=lon)
                session.add(building)
                await session.flush()
            
            organization = Organization(name=generate_company_name(), building_id=building.id)
            session.add(organization)
            await session.flush()
            
            # Телефоны
            for _ in range(random.randint(1, 3)):
                phone = OrganizationPhone(organization_id=organization.id, phone=generate_phone())
                session.add(phone)
            
            # Деятельности
            selected = set()
            for _ in range(random.randint(1, 4)):
                if random.random() < 0.3 and level1_activity_ids:
                    act_id = random.choice(level1_activity_ids)
                else:
                    act_id = random.choice(all_activity_ids)
                selected.add(act_id)
            
            for act_id in selected:
                link = OrganizationActivity(organization_id=organization.id, activity_id=act_id)
                session.add(link)
            
            if (i + 1) % 100 == 0:
                await session.commit()
                print(f"  Создано организаций: {i + 1}")
        
        await session.commit()


async def main():
    print("=== Инициализация БД ===")
    
    print("\nСоздание деятельностей...")
    activity_ids = await create_activities_from_json()
    print(f"✓ Создано деятельностей: {len(activity_ids)}")
    
    print("\nСоздание организаций (1000)...")
    await seed_organizations(activity_ids)
    
    print("\n✓ Готово!")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
