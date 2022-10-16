import os

cur_dir = os.path.join(os.path.join(os.getcwd(), "voices"), "GQ")


def get_ogg_body():
    for file in os.listdir(cur_dir):
        with open(cur_dir + '/' + file, mode='rb') as ogg_file:
            capture_pattern = ogg_file.read(32)
            version = ogg_file.read(8)
            header = ogg_file.read(8)
            capture_pattern.decode("utf-8")

            whole_file = ogg_file.readline()

if __name__ == '__main__':
    get_ogg_body()
