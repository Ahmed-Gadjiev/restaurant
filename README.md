1. Для запуска приложения последовательно выполните команды: 
   ```
   docker-compose build
   docker-compose up -d
   ```
   
2. Для запуска тестов последовательно выполните команды:
   ```
   docker build -t tests_image -f .\Dockerfile-tests .
   docker run --network restaurant_network -d tests_image
   ```
   

   