
import random
import uuid, time


letters = "abcdefghijklmnopqrstuvwxyz0123456789"

def random_str(n: int):
    return ''.join(random.choice(letters) for i in range(n))

def get_nonce():
    new_uuid = uuid.uuid4()
    return new_uuid.hex

def current_milli_time():
    return round(time.time() * 1000)
