# Feynman from scratch

Code for the video **Become Richard Feynman in 20 Minutes**.
Five of Richard Feynman's ideas, rebuilt as seven small programs: 357 lines of Python 3, standard library only, nothing to install.

```bash
python3 tests.py      # checks every step
./run_all.sh          # runs all seven, about 15 seconds; expected output is in demo-output.txt
```

| File | Idea | Year | What the run shows |
| --- | --- | --- | --- |
| `step1_action.py` | Least action | met in high school | A 150 g ball, 2 s in the air. The real path has action −4.800; five rival paths are all higher. Starting flat on the ground and only lowering the action, the program reaches the real throw in 766 steps (peak 4.904 m, formula 4.905 m). No force law is used. |
| `step2_arrows.py` | Every path gets an arrow | thesis 1942, paper 1948 | 401 paths, one arrow each. Laid end to end without turning: 401. Real sum: 34.8, of which 30.7 comes from the 101 paths nearest the real one. Half a turn of the arrow needs a bump of 4.2e-17 m for the ball and 0.012 mm for an electron in flight for a millionth of a second. |
| `step3_mirror.py` | Light reflects from the whole mirror | *QED*, 1985 | 400 strips, toy wavelength 10 cm. Middle quarter: 67.9. Left end, 100 strips: 4.5. Left end with every strip whose arrow points left scraped away, 48 strips: 29.1. With red light (650 nm, 20 million strips) the scraped pattern has 2,116 lines per millimetre: a diffraction grating. |
| `step4_diagrams.py` | Feynman diagrams | 1948 | The strength of the electron's magnet, added order by order: 5, 7, 10, 11, 11 digits right. Full prediction 1.00115965218178, measured 1.00115965218073. |
| `step5_limit.py` | What the arrows cost | 1982 | Arrows to keep for n two-state parts: 2ⁿ. 30 parts need 16 GB, 50 parts 16 PB, 300 parts a number with 91 digits. |
| `step6_trick.py` | Differentiating under the integral sign | from a book in high school | The area under (xᵏ − 1) / ln x from 0 to 1 equals ln(k + 1). Checked by brute force for k = 0, 1, 2, 3, 10. |
| `step7_oring.py` | The test: Challenger | 1986 | 23 flights before the accident. Only the 7 flights with damage: link between temperature and damage +0.02. All 23 flights: −0.51. One neuron trained by gradient descent gives a 0.94 chance of damage at 53 °F. |

`save.py` stores each step's numbers in `runs/stepN.json` (the video reads its on-screen numbers from there).

## Exercise (not run for the video)

The real path does not always have the *smallest* action. For a weight on a spring, followed for longer than half of one bounce, the real path is a saddle: lower in some directions, higher in others.

Try it in `step1_action.py`:

1. Line 15: replace the energy of height `M * G * height` with a spring's `0.5 * K * height ** 2`.
2. Line 46: replace `- M * G * DT` with `- K * y[i] * DT`.
3. Line 23: the real path is now `A * math.sin(math.sqrt(K / M) * t)`; keep its first and last value fixed in `descend`.
4. Choose `T` longer than `math.pi * math.sqrt(M / K)` (half a bounce).

Does a program that only walks downhill still find the real path?

## What is simplified

- **Step 1.** Time is cut into 20 pieces, so the action is a sum, not an integral. The printed actions are for that sum.
- **Step 2.** A toy world in one dimension: the only paths are the real one plus a single bump, and an arrow makes one turn per (bump / 25 cm)². The last table uses the real Planck constant to show how small that scale is for a ball and how large for an electron.
- **Step 3.** Two dimensions, a flat mirror cut into equal strips, one wavelength, and every strip sends an arrow of the same length. The left-right test for "which strips to scrape" is the simplest possible grating.
- **Step 4.** The coefficients of each order are copied from the published calculation (Aoyama, Hayakawa, Kinoshita, Nio, 2012). The program only multiplies and adds them. Nothing here evaluates a diagram.
- **Step 5.** Counts arrows and bytes (16 bytes per arrow). It simulates nothing.
- **Step 7.** One neuron (logistic regression) on 23 data points. At 31 °F it is asked about a temperature 22 degrees below all of its data, so the 0.9996 it prints is an extrapolation, not a measurement.

## Data and sources

- O-ring data: UCI "Challenger USA Space Shuttle O-Ring" data set (Draper, 1993); fitted coefficients agree with Dalal, Fowlkes and Hoadley (1989).
- Electron magnet: T. Aoyama, M. Hayakawa, T. Kinoshita, M. Nio, arXiv:1205.5368 (2012), which also quotes the Harvard measurement used here.

## Licence

MIT for the code.
