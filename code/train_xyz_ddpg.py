import time
import robosuite as suite
from robosuite.wrappers.gym_wrapper import GymWrapper
import numpy as np

from stable_baselines.ddpg.policies import MlpPolicy
from stable_baselines.ddpg.noise import OrnsteinUhlenbeckActionNoise
from stable_baselines import DDPG

# from sawyer_primitive_reach import SawyerPrimitiveReach
from test_sawyer_xyz import SawyerPrimitiveReach
import argparse

parser = argparse.ArgumentParser(description='To log or not to log, no for no log')
parser.add_argument('log', metavar='log', type=str)
args = parser.parse_args()
if args.log == 'no':
  print("No saves")
  log = False 
else:
  print("All the saves")
  log = True

# use robosuite's gym_wrapper to wrap the sawyer stack env for baselines

# no object observation for PX,PY,PZ
# TODO turn on for pick policy?

render = False

policy = 'x'

nb_train_steps = 50
nb_rollout_steps = 100
batch_size = 256
critic_l2_reg = 0.01
buffer_size=int(1e6)
normalize=True

total_timesteps = int(0.4e6)

env = GymWrapper(
        SawyerPrimitiveReach(
            prim_axis=policy,
            has_renderer=render,
            has_offscreen_renderer=False,
      	    use_camera_obs=False,
            use_object_obs=True,
            horizon = 100,
            control_freq=100,  # control should happen fast enough so that simulation looks smooth
        )
    )

# the noise objects for DDPG
n_actions = env.action_space.shape[-1]
#sigma from DDPG paper
#action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=float(0.2) * np.ones(n_actions))
action_noise = None
if log:
  suff = str(time.strftime("_%d_%b_%Y_%H_%M_%S", time.localtime()))
else:
  suff = None

model = DDPG('MlpPolicy', env, verbose=2, render=render, 
              param_noise=None, 
              action_noise=action_noise,
              nb_train_steps = nb_train_steps,
              nb_rollout_steps = nb_rollout_steps,
              normalize_observations = normalize,
              batch_size = batch_size, 
              critic_l2_reg=critic_l2_reg,
              buffer_size=buffer_size,
#              policy_kwargs={'layers':[400,300]},
              logging=suff)

start = time.time()

model.learn(total_timesteps=total_timesteps, log_interval=1)

if log :
  model.save("pkl/{}".format(suff))
  print("Saved as {0}, trained {1} primitive policy for {2} timesteps in {3}".format(suff, policy, total_timesteps, time.strftime('%H:%M:%S', time.gmtime(time.time()-start))))

else: 
  print("Trained {0} primitive policy for {1} timesteps in {2}".format(policy, total_timesteps, time.strftime('%H:%M:%S', time.gmtime(time.time()-start))))
