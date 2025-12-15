import json
from unittest.mock import Mock
from consumer import callback


def test_callback(monkeypatch):
    test_data = {"img_url": "https://example.com/image.jpg"}
    body = json.dumps(test_data).encode()
    monkeypatch.setattr("consumer.load_image_from_url", lambda url: "fake_image")
    monkeypatch.setattr("consumer.process_img", lambda img: 3)
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_post = Mock(return_value=mock_response)
    monkeypatch.setattr("consumer.requests.post", mock_post)
    mock_channel = Mock()
    mock_method = Mock()
    mock_method.delivery_tag = "123"
    callback(mock_channel, mock_method, None, body)
    mock_channel.basic_ack.assert_called_once_with(delivery_tag="123")
