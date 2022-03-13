# from starlette.testclient import TestClient
# from app.main import app
# from decorators.test_db import temp_db
import logging


logger = logging.getLogger('test')
# client = TestClient(app)


def test_post_customer(client):
    
    response = client.post("/customer/", json={"name":"bar"})
    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")
    
    assert response.status_code == 200