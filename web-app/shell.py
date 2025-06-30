# shell.py — Simulated attacker file
import sys

if __name__ == "__main__":
    print(f"Simulated shell received: {' '.join(sys.argv[1:])}")
