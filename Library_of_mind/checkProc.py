import os
import re


def checkProc(listWord):
    count = 0
    for dirname in os.listdir('/proc'):
        if count >= 2:
            break

        if dirname == 'curproc':
            continue

        try:
            with open('/proc/{}/cmdline'.format(dirname), mode='rb') as fd:
                content = fd.read().decode().split('\x00')
        except Exception:
            continue

        for i in listWord:
            regex = re.compile(i, re.IGNORECASE)
            if regex.match(' '.join(content)) is not None and 'self' not in dirname:
                # print('{0:<12} : {1}'.format(dirname, ' '.join(content)))
                count += 1
    return count
