import sys
import re
from battle import Platoon, UnitClass, BattlePlanner

# Regular expression to validate tokens like "Spearmen#10"
# - Matches exactly one of the six valid classes (UnitClass enum values)
# - Followed by '#' and one or more digits (soldier count)
TOKEN_RE = re.compile(r'^(' + '|'.join(c.value for c in UnitClass) + r')#(\d+)$')

def parse_line(line: str, side: str):
    """
    Parse and validate a line of input containing 5 platoon tokens.
    Else raises ValueError.
    """
    tokens = [t.strip() for t in line.strip().split(';')]
    if len(tokens) != 5:
        raise ValueError(f"{side}: expected 5 platoons, got {len(tokens)}")
    
    platoons = []
    seen = set()
    for tok in tokens:
        m = TOKEN_RE.match(tok)
        if not m:
            raise ValueError(f"{side}: invalid token format `{tok}` (must be Class#Number)")
        cls_name, num = m.group(1), int(m.group(2))
        if num <= 0:
            raise ValueError(f"{side}: soldier count must be > 0 (`{tok}`)")
        if tok in seen:
            raise ValueError(f"{side}: duplicate platoon `{tok}`")
        seen.add(tok)
        platoons.append(Platoon.from_str(tok))
    return platoons

def format_line(platoon_list):
    """Format the final battle order as a semicolon-separated string."""
    return ';'.join(str(p) for p in platoon_list)

def main():
    try:
        ours = parse_line(sys.stdin.readline(), "First line")
        theirs = parse_line(sys.stdin.readline(), "Second line")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    planner = BattlePlanner(ours, theirs)
    result = planner.find_optimal_order()
    if result is None:
        print("There is no chance of winning")
    else:
        print(format_line(result))

if __name__ == "__main__":
    main()
