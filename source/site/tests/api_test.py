import pytest
import source.site.rest_api_impl as api
from source.speedmath.errCodes import errCodes, smException

def test_parseSpeedStr():
    response = api.parseSpeedStr('')
    assert not response['completeRequest']

    response = api.parseSpeedStr('dummy')
    assert not response['completeRequest']

    response = api.parseSpeedStr('10')
    assert not response['completeRequest']

    response = api.parseSpeedStr('10k')
    assert not response['completeRequest']

    response = api.parseSpeedStr('10kph')
    assert response['completeRequest']

def test_parsePaceStr():
    response = api.parsePaceStr('')
    assert not response['completeRequest']

    response = api.parsePaceStr('dummy')
    assert not response['completeRequest']

    response = api.parsePaceStr('10')
    assert not response['completeRequest']

    response = api.parsePaceStr('10m')
    assert not response['completeRequest']

    response = api.parsePaceStr('10 min mile')
    assert response['completeRequest']

def test_parseTargetEventStr():
    response = api.parseTargetEventStr('')
    assert not response['completeRequest']

    response = api.parseTargetEventStr('dummy')
    assert not response['completeRequest']

    response = api.parseTargetEventStr('10')
    assert not response['completeRequest']

    response = api.parseTargetEventStr('10m')
    assert response['completeRequest']

def assertFuncRaisesException(func, theErrorCode):
    with pytest.raises(smException) as e:
        func()
    assert e.value.error_code == theErrorCode

def test_getEventTimeWithSpeed():
    assertFuncRaisesException(lambda: api.getEventTimeWithSpeed('', ''), errCodes.PARSE_ERR)
    assertFuncRaisesException(lambda: api.getEventTimeWithSpeed('speedDummyStr', 'eventDummyStr'), errCodes.PARSE_ERR)
    assertFuncRaisesException(lambda: api.getEventTimeWithSpeed('10', 'm'), errCodes.PARSE_ERR)

    response = api.getEventTimeWithSpeed('10kph', '400m')
    assert 'time' in response
