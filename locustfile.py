from locust import HttpUser, between, task


class MinimumLoadTest(HttpUser):
    wait_time = between(5, 15)

    @task
    def test_status(self):
        self.client.get("/api/test/!status")
