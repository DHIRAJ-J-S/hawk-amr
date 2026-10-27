# Event demo

Run this from the repository root with Python 3.10 or newer:

```bash
python -m hawk_amr.cli data/sample_tasks.json --show-map
```

The mission runs three jobs in order:

1. Scan inventory location `A-01-02` with the drone attachment.
2. Move a simulated 45 kg pallet from receiving to shipping with the forklift attachment.
3. Scan inventory location `B-03-01`.

The simulator reports each job as JSON with its result, route, and distance in grid cells. The final ASCII map shows obstacles (`#`), traveled cells (`*`), the start (`S`), and the finish (`E`). Each move begins where the previous move ended, so the route demonstrates state carried across a mission rather than three unrelated point-to-point examples.

## Suggested presentation

1. Point out the warehouse grid and shelf obstacles in `data/sample_tasks.json`.
2. Run the command and show how A* routes around blocked cells.
3. Compare the inventory records returned by the two scans.
4. Change the pallet load or a station coordinate and rerun to show input validation and replanning.

This demo uses a static map and fabricated data. It demonstrates software flow and grid path planning; it does not validate real-world autonomy or payload performance.
