"""Step 7. The 23 flights before Challenger. What did the O-rings say about the cold?"""
import math
from save import save

# (temperature of the joint at launch in Fahrenheit, O-rings with damage), 23 flights
FLIGHTS = [(53, 2), (57, 1), (58, 1), (63, 1), (66, 0), (67, 0), (67, 0), (67, 0),
           (68, 0), (69, 0), (70, 0), (70, 0), (70, 1), (70, 1), (72, 0), (73, 0),
           (75, 0), (75, 2), (76, 0), (76, 0), (78, 0), (79, 0), (81, 0)]
LAUNCH = 31                            # forecast for the morning of 28 January 1986

hurt = [(t, k) for t, k in FLIGHTS if k > 0]
print('flights: %d   with damage: %d   coldest so far: %d F' % (len(FLIGHTS), len(hurt), FLIGHTS[0][0]))


def corr(pairs):
    n = len(pairs)
    mx, my = sum(x for x, y in pairs) / n, sum(y for x, y in pairs) / n
    sxy = sum((x - mx) * (y - my) for x, y in pairs)
    return sxy / math.sqrt(sum((x - mx) ** 2 for x, y in pairs) * sum((y - my) ** 2 for x, y in pairs))


print()
print('only the %d flights with damage:' % len(hurt))
print('  temperatures', [t for t, k in hurt])
print('  link between temperature and damage: %+.2f' % corr(hurt))
print('all %d flights:' % len(FLIGHTS))
cold = [k > 0 for t, k in FLIGHTS if t < 65]
warm = [k > 0 for t, k in FLIGHTS if t >= 65]
print('  below 65 F: %d of %d damaged      65 F and above: %d of %d damaged'
      % (sum(cold), len(cold), sum(warm), len(warm)))
print('  link between temperature and damage: %+.2f' % corr(FLIGHTS))

# one neuron: chance of damage = squash(w * temperature + b), fitted by gradient descent
mean = sum(t for t, k in FLIGHTS) / len(FLIGHTS)
spread = math.sqrt(sum((t - mean) ** 2 for t, k in FLIGHTS) / len(FLIGHTS))


def squash(z):
    return 1 / (1 + math.exp(-z))


def chance(t, w, b):
    return squash(w * (t - mean) / spread + b)


w, b, shots = 0.0, 0.0, {}
for step in range(20001):
    if step in (0, 5, 20, 100, 1000, 20000):
        shots[step] = (w, b)
    gw = gb = 0.0
    for t, k in FLIGHTS:
        miss = chance(t, w, b) - (1 if k else 0)
        gw += miss * (t - mean) / spread
        gb += miss
    w -= 0.5 * gw / len(FLIGHTS)
    b -= 0.5 * gb / len(FLIGHTS)

slope = w / spread
print()
print('one neuron after 20000 steps: chance = squash(%.4f * F + %.2f)' % (slope, b - slope * mean))
table = []
for t in (81, 70, 65, 53, LAUNCH):
    table.append((t, chance(t, w, b)))
    print('  %2d F   chance of damage on a flight: %.4f' % (t, chance(t, w, b)))
print()
print('management said: 1 failure in 100000 flights = %.5f' % (1 / 100000))
print('  one launch a day, one failure in %d years' % round(100000 / 365.25))
print('engineers said:  about 1 in 100            = %.5f' % (1 / 100))
save(7, flights=FLIGHTS, n_hurt=len(hurt), corr_hurt=corr(hurt), corr_all=corr(FLIGHTS),
     cold=(sum(cold), len(cold)), warm=(sum(warm), len(warm)), slope=slope, bias=b - slope * mean,
     table=table, years=round(100000 / 365.25), mean=mean, spread=spread,
     shots={str(s): [chance(t, *wb) for t in range(25, 86)] for s, wb in shots.items()})
