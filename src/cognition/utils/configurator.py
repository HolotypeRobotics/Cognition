class Configurator:
    def __init__(self):
        pass

    def configure_agent(self, agent, config_data):
        """
        Configures an agent with the provided configuration data.

        Args:
            agent (Agent): the agent instance to configure.
            config_data (dict): a dictionary containing configuration settings.
        """

        # Access blocks and modules from the agent
        blocks = agent.blocks
        modules = agent.modules

        # Apply configuration to blocks
        for region, block in blocks.items():
            block_config = config_data.get(region, {})
            self.configure_block(block, block_config)

        # Apply configuration to modules
        for module in modules:
            module_config = config_data.get(module.name, {})
            self.configure_module(module, module_config)

        # Configure the scheduler if applicable
        try:
            scheduler = agent.scheduler
            scheduler_config = config_data.get("scheduler", {})
            self.configure_scheduler(scheduler, scheduler_config)
        except AttributeError:
            pass  # No scheduler present

    def configure_block(self, block, config_data):
        """
        Configures a block with the provided configuration data.

        Args:
            block (Block): the block instance to configure.
            config_data (dict): a dictionary containing configuration settings for the block.
        """
        block.configure(config_data)

    def configure_module(self, module, config_data):
        """
        Configures a module with the provided configuration data.

        Args:
            module (Module): the module instance to configure.
            config_data (dict): a dictionary containing configuration settings for the module.
        """
        module.configure(config_data)

    def configure_scheduler(self, scheduler, config_data):
        """
        Configures a scheduler with the provided configuration data.

        Args:
            scheduler (Scheduler): the scheduler instance to configure.
            config_data (dict): a dictionary containing configuration settings for the scheduler.
        """
        scheduler.configure(config_data)
