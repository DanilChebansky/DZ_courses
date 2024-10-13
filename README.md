# DZ_courses
Инструкция:

Убедитесь, что Docker установлен на ваш компьютер, или установите из дистрибутива, полученного на сайте https://www.docker.com/.

Для запуска процесса создания контейнеров в терминале перейдите в корневую папку проекта и выполните команду: $ docker-compose up -d --build

После завершения процесса развертывания и запуска приложений в контейнерах docker в терминале появится сообщение:
[+] Running 6/6 ✔ Volume "pythonproject9_pg_data" Created 0.9s ✔ Container pythonproject9-db-1 Healthy 91.0s ✔ Container pythonproject9-redis-1 Running 0.0s ✔ Container pythonproject9-app-1 Started 83.1s ✔ Container pythonproject9-celery-beat-1 Started 79.0s ✔ Container pythonproject9-celery-1 Started Теперь к приложению можно обращаться через http://localhost:8000/

В браузере по адресу http://localhost:8000/swagger/ можно ознакомиться с описанием API.
