# Medieval Battle Planner

Project solves the problem of optimally matching your platoons against an opponent's, using a battle assignment algorithm to win the majority of 5 battles.

---

## Table of Contents

- [Overview](#overview)    
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Testing](#testing)  
- [Project Structure](#project-structure) 

---

## Overview

Given 5 platoons for both your army and the enemy, this program:

1. Parses inputs like `Spearmen#10;Militia#30;…`
2. Builds a score matrix (`+1` = win, `0` = draw, `-1` = loss)
3. Uses SciPy’s Hungarian algorithm (`linear_sum_assignment`) to find the optimal assignment
4. Outputs your platoons in the order that correspond to the opponent's lineup, if ≥ 3 battles can be won

---

## Prerequisites

- Python 3.13.3  
- SciPy = 1.16.0   
- NumPy = 2.3.1 

---

## Installation

Run these commands in your terminal:

```bash
git clone https://github.com/varunpanchal752/Casa.git
cd medieval-battle-planner

python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# macOS/Linux:
pip install -r requirements.txt
# Windows:
pip install -r .\requirements.txt
```

---

## Usage

Run these commands in your terminal:

```bash
#Linux
python3 ./medieval_battle/main.py < ./medieval_battle/input.txt
#Windows
Get-Content .\medieval_battle\input.txt | python .\medieval_battle\main.py
```

---

## Testing

Run these commands in your terminal:

```bash
#Linux
python ./medieval_battle./test_battle.py
#Windows
python .\medieval_battle\test_battle.py
```

---

## Project-structure

Run these commands in your terminal:

```bash
 root/
 ┣ projects/
 ┃ ┣ battle_assign.py       # Core logic & Hungarian algorithm
 ┃ ┣ main.py                # IO entrypoint
 ┃ ┗ test_battle_assign.py  # Unit tests
 ┗ README.md
```