"""Step 4. Add up Feynman's diagrams for the electron's magnet, one order at a time."""
import math
from save import save

ALPHA = 1 / 137.035999049              # strength of one electron-photon meeting
MEASURED = 0.00115965218073            # (g - 2) / 2 of the electron, Harvard
PAPER = 0.00115965218178               # full prediction in Aoyama et al. 2012

# (order: how many times light is exchanged, number of diagrams, what they add up to)
ORDERS = [(1, 1, 0.5),
          (2, None, -0.328478965579193),
          (3, None, 1.181241456),
          (4, 891, -1.9106),
          (5, 12672, 9.16)]

x = ALPHA / math.pi
total, rows = 0.0, []
print('alpha / pi = %.10f' % x)
print('%-8s %-9s %-14s %-17s %s' % ('order', 'diagrams', 'they add to', 'running total', 'digits right'))
for n, count, coeff in ORDERS:
    total += coeff * x ** n
    miss = abs(total - MEASURED)
    digits = int(-math.log10(miss / (1 + MEASURED)))
    rows.append((n, count, coeff, total, digits))
    print('%-8d %-9s %-14.9g %.13f   %d' % (n, count or '-', coeff, total, digits))
print()
print('measured            %.14f' % MEASURED)
print('this sum            %.14f' % total)
print('paper, all effects  %.14f' % PAPER)
print('g / 2 measured      %.14f' % (1 + MEASURED))
print('g / 2 paper         %.14f' % (1 + PAPER))
print('they differ by 1 part in %.2e' % ((1 + MEASURED) / abs(PAPER - MEASURED)))
save(4, alpha_pi=x, rows=rows, measured=MEASURED, paper=PAPER, total=total,
     part=(1 + MEASURED) / abs(PAPER - MEASURED))
