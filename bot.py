import datetime

time = '1644475704'
yesterday = str(int(time)+17*60*60)


first = datetime.datetime.utcfromtimestamp(int(time))
second = datetime.datetime.utcfromtimestamp(int(yesterday))
print(str(second))