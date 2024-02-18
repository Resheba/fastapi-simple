Structure
```
Структура папок
C:.
│   .dockerignore
│   .gitignore
│   alembic.ini
│   base.db
│   docker-compose.yml
│   Dockerfile
│   main.py
│   README.md
│   requirements.txt
│       
├───auth
│       schemas.py
│       security.py
│       __init__.py
│       
├───config
│       env.py
│       __init__.py
│       
├───core
│       exception.py
│       response.py
│       __init__.py
│       
├───database
│       manager.py
│       model.py
│       _abcrepos.py
│       __init__.py
│       
├───docker
│       app.sh
│       celery.sh
│       flower.sh
│       
├───migrations
│   │   env.py
│   │   README
│   │   script.py.mako
│   │   
│   └───versions
│           e940e33c9a4c_added_user_table.py
│           ea51b536de48_init_revision.py
│           
├───routers
│   │   __init__.py
│   │   
│   ├───arithmetic
│   │       router.py
│   │       schemas.py
│   │       tasks.py
│   │       __init__.py
│   │       
│   ├───auth
│   │       router.py
│   │       __init__.py
│   │       
│   ├───author
│   │       depends.py
│   │       repos.py
│   │       router.py
│   │       schemas.py
│   │       __init__.py
│   │       
│   └───user
│           repos.py
│           router.py
│           schemas.py
│           __init__.py
│           
└───tasks
        celery.py
        __init__.py
        
```
