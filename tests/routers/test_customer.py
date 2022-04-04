import logging

logger = logging.getLogger('test')


def test_post_customer(client):

    response = client.post("/customer/", json={"name": "bar"})
    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 200


def test_get_all_customers(client, auth_user):
    """call the api customer/all/ to get a list of all customers. should
    return 5 customers.
    """

    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/customer/all/", headers=headers)
    statuscode = response.status_code
    content = response.json()
    logger.debug(f"response from all customers: {response}")
    logger.debug(f"response headers: {response.content}")

    assert statuscode == 200
    assert len(content) == 5


def test_get_1_customer_with_hist_contract(client, auth_user):
    """call the api customer/1/ to get customer with related contracts.
    """

    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/customer/1/", headers=headers)
    statuscode = response.status_code
    content = response.json()
    logger.debug(f"response from all customers: {response}")
    logger.debug(f"response headers: {response.content}")

    customer_id = content['id']
    customer_name = content['name']
    customer_contracts = content['contract']

    assert statuscode == 200
    assert len(customer_contracts) == 2
    assert customer_id == 1
    assert customer_name == 'Bar'
