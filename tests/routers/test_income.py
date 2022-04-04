import logging

from app.enums import Unit

logger = logging.getLogger('test')


def test_income_get_all(auth_user, client):
    """make a get request to fetch all incomes. expect to get back
    3 incomes.
    """

    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get('/income/all', headers=headers)

    data = response.json()

    logger.debug(f"get response income all => {data}")
    # logger.debug(f"get response income all => {len(data)}")

    assert response.status_code == 200
    assert len(data) == 3


def test_income_post_hour_rate(auth_user, client):
    """create a new income for customer_id 1 with 10 hours. The netto
    rate is 10. So expect the expected_data back:
    """

    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}
    input_data = {
        "total": 10,
        "contract_id": 1,
        "invoice_date": "2010-01-24",
    }

    response = client.post('/income/', json=input_data, headers=headers)
    data = response.json()

    expected_data = {
        'total': 10.0,
        'invoice_month_year': 'Jan-2010',
        'total_rate_excl_vat': 200.0,
        'total_rate_incl_vat': 242.0,
        'total_yearly_vat': 120.0,
        'total_netto': 80.0,
        'customer_name': 'Bar',
        'rate_unit': Unit.HOUR.value,
        'contract_id': 1,
        'invoice_date': '2010-01-24',
        'id': 4
    }

    logger.debug(f"response income: {response}")
    logger.debug(f"income data: {data}")
    data.pop('created')  # remove the created key

    assert response.status_code == 200
    assert data == expected_data


def test_income_post_day_rate(auth_user, client):
    """create a new income for customer_id 3 and contract 3 with 3 days. The netto
    rate is 30. So expect the expected_data back:
    """

    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}
    input_data = {
        "total": 3,
        "contract_id": 3,
        "invoice_date": "2011-03-01",
    }

    response = client.post('/income/', json=input_data, headers=headers)
    data = response.json()

    expected_data = {
        'total': 3.0,
        'invoice_month_year': 'Mar-2011',
        'total_rate_excl_vat': 90.0,
        'total_rate_incl_vat': 108.90,
        'total_yearly_vat': 54.0,
        'total_netto': 36.0,
        'customer_name': 'Bar3',
        'rate_unit': Unit.DAY.value,
        'contract_id': 3,
        'invoice_date': '2011-03-01',
        'id': 5,
    }

    logger.debug(f"response income: {response}")
    logger.debug(f"income data: {data}")
    data.pop('created')  # remove the created key

    assert response.status_code == 200
    assert data == expected_data


def test_get_income_by_start_date_end_date(auth_user, client):
    """make a get request with a start_date only. with the start_date
    2010-02-01 and a future end date that has no invoice after
    Expect 2 records starting from 2010-02-01.
    """

    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        '/income/by_date/2010-03-01/2022-04-01/',
        headers=headers
        )
    data = response.json()

    expected_data = [
        {
            'id': 3,
            'contract_id': 3,
            'invoice_month_year': 'Mar-2022',
            'total_rate_excl_vat': 90.0,
            'total_rate_incl_vat': 108.9,
            'total_yearly_vat': 54.0,
            'total_netto': 36.0,
            'rate_unit': 'day'
        },
        {
            'id': 5,
            'contract_id': 3,
            'invoice_month_year': 'Mar-2011',
            'total_rate_excl_vat': 90.0,
            'total_rate_incl_vat': 108.9,
            'total_yearly_vat': 54.0,
            'total_netto': 36.0,
            'rate_unit': 'day'
        }
    ]

    logger.debug(f"response income: {response}")
    logger.debug(f"income data: {data}")
    logger.debug(f"income total records data: {len(data)}")

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0] == expected_data[0]

    assert data[1] == expected_data[1]


def test_get_income_by_start_end_date_1_record(auth_user, client):
    """make a get request with a start_date 2010-02-01 and end
    date 2011-04-01. Expect 1 record starting from 2010-02-01.
    """

    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        '/income/by_date/2010-03-01/2011-04-01/',
        headers=headers
    )
    data = response.json()

    expected_data = [
        {
            'id': 5,
            'contract_id': 3,
            'invoice_month_year': 'Mar-2011',
            'total_rate_excl_vat': 90.0,
            'total_rate_incl_vat': 108.9,
            'total_yearly_vat': 54.0,
            'total_netto': 36.0,
            'rate_unit': 'day'
        }
    ]

    logger.debug(f"response income: {response}")
    logger.debug(f"income data: {data}")
    logger.debug(f"income total records data: {len(data)}")

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0] == expected_data[0]


def test_get_income_by_customer(auth_user, client):
    """make a get request with a customer_id only. with the customer_id 1
    Expect 1 record starting for customer .
    """

    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get('/income/by_customer/1/', headers=headers)
    data = response.json()

    expected_data = [
        {
            'contract_id': 1,
            'id': 1,
            'invoice_month_year': 'Jan-2010',
            'total_rate_excl_vat': 20.0,
            'total_rate_incl_vat': 24.2,
            'total_yearly_vat': 12.0,
            'total_netto': 8.0,
            'rate_unit': 'hour',
        },
        {
            'contract_id': 1,
            'id': 4,
            'invoice_month_year': 'Jan-2010',
            'total_rate_excl_vat': 200.0,
            'total_rate_incl_vat': 242.0,
            'total_yearly_vat': 74.14,
            'total_netto': 125.86,
            'rate_unit': 'hour',
        }
    ]

    logger.debug(f"response income: {response}")
    logger.debug(f"income data: {data}")

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0] == expected_data[0]
