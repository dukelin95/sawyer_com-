from rllab.env_spec import EnvSpec
from robosuite.wrappers import Wrapper
from cached_property import cached_property

class sac_wrapper(Wrapper):

    def __init__(self, env):
        super().__init__(env)

    @cached_property
    def spec(self):
        return EnvSpec(
            observation_space=self.env.observation_space,
            action_space=self.env.action_space,
        )