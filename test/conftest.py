# Config inicial para testes
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
print("root-path-conftest", root)
sys.path.append(str(root))
