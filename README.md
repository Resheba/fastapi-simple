Structure
```
C:.
│   alembic.ini
│   main.py
│   requirements.txt
│       
├───config
│       env.py
│       __init__.py
│       
├───database
│       manager.py
│       model.py
│       repos.py
│       _abcrepos.py
│       __init__.py
│       
├───migrations
│   │   env.py
│   │   README
│   │   script.py.mako
│   │   
│   └───versions
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
│   └───author
│           depends.py
│           router.py
│           schemas.py
│           __init__.py
│           
└───tasks
        celery.py
        __init__.py
        

```
