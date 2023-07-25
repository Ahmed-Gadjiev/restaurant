1. Создайте виртуальное окружение с помощью команды:
   ```
   python -m venv venv 
   ```
2. Активируйте виртуально окружение: 
   ```
   .\venv\Scripts\activate
   ```
2. Установите зависимости из файла requirements.txt:
    ```
   pip install -r requirements.txt
   ```
2. Создайте файл .env по шаблону .env.example
3. Запустите сервер разработки:
    ```
   py -m uvicorn main:app --reload
   ```