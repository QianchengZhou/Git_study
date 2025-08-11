from locust import HttpUser, task, between, LoadTestShape


class MyUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://httpbin.org"

    @task
    def index(self):
        self.client.get("/")


class RealisticLoadShape(LoadTestShape):
    stages = [
        {"duration": 300, "users": 200, "spawn_rate": 4},  # 缓慢预热阶段
        {"duration": 600, "users": 1000, "spawn_rate": 50},  # 快速爆发增长
        {"duration": 900, "users": 1000, "spawn_rate": 0},  # 稳定高峰
        {"duration": 1200, "users": 200, "spawn_rate": 20},  # 缓慢退出
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None  # 结束测试
