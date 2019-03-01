import sys, os, unittest, json, time, math, uuid
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import deadsimplekv

def get_test_id():
    return str(uuid.uuid4()) + '.dat'

class TestInit(unittest.TestCase):
    def test_init(self):
        kv = deadsimplekv.DeadSimpleKV(get_test_id())
    
    def test_get(self):
        test_id = get_test_id()

        with open(test_id , 'w') as test_file:
            test_file.write('{"my_key": "test"}')
        
        # assert we can get written data
        kv = deadsimplekv.DeadSimpleKV(test_id)
        self.assertEqual(kv.get('my_key'), 'test')
    
    def test_delete(self):
        test_id = get_test_id()
        kv = deadsimplekv.DeadSimpleKV(get_test_id())
        kv.put('meme', 'doge')
        kv.delete('meme')
        self.assertIsNone(kv.get('meme'))

    def test_manual_flush(self):
        test_id = get_test_id()
        kv = deadsimplekv.DeadSimpleKV(test_id, flush_seconds=None)
        kv.put('meme', 'doge')
        kv2 = deadsimplekv.DeadSimpleKV(test_id)
        self.assertIsNone(kv2.get('meme'))

    def test_none(self):
        kv = deadsimplekv.DeadSimpleKV(get_test_id())
        # assert non existant value returns none
        self.assertIsNone(kv.get('my_key'))
    
    def test_invalid(self):
        kv = deadsimplekv.DeadSimpleKV(get_test_id())
        try:
            kv.put('rekt', b'bits')
        except ValueError:
            pass
        else:
            self.fail()
        try:
            kv.put(b'bits', 'ok')
        except ValueError:
            pass
        else:
            self.fail()
        
    def test_put(self):
        # Assert data gets written successfully as json
        test_id = get_test_id()

        kv = deadsimplekv.DeadSimpleKV(test_id)
        kv.put('my_key', 'test')

        with open(test_id, 'r') as test_file:
            test_data = json.loads(test_file.read())
        
        self.assertEqual(test_data['my_key'], 'test')
    
    def test_time(self):
        self.assertEqual(deadsimplekv.DeadSimpleKV._get_epoch(), math.floor(time.time()))

unittest.main()