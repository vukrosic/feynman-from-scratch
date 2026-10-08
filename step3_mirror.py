"""Step 3. Light reflects from every part of a mirror. Then we scrape parts of it away."""
import cmath
import math
from save import save

SRC, DET = (-0.5, 0.5), (0.5, 0.5)     # lamp and detector, metres; the mirror lies on y = 0
LEFT, RIGHT = -1.0, 1.0                # the mirror runs from -1 m to +1 m


def length(x):
    """Lamp -> point x on the mirror -> detector."""
    return math.dist(SRC, (x, 0.0)) + math.dist((x, 0.0), DET)


def arrows(wave, n):
    """One arrow per strip of mirror. It turns once for every wavelength of path."""
    xs = [LEFT + (RIGHT - LEFT) * (i + 0.5) / n for i in range(n)]
    return xs, [cmath.exp(2j * math.pi * length(x) / wave) for x in xs]


def band(wave, x):
    """Width of one kept band + one scraped band around x: the path changes by one wavelength."""
    lo, hi = 0.0, 0.5
    for _ in range(80):
        mid = (lo + hi) / 2
        if abs(length(x - mid / 2) - length(x + mid / 2)) < wave:
            lo = mid
        else:
            hi = mid
    return lo


def tilt(x):
    """sin(angle in) - sin(angle out) at point x of the mirror."""
    return abs((x - SRC[0]) / math.dist(SRC, (x, 0)) - (DET[0] - x) / math.dist((x, 0), DET))


def report(wave, n, name):
    xs, arr = arrows(wave, n)
    whole = abs(sum(arr))
    middle = abs(sum(z for x, z in zip(xs, arr) if abs(x) <= 0.25))
    end = [(x, z) for x, z in zip(xs, arr) if x <= -0.5]
    end_all = abs(sum(z for x, z in end))
    # scrape away every strip of the end whose arrow points to the left half
    kept = [(x, z) for x, z in end if z.real > 0]
    end_cut = abs(sum(z for x, z in kept))
    spacing, slope = band(wave, -0.75), tilt(-0.75)
    print(name)
    print('  strips: %d   arrows end to end: %d' % (n, n))
    print('  whole mirror:                  %9.1f' % whole)
    print('  middle quarter (|x| <= 25 cm): %9.1f' % middle)
    print('  left end (x <= -50 cm):        %9.1f   from %d strips' % (end_all, len(end)))
    print('  left end, half scraped away:   %9.1f   from %d strips' % (end_cut, len(kept)))
    print('  one band + one gap at x = -75 cm: %.4g m   grating formula: %.4g m' % (spacing, wave / slope))
    return dict(n=n, whole=whole, middle=middle, end_all=end_all, end_cut=end_cut, n_end=len(end),
                n_kept=len(kept), spacing=spacing, formula=wave / slope,
                turns=[length(x) / wave for x in xs[::max(1, n // 400)]])


print('shortest path: x = 0, %.4f m.   path by the left edge: %.4f m' % (length(0.0), length(LEFT)))
toy = report(0.10, 400, 'toy light, wavelength 10 cm')
red = report(650e-9, 20_000_000, 'red light, wavelength 650 nm')
print('  lines per millimetre: %.0f' % (0.001 / red['spacing']))
red.pop('turns')
save(3, toy=toy, red=red, shortest=length(0.0), edge=length(LEFT), lines_mm=0.001 / red['spacing'])
