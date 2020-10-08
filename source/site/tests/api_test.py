import source.site.rest_api_impl as api

def test_thatTestRuns():
    mynum = 1
    assert 1 == mynum

def test_parseSpeedStr():
    actualResponse = api.parseSpeedStr('')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.parseSpeedStr('dummy')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.parseSpeedStr('10')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.parseSpeedStr('10k')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.parseSpeedStr('10kph')
    assert 0 == actualResponse['exitcode']

def test_parsePaceStr():
    actualResponse = api.parsePaceStr('')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.parsePaceStr('dummy')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.parsePaceStr('10')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.parsePaceStr('10m')
    assert 5 == actualResponse['exitcode']

    actualResponse = api.parsePaceStr('10 min mile')
    assert 0 == actualResponse['exitcode']

def test_parseTargetEventStr():
    actualResponse = api.parseTargetEventStr('')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.parseTargetEventStr('dummy')
    assert 4 == actualResponse['exitcode']

    actualResponse = api.parseTargetEventStr('10')
    assert 4 == actualResponse['exitcode']

    actualResponse = api.parseTargetEventStr('10m')
    assert 0 == actualResponse['exitcode']

def test_getEventTimeWithSpeed():
    actualResponse = api.getEventTimeWithSpeed('', '')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.getEventTimeWithSpeed('speedDummyStr', 'eventDummyStr')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.getEventTimeWithSpeed('10', 'm')
    assert 2 == actualResponse['exitcode']

    actualResponse = api.getEventTimeWithSpeed('10kph', '400m')
    assert 0 == actualResponse['exitcode']
