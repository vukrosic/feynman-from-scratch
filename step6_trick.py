"""Step 6. Feynman's trick: turn a hard integral into an easy one by adding a dial."""
import math
from save import save


def f(x, k):
    return (x ** k - 1) / math.log(x)


def integral(g, n=200000):
    """Area under g from 0 to 1: n thin slices, measured at the middle of each."""
    return sum(g((i + 0.5) / n) for i in range(n)) / n


print('I(k) = area under (x^k - 1) / ln x, from 0 to 1')
rows = []
for k in (0, 1, 2, 3, 10):
    brute = integral(lambda x: f(x, k))
    rows.append((k, brute, math.log(k + 1)))
    print('k = %-3d by brute force %.6f     ln(k + 1) = %.6f' % (k, brute, math.log(k + 1)))

print()
print('turn the dial k a little: how fast does the area grow?')
slopes = []
for k in (1, 2, 3):
    h = 0.001
    grow = (integral(lambda x: f(x, k + h)) - integral(lambda x: f(x, k - h))) / (2 * h)
    easy = integral(lambda x: x ** k)
    slopes.append((k, grow, easy, 1 / (k + 1)))
    print('k = %d   growth %.6f   area under x^k %.6f   1 / (k + 1) = %.6f' % (k, grow, easy, 1 / (k + 1)))
save(6, rows=rows, slopes=slopes,
     curves={str(k): [f((i + 0.5) / 80, k) for i in range(80)] for k in (0.5, 1, 2, 3)})
