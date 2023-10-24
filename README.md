Запуск
1.git clone https://github.com/yariksbachok/everest.git

2.docker-compose up


Адмін панель
email: admin@admin.com
password: adminadmin

Також можна зарейструвати нового якщо в config.py/SECURITY_REGISTERABLE поставити значення True


Дамп БД

everest.sql


Ендпойнт для отримання інформації по статусу замовлення

statis/js/track.js - js файл для взаємодій із сервером та обробкою данних 

на сервер відправдяємо id замовлення post запитом на лінк track_order, сервер обробляє запит та повертає дані, дані ми обробляєм в формат json та виводим їх


для запуска celery використовуються дві команди вони прописанні в docker-composer

для запуска celery

1.celery -A app.celery worker --pool=solo -l info


для beat_schedule

2.celery -A app.celery beat -l info

