"""Checks. run_all.sh runs them last, on the numbers the seven steps saved in runs/."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
r = {i: json.load(open(os.path.join(HERE, 'runs', 'step%d.json' % i))) for i in range(1, 8)}

# 1. no rival path has less action than the real one, and descent lands on the real one
real = r[1]['actions']['the real path']
assert all(a >= real for a in r[1]['actions'].values())
assert abs(r[1]['found_peak'] - r[1]['g'] * r[1]['T'] ** 2 / 8) < 0.002
assert abs(r[1]['found_action'] - real) < 1e-5

# 2. the formula for the extra action matches a direct sum; far paths nearly cancel
assert abs(r[2]['direct'] - r[2]['formula']) < 1e-6
assert r[2]['outer'] < r[2]['middle'] / 4 and r[2]['total'] < r[2]['n'] / 10

# 3. the measured band width matches the grating formula; scraping makes the end brighter
for light in ('toy', 'red'):
    assert abs(r[3][light]['spacing'] / r[3][light]['formula'] - 1) < 0.01
    assert r[3][light]['end_cut'] > 5 * r[3][light]['end_all']
assert abs(r[3]['shortest'] - math.sqrt(2)) < 1e-12

# 4. first term is Schwinger's alpha / 2 pi; the sum is within 1 part in 100 billion of g / 2
assert abs(r[4]['rows'][0][3] - r[4]['alpha_pi'] / 2) < 1e-15
assert abs(r[4]['total'] - r[4]['measured']) < 1e-11

# 5. every added part doubles the number of arrows
assert all(count == 2 ** n for n, count, mem in r[5]['rows']) and r[5]['digits'] == 91

# 6. brute force agrees with ln(a + 1), and the slope with 1 / (a + 1)
assert all(abs(brute - exact) < 1e-6 for a, brute, exact in r[6]['rows'])
assert all(abs(slope - exact) < 1e-6 for a, slope, easy, exact in r[6]['slopes'])

# 7. the neuron lands on the published fit (Dalal, Fowlkes and Hoadley 1989: 15.04, -0.2322)
assert abs(r[7]['slope'] + 0.2322) < 0.0005 and abs(r[7]['bias'] - 15.04) < 0.01
assert r[7]['n_hurt'] == 7 and len(r[7]['flights']) == 23
print('all checks pass')
