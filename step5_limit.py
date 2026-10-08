"""Step 5. What the arrows cost. Each part can be up or down; every arrangement needs an arrow."""
from save import save

BYTES = 16                             # one arrow is two numbers of 8 bytes each
UNITS = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']


def memory(count):
    size, unit = count * BYTES, 0
    while size >= 1024 and unit < len(UNITS) - 1:
        size, unit = size / 1024, unit + 1
    return '%.0f %s' % (size, UNITS[unit])


rows = []
print('%-6s %-24s %s' % ('parts', 'arrows to keep', 'memory'))
for n in (1, 2, 3, 10, 30, 40, 50):
    rows.append((n, 2 ** n, memory(2 ** n)))
    print('%-6d %-24s %s' % rows[-1])
big = 2 ** 300
print()
print('300 parts: %.2e arrows, a number with %d digits' % (big, len(str(big))))
save(5, rows=rows, big=str(big), digits=len(str(big)))
