Python API Course
https://www.youtube.com/watch?v=PuQzQNJZ4c8&list=PL8VzFQ8k4U1L5QpSapVEzoSfob-4CR8zM&index=10

Needed to get phppgadmin working:
sudo pkg install mod_php83

Stop nginx if it's running else just start apache.
Then go to localhost/ phpPgAdmin in browser 

sudo service nginx stop
sudo service apache24 start

sudo pkg install py311-poetry
poetry --version                (main)fastapi-course
Poetry (version 1.7.1)

to start: 
cd ~/projects/python/fastapi-course
poetry shell
uvicorn app.main:app --reload
