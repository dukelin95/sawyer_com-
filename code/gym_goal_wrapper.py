"""
This file implements a wrapper for facilitating compatibility with OpenAI gym.
This is useful when using these environments with code that assumes a gym-like 
interface.
"""

import numpy as np
from gym import spaces
from robosuite.wrappers import Wrapper


class GymGoalEnvWrapper(Wrapper):
    env = None
 
    def __init__(self, env, keys=None, early=False):
        """
        Initializes the Gym wrapper.

        Args:
            env (MujocoEnv instance): The environment to wrap.
            keys (list of strings): If provided, each observation will
                consist of concatenated keys from the wrapped environment's
                observation dictionary. Defaults to robot-state and object-state.
        """
        super().__init__(env)
        self.metadata = None
        if keys is None:
            assert self.env.use_object_obs, "Object observations need to be enabled."
            keys = ["robot-state", "object-state"]
        self.keys = keys

        # set up observation and action spaces
        flat_ob = self._flatten_obs(self.env.reset(), verbose=True)
        self.obs_dim = flat_ob.size
        high = np.inf * np.ones(self.obs_dim)
        low = -high
        self.observation_space = spaces.Dict(dict(
           desired_goal=spaces.Box(-np.inf, np.inf, shape=(3,)),
           achieved_goal=spaces.Box(-np.inf, np.inf, shape = (3,)),
           observation=spaces.Box(low=low, high=high,),
        ))

        self.action_space = self.env.action_space
        self.early = early

    def _flatten_obs(self, obs_dict, verbose=False):
        """
        Filters keys of interest out and concatenate the information.

        Args:
            obs_dict: ordered dictionary of observations
        """
        ob_lst = []
        for key in obs_dict:
            if key in self.keys:
                if verbose:
                    print("adding key: {}".format(key))
                ob_lst.append(obs_dict[key])
        return np.concatenate(ob_lst)

    def reset(self):
        ob_dict = self.env.reset()
        return self.env.get_goalenv_dict(ob_dict)

    def step(self, action):
        ob_dict, reward, done, info = self.env.step(action)
        if reward == 0 and self.early:
            print("early termination")
            done = True
        return self.env.get_goalenv_dict(ob_dict), reward, done, info

    def compute_reward(self, achieved_goal, desired_goal, info=None):
        return self.env.compute_reward(achieved_goal, desired_goal, None)


