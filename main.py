"""Calculate critical-path latency for a DAG of voice-pipeline stages."""
import argparse
import json
import math
from pathlib import Path

