import datetime

time = '1644475704'
yesterday = str(int(time)-24*60*60)

print((datetime.datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')))
print((datetime.datetime.utcfromtimestamp(int(yesterday)).strftime('%Y-%m-%d %H:%M:%S')))