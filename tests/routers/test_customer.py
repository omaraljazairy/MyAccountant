import logging

logger = logging.getLogger('test')


def test_post_customer(client):

    response = client.post("/customer/", json={"name": "bar"})
    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 201


def test_post_customer_exists_409(client):
    """post an existing customer, should get back 409 error"""

    response = client.post("/customer/", json={"name": "Bar"})
    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 409


def test_put_customer_found(client):
    """update customer with id 2 Bar to BOA."""

    response = client.put("/customer/update/", json={"id": 2, "name": "BOA"})
    logger.debug(f"response from update: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 200


def test_put_customer_not_found_404(client):
    """update customer with id 1000 that doesn't exist. expect statuscode 404
    not found."""

    response = client.put("/customer/update/", json={
        "id": 1000,
        "name": "BBB"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 404


def test_delete_customer_success(client):
    """delete customer with id 5 and expect statuscode 200."""

    response = client.delete("/customer/delete/customer_id/5/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 204


def test_delete_customer_not_found(client):
    """delete customer with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/customer/delete/customer_id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 404


# def test_delete_customer_exist_in_contract_error(client):
#     """delete a customer that is a foreign key, should return an error."""

#     response = client.delete("/customer/delete/customer_id/1/")
#     logger.debug(f"response from delete: {response}")
#     logger.debug(f"response content: {response.json()}")
#     logger.debug(f"response headers: {response.content}")

#     assert response.status_code == 500


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
    assert len(content) > 2


def test_get_1_customer_with_his_contract(client, auth_user):
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
