from locust import HttpUser, task, between

class ProjectPerfTest(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 3)

    
    @task()
    def home(self):
        self.client.get("/")
    @task()
    def showSummary(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")
    @task()
    def showSummary(self):
        self.client.get("/display")