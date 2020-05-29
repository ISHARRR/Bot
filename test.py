import os
window_len = os.popen('stty size', 'r').read().split()
print(' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
