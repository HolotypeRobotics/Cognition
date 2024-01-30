from cognition.agent import Agent

# main function
if  __name__ == '__main__':
    agent = Agent()
    agent.configure('configs/agent.yml')
    for i in range(10):
        print(f"Running agent iteration {i}")
        agent.run()