# HAWK AMR reference implementation

HAWK is a concept for a modular autonomous mobile robot for warehouse automation. The SIH material describes an indoor ground robot with a docked drone for QR/RFID inventory work and a front forklift attachment for pallet transport. This repository is a small, runnable software reference for those workflows; it is not production robot firmware and does not drive motors, fly a drone, read physical RFID tags, or provide safety-rated navigation.

## What is included

- A dependency-free Python 3 reference simulator for task selection, inventory scans, and bounded pallet moves.
- Example tasks and simulated inventory in `data/`.
- Unit test cases in `tests/`.
- Architecture and safety boundaries in `docs/ARCHITECTURE.md`.
- An MIT license for the new software and documentation in this repository.


## Requirements

- Python 3.10 or newer
- No third-party packages for the simulator or tests

## Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/DHIRAJ-J-S/hawk-amr.git
cd hawk-amr
```

Create and activate a virtual environment (optional, but recommended):

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

Run the sample task file:

```bash
python -m hawk_amr.cli data/sample_tasks.json
```

Run the automated test cases:

```bash
python -m unittest discover -s tests -v
```

## Repository status

The implementation intentionally models a concept. Navigation, localization, obstacle avoidance, QR decoding, RFID hardware integration, actuator control, drone docking, communications, and emergency stops need real hardware drivers, validated algorithms, and physical safety review before deployment. See `docs/ARCHITECTURE.md` for the current boundary and extension points.

## Publishing

The public GitHub repository is [github.com/DHIRAJ-J-S/hawk-amr](https://github.com/DHIRAJ-J-S/hawk-amr). Before adding team contact details, CAD, or presentation media, confirm the contributors' consent and redistribution rights.

## Project source

This reference package was prepared from the HAWK SIH concepts: team 3 Degrees of Freedom, team ID HSC|TN|02487, and the HAWK modular AMR proposal. The SIH 2026 deck separately identifies problem statement SIH26112. Confirm which event/team metadata should be public before publishing.
