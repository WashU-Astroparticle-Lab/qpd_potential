"""Pytest bootstrap: put the src-layout package on sys.path.

This lets `import qpd_potential` and `pytest` work WITHOUT a permission-gated
editable install (`pip install -e .`). The src/ directory is prepended to
sys.path at collection time.
"""

import os
import sys

_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
