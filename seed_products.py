import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product
from django.core.files.base import ContentFile
import base64

# Simple 1x1 transparent pixel for placeholder
PIXEL = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI'
    b'7wAAAABJRU5ErkJggg=='
)
placeholder_image = ContentFile(base64.b64decode(PIXEL), name='placeholder.png')

def seed_data():
    data = [
        {
            "category": ("Erkaklar kiyimi", "Мужская одежда"),
            "products": [
                ("Klassik kostyum", "Классический костюм", 1200000),
                ("Paxtali futbolka", "Хлопковая футболка", 85000),
                ("Djinsi shim", "Джинсовые брюки", 250000),
                ("Klassik ko'ylak", "Классическая рубашка", 180000),
                ("Junli sviter", "Шерстяной свитер", 320000),
            ]
        },
        {
            "category": ("Ayollar kiyimi", "Женская одежда"),
            "products": [
                ("Kechki ko'ylak", "Вечернее платье", 950000),
                ("Ipak bluzka", "Шелковая блузка", 220000),
                ("Klassik yubka", "Классическая юбка", 190000),
                ("Ayollar djinsisi", "Женские джинсы", 280000),
                ("Trikotaj kardiagan", "Трикотажный кардиган", 350000),
            ]
        },
        {
            "category": ("Bolalar kiyimi", "Детская одежда"),
            "products": [
                ("Bolalar kombinezoni", "Детский комбинезон", 150000),
                ("Maktab formasi", "Школьная форма", 450000),
                ("Rangli mayka", "Цветная майка", 45000),
                ("Sport kostyumi", "Спортивный костюм", 210000),
                ("Bolalar kurtkasi", "Детская куртка", 380000),
            ]
        },
        {
            "category": ("Oyoq kiyimlar", "Обувь"),
            "products": [
                ("Charm tufli", "Кожаные туфли", 550000),
                ("Sport krossovka", "Спортивные кроссовки", 420000),
                ("Qishki botinka", "Зимние ботинки", 680000),
                ("Ayollar shippagi", "Женские тапочки", 95000),
                ("Mokasinalar", "Мокасины", 310000),
            ]
        },
        {
            "category": ("Ustki kiyimlar", "Верхняя одежда"),
            "products": [
                ("Qishki kurtka", "Зимняя куртка", 850000),
                ("Kuzgi palto", "Осеннее пальто", 1100000),
                ("Yengil plash", "Легкий плащ", 520000),
                ("Kojux (Teri kurtka)", "Кожаная куртка", 1500000),
                ("Bomba kurtka", "Куртка-бомбер", 440000),
            ]
        },
        {
            "category": ("Sport kiyimlari", "Спортивная одежда"),
            "products": [
                ("Futbol formasi", "Футбольная форма", 180000),
                ("Sport shortilari", "Спортивные шорты", 95000),
                ("Termo-kiyim", "Термобелье", 240000),
                ("Fitnes leginslari", "Легинсы для фитнеса", 160000),
                ("Kapyushonli xudi", "Худи с капюшоном", 290000),
            ]
        },
        {
            "category": ("Bosh kiyimlar", "Головные уборы"),
            "products": [
                ("Sport kepkasi", "Спортивная кепка", 65000),
                ("Junli shapka", "Шерстяная шапка", 55000),
                ("Klassik shlyapa", "Классическая шляпа", 120000),
                ("Berep (Fransuzcha)", "Берет", 85000),
                ("Panama (Yozgi)", "Панама", 45000),
            ]
        },
        {
            "category": ("Sumkalar va aksessuarlar", "Сумки и аксессуары"),
            "products": [
                ("Charm hamyon", "Кожаный кошелек", 145000),
                ("Maktab ryukzaki", "Школьный рюкзак", 220000),
                ("Ayollar sumkachasi", "Женская сумочка", 380000),
                ("Safar chamodani", "Дорожный чемодан", 750000),
                ("Sport sumkasi", "Спортивная сумка", 165000),
            ]
        },
        {
            "category": ("Soatlar", "Часы"),
            "products": [
                ("Klassik qo'l soati", "Классические часы", 450000),
                ("Smart soat (Aqlli)", "Смарт-часы", 890000),
                ("Sport taymeri", "Спортивный таймер", 120000),
                ("Mexanik soat", "Механические часы", 2500000),
                ("Ayollar bilaguzuk-soati", "Часы-браслет", 340000),
            ]
        },
        {
            "category": ("Kamar va bog'ichlar", "Ремни и аксессуары"),
            "products": [
                ("Charm kamar", "Кожаный ремень", 110000),
                ("Mato kamar", "Тканевый ремень", 45000),
                ("Klassik galstuk", "Классический галстук", 75000),
                ("Kapalak galstuk", "Галстук-бабочка", 35000),
                ("Shim ushlagich", "Подтяжки", 60000),
            ]
        },
        {
            "category": ("Zargarlik buyumlari", "Ювелирные изделия"),
            "products": [
                ("Kumush uzuk", "Серебряное кольцо", 250000),
                ("Tilla zanjir", "Золотая цепочка", 4500000),
                ("Marvarid sirg'a", "Жемчужные серьги", 600000),
                ("Bilaguzuk", "Браслет", 180000),
                ("Kulon (Taqinchoq)", "Кулон", 120000),
            ]
        },
        {
            "category": ("Ko'zoynaklar", "Очки"),
            "products": [
                ("Quyoshdan saqlovchi", "Солнцезащитные очки", 135000),
                ("Kompyuter ko'zoynagi", "Очки для компьютера", 180000),
                ("Klassik ramka", "Классическая оправа", 210000),
                ("Sport ko'zoynagi", "Спортивные очки", 250000),
                ("G'ilof (Ko'zoynak uchun)", "Футляр для очков", 45000),
            ]
        },
        {
            "category": ("Sharflar va qo'lqoplar", "Шарфы и перчатки"),
            "products": [
                ("Kashmir sharf", "Кашемировый шарф", 165000),
                ("Charm qo'lqoplar", "Кожаные перчатки", 140000),
                ("Ipak ro'mol", "Шелковый платок", 95000),
                ("Sport qo'lqopi", "Спортивные перчатки", 110000),
                ("Qishki bo'yinbog'", "Зимний снуд", 75000),
            ]
        },
        {
            "category": ("Ichki kiyimlar", "Нижнее белье"),
            "products": [
                ("Paxtali mayka", "Хлопковая майка", 35000),
                ("Paypoqlar (10 juft)", "Носки (10 пар)", 65000),
                ("Tungi kiyim (Pijama)", "Пижама", 195000),
                ("Hammom xalati", "Банный халат", 320000),
                ("Sport toplari", "Спортивный топ", 85000),
            ]
        },
        {
            "category": ("Parfumeriya", "Парфюмерия"),
            "products": [
                ("Atir (Erkaklar uchun)", "Мужской парфюм", 550000),
                ("Atir (Ayollar uchun)", "Женский парфюм", 620000),
                ("Tana spreyi", "Спрей для тела", 85000),
                ("Sovg'alar to'plami", "Подарочный набор", 450000),
                ("Avtomobil atiri", "Автомобильный парфюм", 40000),
            ]
        },
    ]

    print("Seeding demo products...")
    
    for idx, cat_data in enumerate(data):
        cat_name, cat_name_ru = cat_data["category"]
        category, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={
                "name_ru": cat_name_ru,
                "order": idx,
                "is_active": True
            }
        )
        if created:
            category.image.save('cat_placeholder.png', placeholder_image, save=True)
            print(f"Created category: {cat_name}")
        
        for p_idx, (p_name, p_name_ru, p_price) in enumerate(cat_data["products"]):
            product, p_created = Product.objects.get_or_create(
                category=category,
                name=p_name,
                defaults={
                    "name_ru": p_name_ru,
                    "price": p_price,
                    "order": p_idx,
                    "is_active": True,
                    "description": f"{p_name} haqida batafsil ma'lumot.",
                    "description_ru": f"Подробная информация о {p_name_ru}."
                }
            )
            if p_created:
                product.image.save('prod_placeholder.png', placeholder_image, save=True)
                print(f"  Added product: {p_name}")

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
