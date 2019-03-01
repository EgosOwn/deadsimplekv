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
import json, time, math, os

def is_serializable(data):
    try:
        json.dumps(data)
        return True
    except TypeError:
        return False

class DeadSimpleKV:
    def __init__(self, file_path=None, refresh_seconds=0, flush_seconds=0):
        '''
            Accepts a file path and refresh.
            If file_path is not set, no data will be written to disk.
            Refresh is an integer specifying how many seconds should pass before data is re-read from disk.
            If refresh_seconds or flush_seconds are set to None they will not be done automatically
        '''
        temp_time = DeadSimpleKV._get_epoch() # Initialization time
        self.file_path = file_path # The file path where we write our data in JSON format
        self.refresh_seconds = refresh_seconds # How often to refresh the
        self.flush_seconds = flush_seconds # How often to flush out when setting
        self._data = {} # The key store (in memory)
        self._last_refresh = temp_time # time last refreshed from disk
        self._last_flush = temp_time # time last flushed to disk

        if os.path.exists(file_path):
            self.refresh()
    
    def get(self, key):
        if self.refresh_seconds is not None and self.file_path is not None:
            self.refresh()
        try:
            return self._data[key]
        except KeyError:
            return None
        
    def put(self, key, value):
        '''Value setter. Will automatically flush if auto_flush is True and file_path is not None'''
        self._data[key] = value # Set the key

        # Check if key and value can be put in JSON
        if not is_serializable(key):
            raise ValueError('%s is not JSON serializable' % (key,))
        if not is_serializable(value):
            raise ValueError('%s is not JSON serializable' % (value,))    
        self._do_auto_flush()
        return (key, value)
    
    def delete(self, key):
        del self._data[key]
        self._do_auto_flush()

    def refresh(self):
        '''Refresh data and then mark time read'''
        try:
            self._data = json.loads(DeadSimpleKV._read_in(self.file_path))
        except FileNotFoundError:
            pass
        self._last_refresh = DeadSimpleKV._get_epoch()

    def flush(self):
        '''Write out then mark time flushed'''
        DeadSimpleKV._write_out(self.file_path, json.dumps(self._data))
        self._last_flush = DeadSimpleKV._get_epoch()
    
    def _do_auto_flush(self):
        if self.flush_seconds is not None and self.file_path is not None:
            # flush if automatic and it is time to do so
            temp_time = DeadSimpleKV._get_epoch()
            if temp_time - self._last_flush >= self.flush_seconds:
                self.flush()

    @staticmethod
    def _get_epoch():
        return math.floor(time.time())

    @staticmethod
    def _write_out(file_path, data):
        '''Write out the raw data'''
        with open(file_path, 'w') as write_file:
            write_file.write(data)

    @staticmethod
    def _read_in(file_path):
        '''Read in raw data'''
        with open(file_path, 'r') as read_file:
            return read_file.read()