#  không gian n chiều
#  small NN deep
import numpy as np
from numba import njit
import sys
from setup import SHORT_PATH
import importlib.util

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


from numba.typed import List

# Agent function
def DataAgent():
    per = List(
        [
            np.random.rand(getActionSize(), getStateSize()),  # [0]
            np.zeros((getActionSize(), getStateSize())),  # [1]
            np.zeros((1, 1)),  # [2]
            np.random.rand(getActionSize(), getStateSize()) * 10,  # [3]
            np.zeros((getActionSize(), getStateSize())),  # [4]
        ]
    )
    return per


@njit()
def findOut(state, geo):
    return np.sum((geo * state) ** 2, axis=1)


@njit()
def Train(state, per):
    actions = getValidActions(state)
    #  nState = state - 1
    nState = state - per[3]
    output = np.sum((per[0] * nState) ** 2, axis=1)
    output = actions * output + actions
    action = np.argmax(output)
    win = getReward(state)
    if win == 1:
        per[1] += per[0]
        per[4] += per[3]
        per[2][0] += 1
    if win == 0:
        per[0] = np.random.rand(getActionSize(), getStateSize())
        per[3] = np.random.rand(getActionSize(), getStateSize()) * 10
    return action, per


@njit()
def Test(state, per):
    actions = getValidActions(state)
    #  nState = state - 1
    nState = state - per[0]
    output = np.sum((per[1] * nState) ** 2, axis=1)
    output = actions * output + actions
    #  action = np.argmax(output)
    list_action = np.where(actions == 1)[0]
    action = list_action[np.argmax(output[list_action])]
    return action, per


def convert_to_save(perData):
    if len(perData) == 2:
        raise Exception("Data này đã được convert rồi.")
    data = List()
    data.append(perData[4] / perData[2][0])
    data.append(perData[1] / perData[2][0])
    return data


def convert_to_test(perData):
    return List(perData)
