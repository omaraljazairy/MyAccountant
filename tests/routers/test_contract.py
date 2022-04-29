import logging

from app.enums import Unit

logger = logging.getLogger('test')


def test_post_contract_success_200(client):

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


def test_post_contract_unknown_customer_404(client):
    """provide an unknown customer_id, expect 404."""

    response = client.post("/contract/", json={
        "customer_id": 900,
        "rate": 15.8,
        "unit": Unit.HOUR.value,
        "start_date": '2012-11-01'
        }
    )
    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 404


def test_post_contract_missing_required_field_422(client):

    response = client.post("/contract/", json={
        "customer_id": 1,
        "rate": 15.8,
        "unit": Unit.HOUR.value,
        "start_date": '2012-11-0122'
        }
    )
    content = response.json()

    logger.debug(f"response: {response}")
    logger.debug(f"response content: {content}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 422


def test_patch_unit_success(client):
    """update the unit only of the contract with id 3. expect response 200."""

    response = client.patch("/contract/update/contract_id/4/", json={
        "unit": "hour"
    })

    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 200


def test_patch_rate_success(client):
    """update the rate only of the contract with id 3. expect response 200."""

    response = client.patch("/contract/update/contract_id/4/", json={
        "rate": 16
    })

    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 200


def test_patch_unknown_contractid_404(client):
    """provide an unknown contractid, expect a 404."""

    response = client.patch("/contract/update/contract_id/400/", json={
        "rate": 16
    })

    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 404


def test_delete_contractid_success(client):
    """delete a contractid and expect a 204 response."""

    response = client.delete("/contract/delete/contract_id/4/")

    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 204


def test_delete_contractid_not_exist(client):
    """delete a contractid that does not exist and expect a 404 response."""

    response = client.delete("/contract/delete/contract_id/400/")

    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 404


def test_get_all_contracts_list_200(client):
    """get all contracts as a list with more than 1 contract and
    a 200 response.
    """
    response = client.get("/contract/all/")
    contracts = response.json()

    logger.debug(f"response: {response}")
    logger.debug(f"response headers: {response.content}")

    assert response.status_code == 200
    assert type(contracts) == list
    assert len(contracts) > 1


def test_get_contract_by_id_details_200(client):
    """get contract details for contract_id 2. expect a dict."""

    response = client.get("/contract/contract_id/1/")
    contract = response.json()

    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")
    logger.debug(f"response contract: {contract}")

    expected_contract = {
        'id': 1,
        'customer': {
            'id': 1,
            'name': 'Bar'
        },
        'rate': 20.0,
        'unit': Unit.HOUR.value,
        'start_date': '2010-01-01',
        'income': [
            {
                'id': 1,
                'total': 1.0,
                'invoice_month_year': 'Jan-2010',
                'total_rate_excl_vat': 20.0,
                'total_rate_incl_vat': 24.2,
                'total_yearly_vat': 12.0,
                'total_netto': 8.0
            }
        ]
    }
    contract.pop('created')  # delete the created key
    logger.debug(f"contract: {contract}")

    assert response.status_code == 200
    assert contract == expected_contract
