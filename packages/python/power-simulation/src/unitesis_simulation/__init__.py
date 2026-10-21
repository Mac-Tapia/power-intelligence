"""Power-flow engines and independent comparison. Engines declare scope; none fakes results."""

from .comparison import compare_results, expected_coverage
from .pandapower_engine import PandapowerEngine
from .radial_bfs import RadialBFSEngine

__all__ = ["PandapowerEngine", "RadialBFSEngine", "compare_results", "expected_coverage"]
