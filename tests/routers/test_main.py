import logging

logger = logging.getLogger('test')


def test_read_main(client, auth_user):
    token = auth_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/", headers=headers)
    logger.debug(f"response: {response}")

    assert response.status_code == 200
