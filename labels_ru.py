"""Русские названия всех классов моделей Open Images V7 (600) и COCO (80)."""

RU = {
    # ---- люди и части тела ----
    "Person": "человек", "Man": "мужчина", "Woman": "женщина", "Boy": "мальчик", "Girl": "девочка",
    "Human face": "лицо", "Human hand": "рука", "Human arm": "рука", "Human beard": "борода",
    "Human body": "тело", "Human ear": "ухо", "Human eye": "глаз", "Human foot": "ступня",
    "Human hair": "волосы", "Human head": "голова", "Human leg": "нога", "Human mouth": "рот",
    "Human nose": "нос", "Skull": "череп",

    # ---- транспорт ----
    "Car": "автомобиль", "Bus": "автобус", "Truck": "грузовик", "Bicycle": "велосипед",
    "Motorcycle": "мотоцикл", "Train": "поезд", "Airplane": "самолёт", "Aircraft": "летательный аппарат",
    "Boat": "лодка", "Van": "фургон", "Taxi": "такси", "Ambulance": "скорая помощь", "Limousine": "лимузин",
    "Helicopter": "вертолёт", "Rocket": "ракета", "Missile": "ракета (оружие)", "Submarine": "подводная лодка",
    "Barge": "баржа", "Canoe": "каноэ", "Gondola": "гондола", "Jet ski": "гидроцикл",
    "Watercraft": "плавсредство", "Land vehicle": "наземный транспорт", "Vehicle": "транспортное средство",
    "Golf cart": "гольф-кар", "Cart": "тележка", "Segway": "сигвей", "Unicycle": "моноцикл",
    "Snowmobile": "снегоход", "Snowplow": "снегоочиститель", "Tank": "танк", "Parachute": "парашют",
    "Wheel": "колесо", "Tire": "шина", "Bicycle wheel": "велосипедное колесо", "Auto part": "автозапчасть",
    "Vehicle registration plate": "номерной знак", "Seat belt": "ремень безопасности",
    "Traffic light": "светофор", "Traffic sign": "дорожный знак", "Stop sign": "знак «Стоп»",
    "Parking meter": "паркомат", "Street light": "фонарь", "Fire hydrant": "пожарный гидрант",

    # ---- канцелярия и офис ----
    "Pen": "ручка", "Ruler": "линейка", "Book": "книга/тетрадь", "Eraser": "ластик",
    "Pencil case": "пенал", "Pencil sharpener": "точилка", "Scissors": "ножницы", "Stapler": "степлер",
    "Calculator": "калькулятор", "Envelope": "конверт", "Paper cutter": "резак для бумаги",
    "Whiteboard": "доска", "Poster": "плакат", "Adhesive tape": "скотч", "Ring binder": "папка-регистратор",
    "Office supplies": "канцтовары", "Filing cabinet": "картотечный шкаф", "Printer": "принтер",
    "Fax": "факс", "Office building": "офисное здание", "Briefcase": "портфель",

    # ---- техника и электроника ----
    "Laptop": "ноутбук", "Computer monitor": "монитор", "Computer keyboard": "клавиатура",
    "Computer mouse": "компьютерная мышь", "Mobile phone": "телефон", "Tablet computer": "планшет",
    "Television": "телевизор", "Headphones": "наушники", "Camera": "фотоаппарат", "Remote control": "пульт",
    "Corded phone": "стационарный телефон", "Telephone": "телефон", "Ipod": "плеер iPod",
    "Cassette deck": "кассетная дека", "Microphone": "микрофон", "Light bulb": "лампочка",
    "Light switch": "выключатель", "Power plugs and sockets": "розетка/вилка", "Flashlight": "фонарик",
    "Digital clock": "электронные часы", "Watch": "наручные часы", "Binoculars": "бинокль",
    "Tripod": "штатив", "Scoreboard": "табло", "Billboard": "рекламный щит",

    # ---- бытовая техника ----
    "Home appliance": "бытовая техника", "Kitchen appliance": "кухонная техника",
    "Refrigerator": "холодильник", "Microwave oven": "микроволновка", "Oven": "духовка",
    "Gas stove": "газовая плита", "Toaster": "тостер", "Kettle": "чайник", "Coffeemaker": "кофеварка",
    "Blender": "блендер", "Mixer": "миксер", "Food processor": "кухонный комбайн",
    "Slow cooker": "мультиварка", "Pressure cooker": "скороварка", "Waffle iron": "вафельница",
    "Dishwasher": "посудомойка", "Washing machine": "стиральная машина", "Sewing machine": "швейная машина",
    "Hair dryer": "фен", "Hand dryer": "сушилка для рук", "Humidifier": "увлажнитель",
    "Heater": "обогреватель", "Mechanical fan": "вентилятор", "Ceiling fan": "потолочный вентилятор",
    "Wood-burning stove": "печь", "Fireplace": "камин",

    # ---- мебель и интерьер ----
    "Furniture": "мебель", "Chair": "стул", "Table": "стол", "Desk": "письменный стол",
    "Coffee table": "журнальный столик", "Kitchen & dining room table": "обеденный стол",
    "Couch": "диван", "Sofa bed": "диван-кровать", "Studio couch": "раскладной диван",
    "Loveseat": "двухместный диван", "Bed": "кровать", "Infant bed": "детская кроватка",
    "Bookcase": "книжный шкаф", "Shelf": "полка", "Cabinetry": "шкафы", "Cupboard": "буфет",
    "Closet": "гардеробная", "Wardrobe": "платяной шкаф", "Chest of drawers": "комод",
    "Drawer": "ящик", "Nightstand": "тумбочка", "Stool": "табурет", "Bench": "скамейка",
    "Countertop": "столешница", "Lamp": "лампа", "Curtain": "штора", "Window blind": "жалюзи",
    "Mirror": "зеркало", "Picture frame": "рамка для фото", "Pillow": "подушка", "Vase": "ваза",
    "Flowerpot": "цветочный горшок", "Candle": "свеча", "Clock": "часы", "Wall clock": "настенные часы",
    "Alarm clock": "будильник", "Door": "дверь", "Door handle": "дверная ручка", "Window": "окно",
    "Stairs": "лестница", "Porch": "крыльцо", "Spice rack": "полка для специй", "Wine rack": "винная полка",
    "Cat furniture": "домик для кошки", "Dog bed": "лежанка для собаки",

    # ---- ванная и сантехника ----
    "Bathroom accessory": "аксессуар для ванной", "Bathroom cabinet": "шкафчик для ванной",
    "Bathtub": "ванна", "Shower": "душ", "Sink": "раковина", "Tap": "кран", "Toilet": "унитаз",
    "Bidet": "биде", "Jacuzzi": "джакузи", "Plumbing fixture": "сантехника", "Towel": "полотенце",
    "Toilet paper": "туалетная бумага", "Paper towel": "бумажное полотенце",
    "Facial tissue holder": "салфетница", "Soap dispenser": "дозатор мыла", "Toothbrush": "зубная щётка",

    # ---- кухня и посуда ----
    "Kitchenware": "кухонная утварь", "Kitchen utensil": "кухонный инвентарь", "Tableware": "посуда",
    "Bottle": "бутылка", "Coffee cup": "кружка", "Mug": "кружка", "Cup": "чашка", "Wine glass": "бокал",
    "Plate": "тарелка", "Bowl": "миска", "Mixing bowl": "миска для смешивания", "Saucer": "блюдце",
    "Platter": "блюдо", "Serving tray": "поднос", "Teapot": "заварочный чайник", "Jug": "кувшин",
    "Pitcher (Container)": "кувшин", "Knife": "нож", "Kitchen knife": "кухонный нож", "Spoon": "ложка",
    "Fork": "вилка", "Chopsticks": "палочки для еды", "Ladle": "половник", "Spatula": "лопатка",
    "Whisk": "венчик", "Frying pan": "сковорода", "Wok": "вок", "Cutting board": "разделочная доска",
    "Measuring cup": "мерный стакан", "Cake stand": "подставка для торта", "Drinking straw": "трубочка",
    "Bottle opener": "открывалка", "Can opener": "консервный нож", "Pizza cutter": "нож для пиццы",
    "Salt and pepper shakers": "солонка и перечница", "Cocktail shaker": "шейкер", "Tin can": "жестяная банка",
    "Container": "контейнер", "Box": "коробка", "Barrel": "бочка", "Picnic basket": "корзина для пикника",
    "Beaker": "мензурка", "Grinder": "мельница", "Cooking spray": "кулинарный спрей",
    "Waste container": "мусорный бак", "Plastic bag": "пакет",

    # ---- еда и напитки ----
    "Food": "еда", "Fast food": "фастфуд", "Snack": "закуска", "Dessert": "десерт",
    "Baked goods": "выпечка", "Bread": "хлеб", "Bagel": "бублик", "Croissant": "круассан",
    "Muffin": "маффин", "Doughnut": "пончик", "Pastry": "пирожное", "Cake": "торт", "Cookie": "печенье",
    "Tart": "тарт", "Pancake": "блин", "Waffle": "вафля", "Pretzel": "крендель", "Candy": "конфета",
    "Ice cream": "мороженое", "Popcorn": "попкорн", "Hamburger": "гамбургер", "Hot dog": "хот-дог",
    "Sandwich": "сэндвич", "Submarine sandwich": "сабвей-сэндвич", "Pizza": "пицца", "Pasta": "паста",
    "Burrito": "буррито", "Taco": "тако", "Sushi": "суши", "Salad": "салат", "French fries": "картофель фри",
    "Guacamole": "гуакамоле", "Cheese": "сыр", "Cream": "сливки", "Milk": "молоко",
    "Dairy Product": "молочный продукт", "Egg (Food)": "яйцо", "Seafood": "морепродукты",
    "Drink": "напиток", "Coffee": "кофе", "Tea": "чай", "Juice": "сок", "Beer": "пиво", "Wine": "вино",
    "Cocktail": "коктейль",
    "Fruit": "фрукт", "Apple": "яблоко", "Banana": "банан", "Orange": "апельсин", "Lemon": "лимон",
    "Grapefruit": "грейпфрут", "Grape": "виноград", "Peach": "персик", "Pear": "груша", "Mango": "манго",
    "Pineapple": "ананас", "Strawberry": "клубника", "Watermelon": "арбуз", "Cantaloupe": "дыня",
    "Winter melon": "восковая тыква", "Pomegranate": "гранат", "Coconut": "кокос", "Common fig": "инжир",
    "Vegetable": "овощ", "Tomato": "помидор", "Cucumber": "огурец", "Potato": "картофель",
    "Carrot": "морковь", "Cabbage": "капуста", "Broccoli": "брокколи", "Bell pepper": "болгарский перец",
    "Radish": "редис", "Pumpkin": "тыква", "Zucchini": "кабачок", "Squash (Plant)": "тыква (кабачок)",
    "Artichoke": "артишок", "Garden Asparagus": "спаржа", "Mushroom": "гриб",

    # ---- одежда и аксессуары ----
    "Clothing": "одежда", "Footwear": "обувь", "Boot": "ботинок", "Sandal": "сандалия",
    "High heels": "туфли на каблуке", "Sock": "носок", "Hat": "шапка", "Cowboy hat": "ковбойская шляпа",
    "Fedora": "фетровая шляпа", "Sombrero": "сомбреро", "Sun hat": "панама", "Helmet": "шлем",
    "Bicycle helmet": "велошлем", "Football helmet": "футбольный шлем", "Swim cap": "шапочка для плавания",
    "Jeans": "джинсы", "Trousers": "брюки", "Shorts": "шорты", "Skirt": "юбка", "Miniskirt": "мини-юбка",
    "Dress": "платье", "Shirt": "рубашка", "Jacket": "куртка", "Coat": "пальто", "Suit": "костюм",
    "Tie": "галстук", "Scarf": "шарф", "Glove": "перчатка", "Belt": "ремень", "Brassiere": "бюстгальтер",
    "Swimwear": "купальник", "Sports uniform": "спортивная форма", "Diaper": "подгузник",
    "Glasses": "очки", "Sunglasses": "солнцезащитные очки", "Goggles": "защитные очки",
    "Earrings": "серьги", "Necklace": "ожерелье", "Crown": "корона", "Tiara": "тиара",
    "Fashion accessory": "аксессуар", "Backpack": "рюкзак", "Handbag": "сумка", "Suitcase": "чемодан",
    "Luggage and bags": "багаж и сумки", "Umbrella": "зонт",

    # ---- косметика и уход ----
    "Personal care": "средство ухода", "Cosmetics": "косметика", "Lipstick": "помада",
    "Face powder": "пудра", "Perfume": "духи", "Hair spray": "лак для волос",

    # ---- инструменты ----
    "Tool": "инструмент", "Hammer": "молоток", "Screwdriver": "отвёртка", "Wrench": "гаечный ключ",
    "Ratchet (Device)": "трещотка", "Drill (Tool)": "дрель", "Chainsaw": "бензопила", "Axe": "топор",
    "Chisel": "стамеска", "Nail (Construction)": "гвоздь", "Ladder": "стремянка", "Scale": "весы",
    "Torch": "факел", "Lantern": "фонарь-лампа",

    # ---- музыка ----
    "Musical instrument": "музыкальный инструмент", "Guitar": "гитара", "Piano": "пианино",
    "Musical keyboard": "синтезатор", "Violin": "скрипка", "Cello": "виолончель", "Harp": "арфа",
    "Harpsichord": "клавесин", "Organ (Musical Instrument)": "орган", "Accordion": "аккордеон",
    "Banjo": "банджо", "Drum": "барабан", "Flute": "флейта", "Oboe": "гобой", "Saxophone": "саксофон",
    "Trumpet": "труба", "Trombone": "тромбон", "French horn": "валторна", "Harmonica": "губная гармошка",
    "Maracas": "маракасы", "Chime": "колокольчики",

    # ---- спорт и отдых ----
    "Sports equipment": "спортинвентарь", "Ball": "мяч", "Football": "футбольный мяч",
    "Rugby ball": "мяч для регби", "Volleyball (Ball)": "волейбольный мяч", "Tennis ball": "теннисный мяч",
    "Golf ball": "мяч для гольфа", "Cricket ball": "мяч для крикета", "Racket": "ракетка",
    "Tennis racket": "теннисная ракетка", "Table tennis racket": "ракетка для настольного тенниса",
    "Baseball bat": "бейсбольная бита", "Baseball glove": "бейсбольная перчатка",
    "Bowling equipment": "инвентарь для боулинга", "Billiard table": "бильярдный стол",
    "Skateboard": "скейтборд", "Surfboard": "доска для серфинга", "Snowboard": "сноуборд", "Ski": "лыжи",
    "Roller skates": "ролики", "Flying disc": "фрисби", "Kite": "воздушный змей", "Paddle": "весло",
    "Dumbbell": "гантель", "Punching bag": "боксёрская груша", "Treadmill": "беговая дорожка",
    "Stationary bicycle": "велотренажёр", "Indoor rower": "гребной тренажёр",
    "Training bench": "тренировочная скамья", "Balance beam": "бревно (гимнастика)",
    "Horizontal bar": "турник", "Hiking equipment": "туристическое снаряжение", "Tent": "палатка",
    "Personal flotation device": "спасательный жилет", "Swimming pool": "бассейн",
    "Toy": "игрушка", "Doll": "кукла", "Teddy bear": "плюшевый мишка", "Balloon": "воздушный шар",
    "Dice": "игральные кости",

    # ---- оружие ----
    "Weapon": "оружие", "Handgun": "пистолет", "Rifle": "винтовка", "Shotgun": "дробовик",
    "Sword": "меч", "Dagger": "кинжал", "Bow and arrow": "лук и стрелы", "Cannon": "пушка", "Bomb": "бомба",

    # ---- медицина ----
    "Medical equipment": "медицинское оборудование", "Stethoscope": "стетоскоп", "Syringe": "шприц",
    "Stretcher": "носилки", "Wheelchair": "инвалидная коляска", "Crutch": "костыль",
    "Band-aid": "пластырь",

    # ---- здания и места ----
    "Building": "здание", "House": "дом", "Skyscraper": "небоскрёб", "Tower": "башня",
    "Castle": "замок", "Lighthouse": "маяк", "Tree house": "домик на дереве", "Fountain": "фонтан",
    "Convenience store": "магазин", "Sculpture": "скульптура", "Bronze sculpture": "бронзовая скульптура",
    "Bust": "бюст", "Flag": "флаг", "Christmas tree": "новогодняя ёлка", "Snowman": "снеговик",
    "Coin": "монета",

    # ---- растения ----
    "Plant": "растение", "Houseplant": "комнатное растение", "Tree": "дерево", "Palm tree": "пальма",
    "Maple": "клён", "Willow": "ива", "Flower": "цветок", "Rose": "роза", "Lily": "лилия",
    "Common sunflower": "подсолнух", "Lavender (Plant)": "лаванда",

    # ---- животные ----
    "Animal": "животное", "Mammal": "млекопитающее", "Carnivore": "хищник", "Reptile": "рептилия",
    "Insect": "насекомое", "Invertebrate": "беспозвоночное", "Marine invertebrates": "морские беспозвоночные",
    "Marine mammal": "морское млекопитающее",
    "Dog": "собака", "Cat": "кошка", "Bird": "птица", "Horse": "лошадь", "Mule": "мул", "Cattle": "корова",
    "Bull": "бык", "Sheep": "овца", "Goat": "коза", "Pig": "свинья", "Rabbit": "кролик", "Hamster": "хомяк",
    "Mouse": "мышь", "Squirrel": "белка", "Hedgehog": "ёж", "Porcupine": "дикобраз", "Raccoon": "енот",
    "Skunk": "скунс", "Fox": "лиса", "Otter": "выдра", "Armadillo": "броненосец", "Monkey": "обезьяна",
    "Bear": "медведь", "Brown bear": "бурый медведь", "Polar bear": "белый медведь", "Panda": "панда",
    "Red panda": "малая панда", "Koala": "коала", "Kangaroo": "кенгуру", "Lion": "лев", "Tiger": "тигр",
    "Leopard": "леопард", "Cheetah": "гепард", "Jaguar (Animal)": "ягуар", "Lynx": "рысь",
    "Elephant": "слон", "Giraffe": "жираф", "Zebra": "зебра", "Rhinoceros": "носорог",
    "Hippopotamus": "бегемот", "Camel": "верблюд", "Alpaca": "альпака", "Deer": "олень",
    "Antelope": "антилопа", "Bat (Animal)": "летучая мышь",
    "Chicken": "курица", "Duck": "утка", "Goose": "гусь", "Swan": "лебедь", "Turkey": "индейка",
    "Eagle": "орёл", "Falcon": "сокол", "Owl": "сова", "Parrot": "попугай", "Canary": "канарейка",
    "Sparrow": "воробей", "Raven": "ворон", "Magpie": "сорока", "Blue jay": "голубая сойка",
    "Woodpecker": "дятел", "Ostrich": "страус", "Penguin": "пингвин",
    "Fish": "рыба", "Goldfish": "золотая рыбка", "Shark": "акула", "Whale": "кит", "Dolphin": "дельфин",
    "Sea lion": "морской лев", "Harbor seal": "тюлень", "Rays and skates": "скат", "Jellyfish": "медуза",
    "Starfish": "морская звезда", "Seahorse": "морской конёк", "Squid": "кальмар", "Crab": "краб",
    "Lobster": "омар", "Shrimp": "креветка", "Oyster": "устрица", "Shellfish": "моллюск",
    "Sea turtle": "морская черепаха", "Turtle": "черепаха", "Tortoise": "сухопутная черепаха",
    "Crocodile": "крокодил", "Lizard": "ящерица", "Snake": "змея", "Frog": "лягушка", "Dinosaur": "динозавр",
    "Butterfly": "бабочка", "Moths and butterflies": "бабочка/мотылёк", "Caterpillar": "гусеница",
    "Bee": "пчела", "Beehive": "улей", "Honeycomb": "соты", "Ant": "муравей", "Beetle": "жук",
    "Ladybug": "божья коровка", "Dragonfly": "стрекоза", "Spider": "паук", "Scorpion": "скорпион",
    "Centipede": "многоножка", "Tick": "клещ", "Snail": "улитка", "Worm": "червь", "Isopod": "мокрица",

    # ---- COCO (названия в нижнем регистре, которых нет выше) ----
    "person": "человек", "cell phone": "телефон", "keyboard": "клавиатура", "mouse": "компьютерная мышь",
    "dining table": "стол", "tv": "телевизор", "remote": "пульт", "potted plant": "комнатное растение",
    "cow": "корова", "frisbee": "фрисби", "skis": "лыжи", "sports ball": "мяч", "donut": "пончик",
    "microwave": "микроволновка", "hair drier": "фен", "book": "книга/тетрадь", "laptop": "ноутбук",
    "cup": "чашка", "clock": "часы", "bird": "птица",
}

_LOWER = {k.lower(): v for k, v in RU.items()}


def ru(name: str) -> str:
    """Русское название класса; ищет без учёта регистра (COCO пишет классы строчными)."""
    return RU.get(name) or _LOWER.get(name.lower(), name)
