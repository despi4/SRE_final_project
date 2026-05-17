import uuid

from locust import HttpUser, task, between


class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def list_users(self):
        self.client.get("/api/v1/users")

    @task(5)
    def list_products(self):
        self.client.get("/api/v1/products/sample")

    @task(3)
    def list_orders(self):
        self.client.get("/api/v1/orders/sample")

    @task(2)
    def get_health(self):
        self.client.get("/health")

    @task(1)
    def create_user(self):
        self.client.post(
            "/api/v1/users",
            json={
                "email": f"loadtest+{uuid.uuid4().hex}@example.com",
                "full_name": "Load Test User"
            },
        )
