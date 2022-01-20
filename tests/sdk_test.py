from okdata.sdk import SDK


def test_content_type(requests_mock):
    client = SDK()
    payload = {"foo": "bar"}
    endpoint = "mock://api.com/foo"

    for method in ["patch", "post", "put"]:
        getattr(requests_mock, method)(endpoint)
        getattr(client, method)(endpoint, payload)

        req = requests_mock.last_request

        assert "Content-Type" in req.headers
        assert req.headers["Content-Type"] == "application/json"
        assert req.json() == payload
