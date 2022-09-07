from email import message
import sys
import json
import struct


def encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent).encode('utf-8')
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}


def sendMessage(encodeMessage):
    sys.stdout.buffer.write(encodeMessage['length'])
    sys.stdout.buffer.write(encodeMessage['content'])
    sys.stdout.buffer.flush()


while True:
    temp = input('Press n for next post, p for previous and q to quit ')
    if temp == 'q':
        break
    elif temp == 'n' or temp == 'p':
        message = encodeMessage(temp)
        sendMessage(message)
    else:
        print('Enter p, q or n')
