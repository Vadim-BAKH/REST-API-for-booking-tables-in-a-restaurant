# REST-API-for-booking-tables-in-a-restaurant

Задание приложения в файле TASK.md

Для запуска приложения необходимо создать файл **.env**.

Шаблон для создания в файле **.env.template**:

        POSTGRES_USER=
        POSTGRES_PASSWORD=
        DB_PORT=
        POSTGRES_DB=
        DB_HOST=
        LOGLEVEL=

Приложение можно запустить командой bash:

        docker compose up --build -d


Документация для фронтенда открывается по адресу:

        http://localhost:8000/docs

![image](https://github.com/user-attachments/assets/e618e1c5-c539-495e-a650-5409f69627d1)


Тесты можно запустить командой bash:

       pytest -v

![image](https://github.com/user-attachments/assets/4646f670-9943-48b5-a19f-197ab2d5e81c)

Есть возможность запускать отдельно по категориям, например:

       pytest -m dish 
       pytest -m order
       
![image](https://github.com/user-attachments/assets/b66e0554-57c7-434a-b14e-6f91cfba5871)

![image](https://github.com/user-attachments/assets/b753eff1-4c29-4ad7-8811-d1bd89bd3903)

       

        

        
        



