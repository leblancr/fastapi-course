Python API Course
https://www.youtube.com/watch?v=PuQzQNJZ4c8&list=PL8VzFQ8k4U1L5QpSapVEzoSfob-4CR8zM&index=10

Needed to get phppgadmin working:
sudo pkg install mod_php83

Stop nginx if it's running else just start apache.
Then go to localhost/ phpPgAdmin in browser 

sudo service nginx stop
sudo service apache24 start - serves phppgadmin

sudo pkg install py311-poetry
poetry --version                (main)fastapi-course
Poetry (version 1.7.1)

to start: 
cd ~/projects/python/fastapi-course/fastapi-course/app - have to be in directory with models.
poetry shell
To start this serves our app on http://127.0.0.1:8000 or localhost:
(fastapi-course-py3.11) rich@b450m-a /home/rich/projects/python/fastapi-course/fastapi-course/app $ uvicorn main:app --reload                                                                                       

Errors:
poetry install     
Installing dependencies from lock file

Package operations: 1 install, 0 updates, 0 removals

  • Installing uvicorn (0.24.0.post1): Failed

  PermissionError

  [Errno 13] Permission denied: '/usr/local/bin/uvicorn'

  at /usr/local/lib/python3.11/pathlib.py:1044 in open
      1040│         the built-in open() function does.
      1041│         """
      1042│         if "b" not in mode:
      1043│             encoding = io.text_encoding(encoding)
    → 1044│         return io.open(self, mode, buffering, encoding, errors, newline)
      1045│ 
      1046│     def read_bytes(self):
      1047│         """
      1048│         Open the file in bytes mode, read it, and close the file.

Cannot install uvicorn.

(fastapi-course-py3.11) rich@b450m-a /home/rich/projects/python/fastapi-course $ sudo chown -R $(whoami) /usr/local/bin
(fastapi-course-py3.11) rich@b450m-a /home/rich/projects/python/fastapi-course $ poetry install
Installing dependencies from lock file

Package operations: 1 install, 0 updates, 0 removals

  • Installing uvicorn (0.24.0.post1)

Installing the current project: fastapi-course (0.1.0)

raise TypeError('{!r} is not a callable object'.format(obj))
TypeError: <generator object get_db at 0x1f007a3901e0> is not a callable object

Depends(database.get_db()) should be: Depends(database.get_db)), remove parenthesis