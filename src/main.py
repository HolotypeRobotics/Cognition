from cognition.agent import Agent

# main function
if  __name__ == '__main__':
    agent = Agent()
    agent.configure('configs/agent.yml')
    while True:
        agent.run()