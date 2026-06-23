# Блок 3.5 — Docker и контейнеризация
---
## [Репозиторий с работой]()
## Результаты
1. Image = 206MB
```bash
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ docker images
REPOSITORY                                                      TAG       IMAGE ID       CREATED          SIZE
llm-service                                                     dev       c9a3d8c7c88a   12 minutes ago   206MB
2. Ready
```bash
{"status":"ok"}(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS                   PORTS                                         NAMES
b2f94d2edec6   llm-service:dev    "uvicorn app.main:ap…"   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   llm-service
79dd0b2c3902   redis:7.4-alpine   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes (healthy)   6379/tcp                                      llm-redis
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ curl http://172.16.30.101:8000/health
{"status":"ok"}(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ curl http://172.16.30.101:8000/ready
{"status":"ok","redis":"up"}(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$
```
3. Secrets
```bash
(netology-ai-dev) odv@matebook16s:~/project/MY/Netology-AI-Dev$ docker run --rm llm-service:dev ls -la /app
total 192
drwxr-xr-x 1 root    root      4096 Jun 23 20:24 .
drwxr-xr-x 1 root    root      4096 Jun 23 20:33 ..
drwxr-xr-x 4 appuser appuser   4096 Jun 23 17:54 .venv
drwxr-xr-x 9 appuser appuser   4096 Jun 22 14:27 app
-rw-rw-r-- 1 appuser appuser    860 Jun 22 15:21 pyproject.toml
-rw-rw-r-- 1 appuser appuser 174551 Jun 22 14:27 uv.lock
```
