

1. Создайте виртуальное окружение с помощью команды:
   ```
   python -m venv venv 
   ```
   
2. Активируйте виртуально окружение: 
   ```
   .\venv\Scripts\activate
   ```

3. Для запуска приложения последовательно выполните команды: 
   ```
   docker-compose build
   docker-compose up -d
   ```
   
4. Для запуска тестов последовательно выполните команды:
   ```
   docker build -t tests_image -f .\Dockerfile-tests .
   docker run --network restaurant_network tests_image
   ```
   

   