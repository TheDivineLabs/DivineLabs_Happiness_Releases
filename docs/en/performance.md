[Русский](../performance.md) · English

# Performance and measurements

Recorded main EXE sizes for version 0.2.8:

| | Client | Plus |
| --- | --- | --- |
| Main EXE | 4.16 MiB | 15.80 MiB |

The editions contain different modules. File size is not a measure of FPS, CPU usage or RAM usage. Browser components add to the total download and installation size.

The app can record technical measurements for 60 seconds. Recording is disabled by default. Reports are saved locally under `Data/Diagnostics/Performance` and are not uploaded automatically.

Reports include CPU usage, memory and available Flash frame intervals. Game logic events are not equivalent to displayed frames; they are not reported as visible FPS.

Comparable browser benchmarks and graphics optimization results have not been published. Comparisons need the same scene, window size and cache state, a warm-up period and repeated runs.
