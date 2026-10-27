# HAWK AMR

HAWK is a modular autonomous mobile robot concept for warehouse work. The proposed platform combines an indoor mobile robot, a docked drone for QR and RFID inventory scanning, and a front forklift attachment for moving pallets. The same drone platform is also intended for disaster-response missions.

This repository contains a small Python simulator for the HAWK task workflows. It plans routes through a sample warehouse, processes inventory scans, and checks pallet-move requests from a JSON file. It is a software prototype: it does not connect to robot hardware or control a drone, motors, or forklift.

## Getting started

**Requirements:** Python 3.10 or newer. The project uses only the Python standard library.

Clone the repository and run the sample tasks:

```bash
git clone https://github.com/DHIRAJ-J-S/hawk-amr.git
cd hawk-amr
python -m hawk_amr.cli data/sample_tasks.json --show-map
```

The sample mission scans two locations and moves a 45 kg pallet between receiving and shipping. It uses three fabricated inventory records. The output includes each planned route and a map of the warehouse.

To run the test suite:

```bash
python -m unittest discover -s tests -v
```

## Project layout

- `hawk_amr/` — task models, A* route planner, simulator, and command-line interface
- `data/` — sample tasks and inventory
- `tests/` — unit tests for route planning, scans, attachment selection, and pallet-load validation
- `docs/ARCHITECTURE.md` — component overview, task flow, and future integration points
- `docs/DEMO.md` — event demo walkthrough

## Current scope

The route planner uses A* on a four-direction grid with static obstacles. The simulator checks attachment selection, returns sample inventory at a requested location, and rejects pallet loads above the configured example limit. It does not implement ROS 2, live perception, physical QR/RFID readers, drone docking, or actuator control. The example load limit is not a hardware rating.

## License

The code and documentation are provided under the [MIT License](LICENSE).
