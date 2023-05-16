from math import floor
scrsht_bounds =  (700, 450, 1100, 850)
scrsht_time = 0.3
item_mapping = {
    "normal": 0,
    "bomb": 1,
    "100t": 2,
    "donut": 3,
    "banana": 4,
    "peel": 4.5,
    "afro": 5,
    "meteor": 6,
    "minifaust": 7,
    "trumpet": 8,
    "hammer": 9,
    "banana|peel": 14
}

def get_item_index(item):
    return floor(item_mapping[item]) % 10

def delete_failed_captures():
    import os, shutil
    folder = 'failed_captures'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))