import unittest
import telapi.telml as telml

class TestAllTelml(unittest.TestCase):
    def setUp(self):
        self.response = telml.Response()



    # Response
    def test_response(self):
        with self.assertRaises(ValueError):
            self.assertEqual(str(self.response), '<Response></Response>')



    # Say
    def test_say_no_body(self):
        with self.assertRaises(ValueError):
            str(telml.Say())

    def test_bad_child(self):
        with self.assertRaises(TypeError):
            say = telml.Say('Hi')
            say.append(telml.Say("there"))

    def test_say_body(self):
        self.response.append(telml.Say('Hello there'))
        self.assertEqual(str(self.response), '<Response><Say>Hello there</Say></Response>')

    def test_say_bad_attributes(self):
        with self.assertRaises(AttributeError):
            telml.Say('hello', loops=5)

    def test_say_all_attributes(self):
        self.response.append(telml.Say('Hello there', voice='man', loop=1))
        self.assertEqual(str(self.response), '<Response><Say voice="man" loop="1">Hello there</Say></Response>')



    # Play
    def test_play_body(self):
        self.response.append(telml.Play('http://test.url.com/myfile.mp3', loop=1))
        self.assertEqual(str(self.response), '<Response><Play loop="1">http://test.url.com/myfile.mp3</Play></Response>')



    # Gather
    def test_gather(self):
        self.response.append(telml.Gather())
        self.assertEqual(str(self.response), '<Response><Gather></Gather></Response>')

    def test_gather_attributes(self):
        self.response.append(telml.Gather(action="http://mysite.com/gather/", method="POST", timeout=10, 
            finishOnKey='true', numDigits=5))
        self.assertEqual(str(self.response), 
            '<Response><Gather finishOnKey="true" action="http://mysite.com/gather/" method="POST" timeout="10" numDigits="5"></Gather></Response>')

    def test_gather_bad_attributes(self):
        with self.assertRaises(AttributeError):
            self.response.append(telml.Gather(action="http://mysite.com/gather/", method="POST", timeout=10, 
                finishOnKey='true', numdigits=5))

    def test_gather_children(self):
        self.response.append(
            telml.Gather(
                telml.Say('Enter digits'), 
                telml.Play('http://test.com/pound.mp3'), 
                telml.Pause(), 
                telml.Say("Followed by pound key"),
                timeout = 30
            )
        )
        self.assertEqual(str(self.response), 
            '<Response><Gather timeout="30"><Say>Enter digits</Say><Play>http://test.com/pound.mp3</Play><Pause></Pause><Say>Followed by pound key</Say></Gather></Response>')



    # Record
    def test_record_attributes(self):
        # No value validation yet, so just make sure all the attrs are assignable
        record_attrs = dict([(attr, attr) for attr in ['action', 'method', 'timeout', 'finishOnKey', 'transcribe', 'transcribeCallback', 'playBeep', 'bothLegs', 'fileFormat']])
        self.response.append(telml.Record(**record_attrs))
        self.assertEqual(
            str(self.response), 
            '<Response><Record finishOnKey="finishOnKey" transcribe="transcribe" playBeep="playBeep" transcribeCallback="transcribeCallback" fileFormat="fileFormat" bothLegs="bothLegs" timeout="timeout" action="action" method="method"></Record></Response>'
        )


    # Dial
    def test_dial_simple(self):
        self.response.append(telml.Dial('1-555-222-3456'))
        self.assertEqual(str(self.response), '<Response><Dial>1-555-222-3456</Dial></Response>')

    def test_dial_number(self):
        self.response.append(telml.Dial(telml.Number('1-555-222-3456')))
        self.assertEqual(
            str(self.response), 
            '<Response><Dial><Number>1-555-222-3456</Number></Dial></Response>'
        )

    def test_dial_blank_number(self):
        with self.assertRaises(ValueError):
            self.response.append(telml.Dial(telml.Number()))
            str(self.response)

    def test_dial_attributes(self):
        # No value validation yet, so just make sure all the attrs are assignable
        dial_attrs = dict([(attr, attr) for attr in ['action', 'method', 'timeout', 'hangupOnStar', 'timeLimit', 'callerId', 'hideCallerId', 'callerName', 'dialMusic', 
        'callbackUrl', 'callbackMethod', 'confirmSound', 'digitsMatch', 'straightToVm', 'heartbeatUrl', 'heartbeatMethod', 'forwardedFrom']])
        self.response.append(telml.Dial("1-555-222-3456", **dial_attrs))
        self.assertEqual(
            str(self.response), 
            '<Response><Dial hideCallerId="hideCallerId" heartbeatMethod="heartbeatMethod" callerName="callerName" callerId="callerId" confirmSound="confirmSound" digitsMatch="digitsMatch" timeout="timeout" callbackMethod="callbackMethod" timeLimit="timeLimit" dialMusic="dialMusic" straightToVm="straightToVm" heartbeatUrl="heartbeatUrl" action="action" forwardedFrom="forwardedFrom" hangupOnStar="hangupOnStar" method="method" callbackUrl="callbackUrl">1-555-222-3456</Dial></Response>'
        )

    def test_dial_blank_conference(self):
        with self.assertRaises(ValueError):
            self.response.append(telml.Dial(telml.Conference()))
            str(self.response)

    def test_dial_conference(self):
        self.response.append(telml.Say('You are about to enter the conference'))
        self.response.append(telml.Dial(telml.Conference('Conference Room A')))
        self.assertEqual(
            str(self.response), 
            '<Response><Say>You are about to enter the conference</Say><Dial><Conference>Conference Room A</Conference></Dial></Response>'
        )

if __name__ == '__main__':
    unittest.main()
