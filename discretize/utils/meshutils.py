from discretize.utils.mesh_utils import *  # NOQA F401,F403
import warnings

warnings.warn(
    "Importing from discretize.meshutils is deprecated behavoir. Please import "
    "from discretize.utils. This module will be removed in version 1.0.0 of discretize.",
    FutureWarning,
)
