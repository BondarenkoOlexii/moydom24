<div align="center">

# 🏢 MoyDom24 — CRM & Billing System for Residential Complexes (ОСББ / ЖК)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django Ninja](https://img.shields.io/badge/Django%20Ninja-Fast%20API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://django-ninja.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Broker%20%26%20Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-Async%20Tasks-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

<p align="center">
  <b>Комплексна веб-платформа для автоматизації управління багатоквартирними будинками, білінгу комунальних послуг, обліку показників лічильників та взаємодії з мешканцями.</b>
</p>

</div>

---

## 📌 Про проєкт

**MoyDom24** — це спеціалізована CRM/ERP-система для керівних компаній, ОСББ та житлових комплексів. Платформа об'єднує повноцінний бекофіс для адміністрації (бухгалтерія, менеджери, технічні спеціалісти) та зручний особистий кабінет для власників квартир.

Система автоматизує облік житлового фонду, нарахування за комунальні послуги, збір показників лічильників, обробку заявок на виклик майстрів та касові операції.

---

## ✨ Ключові можливості

### ⚙️ Панель адміністратора та управління ЖК
* **Житловий фонд:** Ієрархічна структура об'єктів (Будинки → Секції → Поверхи → Квартири → Особові рахунки).
* **Білінг та тарифи:** Гнучка тарифна сітка за послугами (водопостачання, електроенергія, опалення, квартплата, вивіз сміття).
* **Квитанції та нарахування:** Автоматичне формування рахунків на основі тарифів і спожитих ресурсів, масовий друк та вивантаження у формати **Excel** та **PDF**.
* **Каса та фінансовий облік:** Облік надходжень і витрат коштів (прибуткові та видаткові касові ордери, статистика заборгованостей).
* **Показники лічильників:** Централізований журнал обліку споживання з прив'язкою до квартир та особових рахунків.
* **Диспетчерська (Заявки майстрам):** Облік і контроль виконання звернень мешканців (сантехнік, електрик, аварійні роботи) зі зміною статусів та призначеними виконавцями.
* **Гнучка система ролей (RBAC):** Розмежування прав доступу до розділів системи для різних категорій персоналу.

### 👤 Особистий кабінет мешканця (`/cabinet/`)
* **Огляд квартири та балансу:** Перегляд поточної інформації про власність, особовий рахунок і баланс.
* **Внесення показників лічильників:** Зручна передача актуальних даних приладів обліку онлайн.
* **Квитанції та оплата:** Перегляд історії нарахувань, завантаження розгорнутих квитанцій та онлайн-оплата.
* **Виклик майстра:** Створення онлайн-заявок на обслуговування з вибором зручного часу та описом проблеми.
* **Профіль користувача:** Керування персональними контактними даними та зміна пароля.

---

## 🛠 Технологічний стек

| Сфера | Стек технологій |
| :--- | :--- |
| **Backend** | Python 3.11+, Django 5.x (MVT Architecture) |
| **API Endpoints** | Django Ninja (швидкі типізовані ендпоінти) |
| **База даних & Кеш** | PostgreSQL, Redis |
| **Фонові завдання** | Celery (розсилки сповіщень) |
| **Frontend & UI** | Bootstrap, HTML5/CSS3, JavaScript (ES6+), jQuery |
| **Таблиці та віджети** | AjaxDatatable (серверна пагінація та фільтрація), Select2 (динамічні випадаючі списки) |
| **Експорт даних** | Формування та експорт звітів і квитанцій у Excel / PDF |

---

## 👥 Ролі користувачів за замовчуванням

Система підтримує попередньо налаштовані рівні доступу для персоналу:
* **👑 Директор:** Повний доступ до всіх розділів, аналітики, фінансової статистики та налаштувань.
* **📊 Бухгалтер:** Керування тарифами, нарахуваннями, квитанціями, касою та особовими рахунками.
* **💼 Менеджер:** Робота з базою власників, квартирами, перевірка лічильників та організація процесів.
* **🔧 Сантехнік / ⚡ Електрик:** Доступ виключно до журналу призначених заявок на виклик майстра.
* **🏠 Мешканець (Власник квартири):** Доступ тільки до власного кабінету (`/cabinet/`).

---

## 🚀 Встановлення та запуск

### 1. Клонування репозиторію
```bash
git clone [https://github.com/BondarenkoOlexii/moydom24.git](https://github.com/BondarenkoOlexii/moydom24.git)
cd moydom24
```

### 2. Створення та активація віртуального середовища
**Windows (PowerShell / CMD):**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Встановлення залежностей
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Налаштування змінних середовища
Створіть файл `.env` у корені проєкту:

```env
DEBUG=True
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_NAME=moydom24_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Redis & Celery
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
CELERY_BROKER_URL=redis://127.0.0.1:6379/0

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
```

### 5. Застосування міграцій та генерація первинних даних
Виконайте міграції та запустіть команду `settups` для автоматичного створення тестових будинків, базових ролей та облікових записів співробітників (директора, бухгалтера, менеджера, сантехніка й електрика):

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py settups
```

### 6. Запуск черги завдань Celery
В окремому вікні термінала запустіть Celery worker:

**Linux / macOS:**
```bash
celery -A moydom24 worker -l info
```

**Windows (із прапорцем solo):**
```bash
celery -A moydom24 worker -l info -P solo
```

### 7. Запуск веб-сервера
```bash
python manage.py runserver
```

* **Панель управління (CRM / Адмінка):** [http://127.0.0.1:8000/adminpanel/](http://127.0.0.1:8000/adminpanel/)
* **Кабінет мешканця:** [http://127.0.0.1:8000/cabinet/](http://127.0.0.1:8000/cabinet/)
* **Документація API (Django Ninja):** [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

---

## 👨‍💻 Автор
**Bondarenko Olexii**

* GitHub: [@BondarenkoOlexii](https://github.com/BondarenkoOlexii)
