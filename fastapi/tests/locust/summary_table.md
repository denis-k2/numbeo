Testing is carried out on a laptop with the following characteristics:
- CPU: Ryzen 5 2500u = 4 Cores, 8 Threads, 2.0 -> 3.6 GHz
- RAM: DDR4, 2400 MHz
- SSD: Timing buffered disk reads = 504.93 MB/sec


Full commands (examples)
- **FastAPI**: `uvicorn main:app --workers 4 --log-level critical`, `gunicorn main:app --workers 9 --worker-class uvicorn.workers.UvicornWorker`
- **Locust**: `locust -H http://127.0.0.1:8000 -u 500 -r 2 -t 420s --autostart --modern-ui`


- *4 workers* — most common recommendation, regardless of CPU
- *9 workers* — recommendation from [gunicorn docs](https://docs.gunicorn.org/en/latest/design.html#how-many-workers)
  (4 * 2 + 1 = 9)
- *12 workers* — experiment


### Sync code (Relese 0.1.0)

| **#**                                                                   | **Run command**                                                             | **Locust**          | **# Requests** | **# Fails** | **Median (ms)** | **90%ile (ms)** | **99%ile (ms)** | **Average (ms)** | **Min (ms)** | **Max (ms)** | **Average size (bytes)** | **Current RPS** | **Current Failures/s** |
|-------------------------------------------------------------------------| --------------------------------------------------------------------------- | ------------------- | -------------- | ----------- | --------------- | --------------- | --------------- | ---------------- | ------------ | ------------ | ------------------------ | --------------- | ---------------------- |
| [1](/relohelper/fastapi/tests/locust/reports/sync_code/report_1.html)   | uvicorn main:app                                                            | -u 180 -r 2 -t 420s | 22061          | 24          | 74              | 200             | 340             | 96.7             | 2            | 565          | 9809.42                  | 58.6            | 0.1                    |
| [2](/relohelper/fastapi/tests/locust/reports/sync_code/report_2.html)   | uvicorn main:app                                                            | -u 150 -r 2 -t 420s | 18946          | 14          | 47              | 120             | 290             | 62.62            | 2            | 462          | 9766.72                  | 49.5            | 0                      |
| [3](/relohelper/fastapi/tests/locust/reports/sync_code/report_3.html)   | uvicorn main:app --workers 4                                                | -u 500 -r 2 -t 420s | 49177          | 28          | 33              | 85              | 310             | 46.87            | 2            | 636          | 9771.8                   | 163             | 0                      |
| [4](/relohelper/fastapi/tests/locust/reports/sync_code/report_4.html)   | uvicorn main:app --workers 4                                                | -u 600 -r 2 -t 420s | 50969          | 100         | 64              | 730             | 1400            | 233.56           | 2            | 4026         | 9737.25                  | 168.2           | 1.1                    |
| [5](/relohelper/fastapi/tests/locust/reports/sync_code/report_5.html)   | uvicorn main:app --workers 4 --log-level critical                           | -u 500 -r 2 -t 420s | 49098          | 35          | 31              | 78              | 300             | 44.06            | 2            | 468          | 9809.99                  | 163.3           | 0.1                    |
| [6](/relohelper/fastapi/tests/locust/reports/sync_code/report_6.html)   | uvicorn main:app --workers 9                                                | -u 500 -r 2 -t 420s | 49313          | 18          | 28              | 56              | 290             | 36.44            | 2            | 498          | 9735.94                  | 164.3           | 0                      |
| [7](/relohelper/fastapi/tests/locust/reports/sync_code/report_7.html)   | uvicorn main:app --workers 9                                                | -u 600 -r 2 -t 420s | 53515          | 91          | 40              | 210             | 560             | 84.52            | 2            | 1046         | 9730.86                  | 188             | 1                      |
| [8](/relohelper/fastapi/tests/locust/reports/sync_code/report_8.html)   | uvicorn main:app --workers 9 —log-level critical                            | -u 600 -r 2 -t 420s | 54142          | 39          | 29              | 72              | 320             | 42.23            | 1            | 596          | 9746.39                  | 199.8           | 0.1                    |
| [9](/relohelper/fastapi/tests/locust/reports/sync_code/report_9.html)   | gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker  | -u 150 -r 2 -t 420s | 18894          | 17          | 44              | 120             | 260             | 59.52            | 1            | 401          | 9841.12                  | 49.6            | 0                      |
| [10](/relohelper/fastapi/tests/locust/reports/sync_code/report_10.html) | gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker  | -u 500 -r 2 -t 420s | 49245          | 44          | 33              | 84              | 320             | 47.63            | 2            | 773          | 9747.66                  | 163.5           | 0.5                    |
| [11](/relohelper/fastapi/tests/locust/reports/sync_code/report_11.html) | gunicorn main:app --workers 9 --worker-class uvicorn.workers.UvicornWorker  | -u 500 -r 2 -t 420s | 49377          | 27          | 29              | 58              | 290             | 37               | 2            | 467          | 9718.23                  | 163             | 0                      |
| [12](/relohelper/fastapi/tests/locust/reports/sync_code/report_12.html) | gunicorn main:app --workers 9 --worker-class uvicorn.workers.UvicornWorker  | -u 600 -r 2 -t 420s | 54299          | 39          | 30              | 62              | 300             | 39.04            | 2            | 453          | 9729.45                  | 199.5           | 0.1                    |
| [13](/relohelper/fastapi/tests/locust/reports/sync_code/report_13.html) | uvicorn main:app --workers 12                                               | -u 600 -r 2 -t 420s | 53476          | 79          | 38              | 180             | 520             | 76.51            | 2            | 1275         | 9740.91                  | 194.1           | 0.8                    |
| [14](/relohelper/fastapi/tests/locust/reports/sync_code/report_14.html) | uvicorn main:app --workers 12 —log-level critical                           | -u 600 -r 2 -t 420s | 54072          | 22          | 29              | 71              | 320             | 41.38            | 2            | 503          | 9706.6                   | 192.6           | 0                      |
| [15](/relohelper/fastapi/tests/locust/reports/sync_code/report_15.html) | gunicorn main:app --workers 12 --worker-class uvicorn.workers.UvicornWorker | -u 600 -r 2 -t 420s | 54194          | 26          | 30              | 59              | 300             | 38.12            | 2            | 485          | 9715.03                  | 195.8           | 0.1                    |




