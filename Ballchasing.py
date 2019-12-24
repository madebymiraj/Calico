import argparse
import sys
import asyncio
import time
import platform
from Uploader import Uploader
from pprint import pprint
try:
    import ctypes.wintypes
except:
    pass


def main():
    args = parse_args()
    uploader = Uploader(args.folderpath, args.visibility)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uploader.asyncUpload())
    uploader.logResponses(uploader.asyncPayloads)  


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--folderpath', type=str, default=getUserDemoPath(), help='Path of the folder to upload')
    parser.add_argument('-v', '--visibility', type=str, default='public', choices=['public', 'private', 'unlisted'], help='Visibility of the replays')
    return parser.parse_args()

# Finds the path Rocket League uses to store the replay files on the system
# Default windows path: C:/Users/%USERNAME%/Documents/My Games/Rocket League/TAGame/Demos/
# Default macos path: '~/Library/Application Support/Rocket League/TAGame/Demos'
def getUserDemoPath():
    if platform.system() == 'Windows':
        CSIDL_PERSONAL= 5
        SHGFP_TYPE_CURRENT= 0
        buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
        dPath = str(buf.value) + '\\My Games\\Rocket League\\TAGame\\Demos\\'
        return dPath
    elif platform.system() == 'Darwin':
        dPath = '/Library/Application Support/Rocket League/TAGame/Demos/'
        return dPath


if __name__ == '__main__':
    main()