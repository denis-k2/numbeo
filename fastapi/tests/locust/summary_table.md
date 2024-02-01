Testing is carried out on a laptop with the following characteristics
- CPU: Ryzen 5 2500u = 4 Cores, 8 Threads, 2.0 -> 3.6 GHz
- RAM: DDR4, 2400 MHz
- SSD: Timing buffered disk reads = 645 MB/sec


- Postgres version: 15.5
- Locust version: 2.20.1


Whole run commands in Docker Compose (examples):
- **FastAPI**: `uvicorn main:app --workers 9 --host 0.0.0.0`, `gunicorn main:app -w 9 -k uvicorn.workers.UvicornWorker -b 0.0.0.0`
- **Locust**: `locust -H http://127.0.0.1:8000 -u 500 -r 2 -t 600s --autostart --modern-ui`

Number of workers:
- *4 workers* — most common recommendation, regardless of CPU
- *9 workers* — recommendation from [gunicorn docs](https://docs.gunicorn.org/en/latest/design.html#how-many-workers)
  (4 * 2 + 1 = 9)
- *12 workers* — experiment


### Sync code (Release 0.1.1)

| **#**                                                                            | **Run command**                                          | **Locust**          | **# Requests** | **# Fails** | **Median (ms)** | **90%ile (ms)**  | **99%ile (ms)** | **Average (ms)** | **Min (ms)** | **Max (ms)** | **Average size (bytes)** | **Current RPS** | **Current Failures/s** |
|----------------------------------------------------------------------------------|----------------------------------------------------------|---------------------|----------------|-------------|-----------------|------------------|-----------------|------------------|--------------|--------------|--------------------------|-----------------|----------------------|
| [1](https://denis-k2.github.io/Relohelper/LocustReports/sync_code/report_1.html) | uvicorn main:app                                         | -u 180 -r 2 -t 420s | 22229          | 29          | 56              | 160              | 320             | 77.35            | 2            | 525          | 9689.62                  | 59.5            | 0.1                  |
| [2](https://denis-k2.github.io/Relohelper/LocustReports/sync_code/report_2.html) | uvicorn main:app --workers 4                             | -u 500 -r 2 -t 600s | 77251          | 119         | 49              | 230              | 600             | 96.1             | 3            | 2611         | 9767.05                  | 163.2           | 0.1                  |
| [3](https://denis-k2.github.io/Relohelper/LocustReports/sync_code/report_3.html) | uvicorn main:app --workers 9                             | -u 500 -r 2 -t 600s | 77094          | 117         | 57              | 190              | 470             | 88.59            | 2            | 1472         | 9773.07                  | 161.9           | 0.4                  |
| [4](https://denis-k2.github.io/Relohelper/LocustReports/sync_code/report_4.html) | gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker  | -u 180 -r 2 -t 420s | 22059          | 30          | 53              | 150              | 310             | 73.65            | 2            | 467          | 9777.65                  | 57.1            | 0.2                  |
| [5](https://denis-k2.github.io/Relohelper/LocustReports/sync_code/report_5.html) | gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker  | -u 500 -r 2 -t 600s | 76045          | 231         | 85              | 330              | 580             | 136.28           | 2            | 1043         | 9764.47                  | 156.8           | 0.4                  |
| [6](https://denis-k2.github.io/Relohelper/LocustReports/sync_code/report_6.html) | gunicorn main:app -w 9 -k uvicorn.workers.UvicornWorker  | -u 500 -r 2 -t 600s | 78482          | 105         | 40              | 100              | 280             | 55.44            | 2            | 921          | 9777.23                  | 165.3           | 0.6                  |
| [7](https://denis-k2.github.io/Relohelper/LocustReports/sync_code/report_7.html) | gunicorn main:app -w 12 -k uvicorn.workers.UvicornWorker | -u 500 -r 2 -t 600s | 78103          | 102         | 40              | 98               | 280             | 53.61            | 2            | 899          | 9803.14                  | 160.7           | 0                    |

### Async code (Release 0.2.0)

| **#**                                                                             | **Run command**                                          | **Locust**          | **# Requests** | **# Fails** | **Median (ms)** | **90%ile (ms)** | **99%ile (ms)** | **Average (ms)** | **Min (ms)** | **Max (ms)** | **Average size (bytes)** | **Current RPS** | **Current Failures/s** |
|-----------------------------------------------------------------------------------|----------------------------------------------------------|---------------------|----------------|-------------|-----------------|-----------------|-----------------|------------------|--------------|--------------|--------------------------|-----------------|------------------------|
| [1](https://denis-k2.github.io/Relohelper/LocustReports/async_code/report_1.html) | uvicorn main:app                                         | -u 180 -r 2 -t 420s | 21456          | 49          | 57              | 470             | 840             | 163.96           | 4            | 1740         | 9730.55                  | 55.3            | 0.3                    |
| [2](https://denis-k2.github.io/Relohelper/LocustReports/async_code/report_2.html) | uvicorn main:app --workers 4                             | -u 500 -r 2 -t 600s | 74705          | 196         | 58              | 640             | 1200            | 208.14           | 3            | 2300         | 9803.03                  | 153.2           | 0.1                    |
| [3](https://denis-k2.github.io/Relohelper/LocustReports/async_code/report_3.html) | uvicorn main:app --workers 9                             | -u 500 -r 2 -t 600s | 75816          | 468         | 54              | 340             | 1900            | 157.28           | 3            | 3512         | 9665.16                  | 162.6           | 0.4                    |
| [4](https://denis-k2.github.io/Relohelper/LocustReports/async_code/report_4.html) | gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker  | -u 180 -r 2 -t 420s | 21317          | 73          | 99              | 570             | 910             | 207.08           | 3            | 1617         | 9817.02                  | 53              | 0.2                    |
| [5](https://denis-k2.github.io/Relohelper/LocustReports/async_code/report_5.html) | gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker  | -u 500 -r 2 -t 600s | 71544          | 529         | 200             | 880             | 1500            | 332.88           | 2            | 2967         | 9687.34                  | 147             | 1.2                    |
| [6](https://denis-k2.github.io/Relohelper/LocustReports/async_code/report_6.html) | gunicorn main:app -w 9 -k uvicorn.workers.UvicornWorker  | -u 500 -r 2 -t 600s | 78674          | 100         | 32              | 68              | 210             | 41.49            | 2            | 687          | 9761.63                  | 164.6           | 0.2                    |
| [7](https://denis-k2.github.io/Relohelper/LocustReports/async_code/report_7.html) | gunicorn main:app -w 12 -k uvicorn.workers.UvicornWorker | -u 500 -r 2 -t 600s | 78543          | 100         | 34              | 76              | 230             | 44.45            | 2            | 889          | 9724.24                  | 163.9           | 0.2                    |
| [8](https://denis-k2.github.io/Relohelper/LocustReports/async_code/report_8.html) | gunicorn main:app -w 9 -k uvicorn.workers.UvicornWorker  | -u 700 -r 2 -t 600s | 86208          | 19571       | 370             | 980             | 2300            | 455.79           | 2            | 5422         | 7584.62                  | 192.3           | 67.3                   |



`--log-level critical` — doesn't use 


