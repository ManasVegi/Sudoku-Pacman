# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
import sys
import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        "*** YOUR CODE HERE ***"
        self.q_dict = {}

    def getQValue(self, state, action):
      # Just retrieve Q from dictionary
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # data structure to store the current Q values (e.g. dictionary / hashing)
        if (state, action) in self.q_dict:
              return self.q_dict[(state, action)]
        else:
          return 0.0


    def computeValueFromQValues(self, state):
      # Part 2 of step d
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        max_q_value = -float('inf')
        max_q_action = None
        unseen_actions = list()
        for action in self.getLegalActions(state):
          current_q_value = self.getQValue(state, action)
          if current_q_value > max_q_value: # catch the negative seen cases 
            max_q_value = current_q_value
            max_q_action = action
          elif current_q_value == 0.0: # cases that are unseen
            unseen_actions.append(action)

        if (len(self.getLegalActions(state)) == 0):
          return 0.0
        elif max_q_value < 0 and len(unseen_actions) > 0: # all the seen cases are negative
          value = self.getQValue(state, random.choice(unseen_actions))
          return value
        else:
          return max_q_value

    def computeActionFromQValues(self, state):
        # Step a
        # Select the action with the largest Q value
        max_q_value = -float('inf')
        max_q_action = None
        unseen_actions = list()
        for action in self.getLegalActions(state):
          current_q_value = self.getQValue(state, action)
          if current_q_value > max_q_value: # catch the negative seen cases 
            max_q_value = current_q_value
            max_q_action = action
          elif current_q_value == 0.0: # cases that are unseen
            unseen_actions.append(action)
        if (len(self.getLegalActions(state)) == 0):
          return None
        elif max_q_value < 0 and len(unseen_actions) > 0: # all the seen cases are negative
          return random.choice(unseen_actions)
        else:
          return max_q_action

    def getAction(self, state):
      # Step a
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        # Step a from value iteration algorithm
        if (util.flipCoin(self.epsilon)):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):
      # Step d
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        value = reward + self.discount * self.computeValueFromQValues(nextState)
        self.q_dict[(state, action)] = value
            # over here 
            # call compute values from q values 

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        return self.weights * self.featExtractor.getFeatures(state, action)

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        max_q_value = self.computeValueFromQValues(nextState)
        difference = (reward + self.discount * max_q_value) - self.getQValue(state, action)
        for k, v in self.featExtractor.getFeatures(state, action).items():
          self.weights[k] = self.weights[k] + self.alpha * difference * v


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            print(self.weights.items())
            pass
