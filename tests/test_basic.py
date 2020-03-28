'''
    DeadSimpleKv. An extremely simple key-value storage system with cache
    Copyright (C) 2019 Kevin Froman

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
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

    def test_get_raw_json(self):
        test_id = get_test_id()

        with open(test_id , 'w') as test_file:
            test_file.write('{"my_key": "test"}')

        # assert we can get written data
        kv = deadsimplekv.DeadSimpleKV(test_id)
        self.assertEqual(kv.get_raw_json(), '{"my_key": "test"}')

    def test_delete(self):
        # test key deletion
        test_id = get_test_id()
        kv = deadsimplekv.DeadSimpleKV(get_test_id())
        kv.put('meme', 'doge')
        kv.delete('meme')
        self.assertIsNone(kv.get('meme'))

    def test_manual_flush(self):
        # test manual flushing
        test_id = get_test_id()
        kv = deadsimplekv.DeadSimpleKV(test_id, flush_seconds=None)
        kv.put('meme', 'doge')
        kv2 = deadsimplekv.DeadSimpleKV(test_id)
        self.assertIsNone(kv2.get('meme'))

    def test_manual_refresh(self):
        # Test manual refreshing
        test_id = get_test_id()
        kv = deadsimplekv.DeadSimpleKV(test_id, refresh_seconds=None)
        kv2 = deadsimplekv.DeadSimpleKV(test_id)

        kv2.put('test', True)
        self.assertIsNone(kv.get('test'))
        kv.refresh()
        self.assertTrue(kv.get('test'))

    def test_none(self):
        kv = deadsimplekv.DeadSimpleKV(get_test_id())
        # assert non existant value returns none
        self.assertIsNone(kv.get('my_key'))

    def test_invalid(self):
        kv = deadsimplekv.DeadSimpleKV(get_test_id(), flush_on_exit=False)
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

    def test_flush_no_path(self):
        # assert data gets flushed when the path is not made yet

        test_id = "my_test_dir/my_second_dir/" + get_test_id()

        kv = deadsimplekv.DeadSimpleKV(test_id)
        kv.put('my_key', 'test2')

        with open(test_id, 'r') as test_file:
            test_data = json.loads(test_file.read())

        self.assertEqual(test_data['my_key'], 'test2')

    def test_time(self):
        self.assertEqual(deadsimplekv.DeadSimpleKV._get_epoch(), math.floor(time.time()))

unittest.main()