1. Ссылка на проект https://fastapi-85rb.onrender.com/test/
2. Для локального запуска нужно будет сделать git clone https://github.com/dbisenev/fastapi
скачать все библиотеки pip install -r requirements.txt
В данной api реализована CRUD для локальной бд SQLite
В документации /docs можно увидеть все эндпоинты
где эндпоинт /test/ является простой проверкой отправления запроса на стороннюю api (fakestoreapi.com) - для заполнения Products
эндпоинт import кидает запрос на fakestoreapi далее парсит его под модель Products где сохраняет в бд, старался сделать этот запрос идемпотентным
