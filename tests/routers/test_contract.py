# from starlette.testclient import TestClient
# from app.main import app
# from decorators.test_db import temp_db
import logging
from app.enums import Unit


logger = logging.getLogger('test')
# client = TestClient(app)


def test_post_contract(client):

    response = client.post("/contract/", json={
        "customer_id": 1,
        "rate": 15.8,
        "unit": Unit.HOUR.value,
        "start_date": '2012-11-01'
        }
    )
    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 200
