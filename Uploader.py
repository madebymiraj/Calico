import os
import time
import json
import hashlib
import asyncio
import aiohttp
import platform
import datetime
import subprocess
from tqdm import tqdm
from pprint import pprint
try:
    import ctypes.wintypes
except:
    pass


class Uploader:

    def __init__(self, demo_path, visibility):
        self.demo_path = demo_path
        self.visibility = visibility
        self.sync_payloads = {}
        self.async_payloads = []
        self.get_upload_parameters()
        self.file_list = self.get_file_list()
        self.replay_list = self.filter_file_list(self.file_list)
        self.hashes_list = self.get_used_hashes()
        self.replay_hashes = {}
        self.open_all()
        self.replay_count = len(self.opened_replays)

    def get_upload_parameters(self):
        cwd = os.path.dirname(__file__)
        self.upload_url = 'https://ballchasing.com/api/v2/upload?visibility=' + self.visibility
        self.auth_file_path = cwd + '/Resources/auth'
        self.auth_id = self.get_auth_id()
        self.auth_parameter = {'Authorization': self.auth_id}
        self.temp_response_path = cwd + '/Resources/Logs/tempResponse'
        self.response_log_path = cwd + '/Resources/Logs/Responses'
        self.hashes_log_path = cwd + '/Resources/Logs/hashes.txt'

    def get_auth_id(self):
        with open(self.auth_file_path, 'r') as file:
            auth_id = file.read()
        return auth_id

    def get_file_list(self, demo_path=None):
        if demo_path is None:
            demo_path = self.demo_path
        return [(x[0], time.ctime(x[1].st_ctime), os.path.getsize(x[0])) for x in sorted([((demo_path + fn), os.stat((demo_path + fn))) for fn in os.listdir(demo_path)], key = lambda x: x[1].st_ctime)]

    def filter_file_list(self, file_list):
        filtered_list = []
        for replay in file_list:
            if replay[2] > 5000 and ('.replay' in replay[0]):
                filtered_list.append(replay)
        return filtered_list

    def get_used_hashes(self):
        with open(self.hashes_log_path, 'r') as file:
            data = file.readlines()
        return [line.strip() for line in data]

    def open_all(self):
        self.opened_replays = []
        for replay in self.replay_list:
            replay_hash = self.get_hash(replay[0])
            if replay_hash not in self.hashes_list:
                self.opened_replays.append({'data': {'file': open(replay[0], 'rb')}, 'Name':os.path.basename(replay[0]), 'Hash': replay_hash})
                self.replay_hashes[os.path.basename(replay[0])] = replay_hash

    def get_temp_response(self):
        if os.path.exists(self.temp_response_path):
            return self.read_json()
        return None

    def read_json(self):
        with open(self.temp_response_path, 'r') as file:
            response = json.load(file)
        return response

    def write_json(self, data):
        logPath = self.response_log_path + str(datetime.datetime.now().strftime(" %Y-%m-%d %H-%M-%S"))
        with open(logPath, 'w') as file:
            json.dump(data, file, indent=4)

    def update_hashes(self, hashes):
        with open(self.hashes_log_path, 'a') as file:
            for replay_hash in hashes:
                file.write('\n' + replay_hash)

    def write_hash(self, replay_hash):
        with open(self.hashes_log_path, 'a') as file:
            file.write('\n' + replay_hash)                        

    def log_responses(self, data=None):
        if data is None:
            data = self.async_payloads
        self.write_json(data)
        self.update_hashes(list(self.replay_hashes.values()))

    def upload_sync(self):
        self.response_list['UploadInformation'] = {'Path':self.demo_path, 'Visibility':self.visibility, 'ReplayCount':self.replay_count}
        for replay in tqdm(self.replay_list, total=self.replay_count):
            subprocess.call(['curl', '-s', '-o', self.temp_response_path, '-F', 'file=@' + replay[0],'-H', 'Authorization:' + self.auth_id, self.upload_url], shell=False)
            temp_response = self.get_temp_response()
            self.response_list[replay[0]] = temp_response
        self.log_responses()

    def get_hash(self, file_name):
        hasher = hashlib.md5()
        with open(file_name, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
        return hasher.hexdigest()

    async def upload_async(self):
        async with aiohttp.ClientSession() as self.session:
            responses = [await future for future in tqdm(asyncio.as_completed(map(self.post_async, self.opened_replays)), total=self.replay_count)]

    async def post_async(self, replay):
        async with self.session.post(self.upload_url, headers=self.auth_parameter, data=replay['data']) as response:
            self.async_payloads.append([replay['Name'], await response.json()])
            self.write_hash(replay['Hash'])


