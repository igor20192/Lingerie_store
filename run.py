import subprocess

# subprocess.run(["docker-compose", "up", "-d"])
subprocess.run(["python", "manage.py", "runserver"])
