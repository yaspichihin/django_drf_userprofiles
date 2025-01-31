# Система управления пользователями

## Задача

Переопределить модель `User` собственной моделью `UserProfile`, чтобы:  
- Использовать **адрес электронной почты** вместо стандартного имени пользователя (`username`).  
- Расширить модель для дополнительных требований(Гибкое управление статусами пользователей).

> **Примечание:**  
> Альтернативный вариант — расширение модели `User` за счет создания модели 
> `Profile` (связь `OneToOne`) и использования сигналов **не рассматривается**.



# Требования

```txt
Python 3.12
```



# Установка
Создать виртуальное окружение.
```shell
pip -m venv .venv
```

Задать виртуальное окружение
```shell
source .venv/bin/activate
```

Установить зависимость
```shell
pip install -r requirements.txt
```



# Настройка
Создать файл `.env` и установить значения для:
* SECRET_KEY

Выполнить миграции
```shell
./manage.py migrate
```

Создать супер пользователя
```shell
./manage.py createsuperuser
```



# Запуск сервера
```shell
./manage.py runserver
```

Перейдите в браузере на страницу api.
```shell
http://127.0.0.1:8000/api/
```

Ссылка на админ панель
```shell
http://127.0.0.1:8000/admin/
```


