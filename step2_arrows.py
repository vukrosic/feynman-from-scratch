"""Step 2. Every path gets an arrow. Add the arrows and see which paths are left."""
import cmath
import math
from save import save

H = 6.62607015e-34                     # Planck's constant, joule seconds
G, T = 9.81, 2.0


def extra_action(m, a, T):
    """Action of (real path + a bump of height a) minus the action of the real path."""
    return m * math.pi ** 2 * a ** 2 / (4 * T)


def arrow(turns):
    """An arrow of length 1 that has turned this many times."""
    return cmath.exp(2j * math.pi * turns)


# A toy world where one turn of the arrow costs much more action, so we can look at it.
A0 = 0.25                               # a bump of 25 cm turns the arrow once
bumps = [-1 + 2 * i / 400 for i in range(401)]            # 401 paths, bump from -1 m to +1 m
arrows = [arrow((a / A0) ** 2) for a in bumps]
total = sum(arrows)
middle = sum(z for z, a in zip(arrows, bumps) if abs(a) <= A0)
outer = total - middle
print('toy world: 401 paths, bumps from -1 m to +1 m, one turn per (bump / 25 cm) squared')
print('arrows laid end to end without turning: %d' % len(arrows))
print('length of the real sum:               %.1f' % abs(total))
print('  from the %d paths within 25 cm:     %.1f' % (sum(abs(a) <= A0 for a in bumps), abs(middle)))
print('  from the %d paths outside:          %.1f' % (sum(abs(a) > A0 for a in bumps), abs(outer)))


def check_bump():
    """The formula for the extra action, checked against a direct sum over a path."""
    m, a, n = 0.15, 0.3, 20000
    dt = T / n

    def act(bump):
        s, prev = 0.0, 0.0
        for i in range(1, n + 1):
            t = i * dt
            y = 0.5 * G * t * (T - t) + bump * math.sin(math.pi * t / T)
            s += (0.5 * m * ((y - prev) / dt) ** 2 - m * G * (y + prev) / 2) * dt
            prev = y
        return s
    return act(a) - act(0.0), extra_action(m, a, T)


direct, formula = check_bump()
print()
print('extra action of a 30 cm bump: summed %.6f, formula %.6f' % (direct, formula))


def half_turn(m, T):
    """The bump that turns the arrow half a turn: extra action = H / 2."""
    return math.sqrt(2 * T * H / (m * math.pi ** 2))


print()
print('the real world: how big a bump before the arrow has turned half a turn')
things = [('ball, 150 g, 2 s', 0.15, 2.0), ('grain of sand, 1 mg, 2 s', 1e-6, 2.0),
          ('electron, 2 s', 9.1093837139e-31, 2.0), ('electron, 1 millionth of a second', 9.1093837139e-31, 1e-6)]
rows = []
for name, m, t in things:
    rows.append((name, half_turn(m, t)))
    print('%-36s %.2e m' % (name, half_turn(m, t)))
save(2, a0=A0, n=len(arrows), total=abs(total), middle=abs(middle), outer=abs(outer),
     n_mid=sum(abs(a) <= A0 for a in bumps), turns=[(a / A0) ** 2 for a in bumps],
     direct=direct, formula=formula, half=rows)
