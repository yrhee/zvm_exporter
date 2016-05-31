import httpretty
from zvm_exporter.requester import Requester


@httpretty.activate
def test_requester():
    r = Requester("dummy", "user", "password", "example.com", 443)
    httpretty.register_uri(httpretty.PUT, "http://example.com:443",
                           status=200, body="test", content_type='text/plain')
    r.send_request("test text")
    last_request = httpretty.last_request()
    assert last_request.querystring["userName"] == ["user"]
    assert last_request.querystring["password"] == ["password"]
    assert last_request.headers['content-type'] == 'text/plain'
    assert last_request.headers['content-length'] != 0
    assert last_request.parsed_body == '["command=smcli test text"]'
