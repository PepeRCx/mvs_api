# MVS APi

> [!IMPORTANT]
> Python version 3.8 or greater required

You'll need a virtual environment in order to run the api, create it with:
```
python3 -m venv venv
source venv/bin/activate
```

then install the required libraries with:
````
pip install -r requirements.txt
```

create your .env, you just need one var (you can use any name for your database, it will be created automatically):
```
DATABASE_NAME=name_it_as_you_want
```

and finally run the api with:
````
fastapi dev src/main.py
```

you can test all the endpoints just by pasting this in your browser:

http://127.0.0.1:8000/docs

All documentation is there build with swaggerAPI