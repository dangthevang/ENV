import importlib.util
import os
import random as rd
import sys

import numpy as np
from numba import jit, njit
from numba.typed import List

from setup import SHORT_PATH

game_name = sys.argv[1]


def setup_game(game_name):
    spec = importlib.util.spec_from_file_location(
        "env", f"{SHORT_PATH}Base/{game_name}/env.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


env = setup_game(game_name)

getActionSize = env.getActionSize
getStateSize = env.getStateSize
getAgentSize = env.getAgentSize

getValidActions = env.getValidActions
getReward = env.getReward


def DataAgent():
    return np.array([])


@njit()
def Test(state, per):
    validActions = getValidActions(state)
    validActions[79] = 0
    validActions = np.where(validActions == 1)[0]

    if 61 in validActions:
        return 61, per

    if 78 in validActions:
        return 78, per

    if 81 in validActions:
        return 81, per

    if 77 in validActions:
        return 77, per

    if 80 in validActions:
        return 80, per

    if 44 in validActions:
        return 44, per

    action = validActions[np.random.randint(len(validActions))]
    return action, per
