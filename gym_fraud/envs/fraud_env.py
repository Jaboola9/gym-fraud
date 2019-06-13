import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pandas as pd
import random


class FraudEnv(gym.Env):
    def __init__(self):
        self.f = './dataset/creditcard.csv'
        self.df_xy = pd.DataFrame(pd.read_csv(self.f))
        self.ACTION_LOOKUP = {0: 'not_fraud', 1: 'fraud'}

        self.action_space = spaces.Discrete(len(self.ACTION_LOOKUP))
        self.observation_space = spaces.Discrete(self.df_xy.shape[0])

        self.ob = self._get_random_initial_state()
        self.episode_over = False
        self.turns = 0
        self.sum_rewards = 0.0
        print(self.df_xy.shape[0])

    def step(self, action_index):
        """
                Parameters
                ----------
                action_index :
                Returns
                -------
                ob, reward, episode_over, info : tuple
                    ob (object) :
                        an environment-specific object representing your observation of
                        the environment.
                    reward (float) :
                        amount of reward achieved by the previous action. The scale
                        varies between environments, but the goal is always to increase
                        your total reward.
                    episode_over (bool) :
                        whether it's time to reset the environment again. Most (but not
                        all) tasks are divided up into well-defined episodes, and done
                        being True indicates the episode has terminated. (For example,
                        perhaps the pole tipped too far, or you lost your last life.)
                    info (dict) :
                         diagnostic information useful for debugging. It can sometimes
                         be useful for learning (for example, it might contain the raw
                         probabilities behind the environment's last state change).
                         However, official evaluations of your agent are not allowed to
                         use this for learning.
                """
        self.turns += 1
        self._take_action(action_index)
        self.ob = self._get_reward(action_index)
        self.reward = self._get_reward(action_index)
        if self.turns > 100 or self.sum_rewards > 50:
            self.episode_over = True

        return self.ob, self.reward, self.episode_over, {}

    def reset(self):
        """
               Reset the environment and supply a new state for initial state
               :return:
               """
        self.turns = 0
        self.ob = self._get_random_initial_state()
        self.episode_over = False
        self.sum_rewards = 0.0
        return self.ob

    def render(self, mode='human', close=False):
        pass

    def _take_action(self, action_index):
        """
                Take an action correpsonding to action_index in the current state
                :param action_index:
                :return:
                """
        assert action_index < len(self.ACTION_LOOKUP)
        action = self.ACTION_LOOKUP[action_index]
        # print(action)
        return

    def _get_random_initial_state(self):
        nrand = random.randint(0, self.df_xy.shape[0])
        return self.df_xy.iloc[nrand]['Class']

    def _get_reward(self, action_index):
        """
                Get reward for the action taken in the current state
                :return:
                """
        df = self.df_xy
        n = df[df['Class'] == self.ob].index[0]
        y = df.iloc[n]['Class']
        reward = 0.0
        if y == 0.0:
            if action_index == 0.0:
                reward = 1.0
            else:
                reward = -1.0
        elif y == 1.0:
            if action_index == 1.0:
                reward = 1.0
            else:
                reward = -1.0
        return reward

    # def _get_new_state(self):
    #     """
    #     Get the next state from current state
    #     :return:
    #     """
    #     df = self.df_xy
    #     n = df[df['Class'] == self.ob].index[0]
    #     y = df.iloc[n][0]
    #     next_state = df.iloc[n + 1][1]
    #     return next_state

    def _seed(self):
        return
