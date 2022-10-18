import subprocess
import os

PACK_NAME = "GQ"
# PACK_NAME = "кремниевая долина"

cur_dir = os.path.join(os.path.join(os.getcwd(), "voices"), PACK_NAME)

for file in os.listdir(cur_dir):
    new_fn = os.path.join(cur_dir, os.path.basename(file) + "2.ogg")
    subprocess.run(["ffmpeg", '-i', os.path.join(cur_dir, file), '-acodec', 'libopus',  new_fn, '-y'])
