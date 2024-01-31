from uuid import uuid4
import time 
rand_id = uuid4()

print(rand_id.int%10000000)

print(int(time.time()))