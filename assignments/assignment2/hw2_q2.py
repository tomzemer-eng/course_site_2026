from enum import Enum
from collections import namedtuple
from itertools import filterfalse


Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))

cond_dict = {Condition.CURE: -1, Condition.HEALTHY: 0, Condition.SICK: 1,
              Condition.DYING: 2, Condition.DEAD: 3}

def update_condition(agent1: Agent, agent2: Agent) -> tuple:
    """

    Notes
    -----
    Help function
    Update the conditions of two agents after a meeting.

    Parameters
    ----------
    agent1 : Agent
        An agent with a 'name' field and a 'category' field with a type of Condition.
    agent2 : Agent
        An agent with a 'name' field and a 'category' field with a type of Condition.

    Returns
    -------
    updated_agent1 : Agent
        An agent with an updated 'category' field.
    updated_agent2 : Agent
        An agent with an updated 'category' field.
    """
    if agent1.category == Condition.CURE and agent2.category == Condition.CURE:
        return agent1, agent2
    elif ((agent1.category == Condition.CURE and agent2.category != Condition.CURE) 
          or (agent2.category == Condition.CURE and agent1.category != Condition.CURE)):
            cure_agent = agent1 if agent1.category == Condition.CURE else agent2
            sick_agent = agent2 if agent1.category == Condition.CURE else agent1
            cond_val = cond_dict[sick_agent.category] -1
            new_cond = next((k for k, v in cond_dict.items() if v == cond_val), None)
            return cure_agent, Agent(sick_agent.name, new_cond)
    else:
        cond_val1 = cond_dict[agent1.category] + 1
        cond_val2 = cond_dict[agent2.category] + 1
        new_cond1 = next((k for k, v in cond_dict.items() if v == cond_val1), None)
        new_cond2 = next((k for k, v in cond_dict.items() if v == cond_val2), None)
        return Agent(agent1.name, new_cond1), Agent(agent2.name, new_cond2)

def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent type, containing a 'name' field and a 'category' field, with 'category' being of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result of the meeting.
    """
    conditions_to_drop = [Condition.DEAD, Condition.HEALTHY]
    updated_list = []
    list_agents = list(agent_listing)
    updated_list = list(filter(lambda agent: agent.category in conditions_to_drop, list_agents))
    list_agents = list(filterfalse(lambda agent: agent.category in conditions_to_drop, list_agents))
    for i in range(0, len(list_agents)-1, 2):
        updated_agent1, updated_agent2 = update_condition(list_agents[i], list_agents[i+1])
        updated_list.extend([updated_agent1, updated_agent2])
    if len(list_agents) % 2 == 1:
        updated_list.append(list_agents[-1]) 
    return updated_list
