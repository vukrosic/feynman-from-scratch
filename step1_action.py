"""Step 1. Least action: the path a thrown ball takes, found without using forces."""
import math
from save import save

M, G, T, N = 0.15, 9.81, 2.0, 20       # kg, m/s^2, seconds in the air, pieces of time
DT = T / N


def action(y):
    """Add up (energy of motion - energy of height) * time over the whole path."""
    total = 0.0
    for i in range(N):
        speed = (y[i + 1] - y[i]) / DT
        height = (y[i] + y[i + 1]) / 2
        total += (0.5 * M * speed ** 2 - M * G * height) * DT
    return total


def times():
    return [i * DT for i in range(N + 1)]


real = [0.5 * G * t * (T - t) for t in times()]
rivals = {
    'the real path': real,
    'stay on the ground': [0.0 for t in times()],
    'half as high': [0.5 * y for y in real],
    'twice as high': [2.0 * y for y in real],
    'straight up, straight down': [max(real) * (1 - abs(2 * t / T - 1)) for t in times()],
    'real path with a wobble': [y + 0.5 * math.sin(3 * math.pi * t / T) for y, t in zip(real, times())],
}
print('ball %.2f kg, in the air %.0f s, real path peaks at %.3f m' % (M, T, max(real)))
print('%-28s %10s' % ('path', 'action'))
for name, y in rivals.items():
    print('%-28s %10.3f' % (name, round(action(y), 3) + 0.0))


def descend(y, rate=0.3, tol=0.001):
    """Move every point of the path a little in the direction that lowers the action."""
    steps, shots = 0, {}
    while True:
        if steps in (0, 10, 50, 150, 400, 1000):
            shots[steps] = [round(v, 4) for v in y]
        grad = [0.0] * (N + 1)
        for i in range(1, N):
            grad[i] = M * (2 * y[i] - y[i - 1] - y[i + 1]) / DT - M * G * DT
        y = [v - rate * g for v, g in zip(y, grad)]
        steps += 1
        if max(abs(a - b) for a, b in zip(y, real)) < tol:
            return y, steps, shots


found, steps, shots = descend([0.0] * (N + 1))
print()
print('start flat on the ground, lower the action step by step')
print('steps until every point is within 1 mm of the real path: %d' % steps)
print('peak found %.3f m, formula g*T*T/8 = %.3f m' % (max(found), G * T * T / 8))
print('action found %.3f, real %.3f' % (action(found), action(real)))
save(1, m=M, g=G, T=T, N=N, peak=max(real), actions={k: action(v) for k, v in rivals.items()},
     paths={k: [round(x, 4) for x in v] for k, v in rivals.items()},
     steps=steps, shots=shots, found_peak=max(found), found_action=action(found))
