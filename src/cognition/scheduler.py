class Scheduler:

    def __init__(self, blocks):
        self.blocks = blocks


    def run(self):
        for block in self.blocks:
            block.update()

    def add_block(self, block):
        self.blocks.append(block)

    

    # def __init__(self, tasks):
    #     self.tasks = tasks  # type: List[Task]
    #     self.current_time = 0
            
    # def run(self):
    #     while True:
    #         yield from self._run_once()
    #         self.run = run.__get__(self)

    # @property
    # def is_running(self):
    #         return self.run != run.__get__(None)
    #     self.run = None

    # def _run_once(self):
    #     yield from sorted(self.tasks, key=lambda t: t.deadline)
    #     self.current_time = self.tasks[0].deadline
    #     while self.tasks:
    #         next_task = self.tasks.pop(0)
    #         print(f"Running {next_task}")
    #         next_task.action()
    #         yield from sorted(self.tasks, key=lambda t: t.deadline)
    #         self.current_time = self.tasks[0].deadline


    # def add_task(self, task: Task) -> None:
    #     """Add a new task to the scheduler."""
    #     if not isinstance(task, Task):
    #         raise TypeError("Argument must be of type 'Task'")
    #     self.tasks.append(task)
    #     def remove_task(self, task: Task) -> bool:
    #         return self.tasks.remove(task)
    #     setattr(task, "remove", remove_task.__get__(task))
    #     def run_next_task(self) -> None:
    #         next_task = min((t for t in self.tasks if t.deadline <= self.current_time), default=None)
    #         if next_task is None:
    #             print("No tasks left.")
    #         else:
    #             print(f"Running {next_task}")
    #             next_task.action()
    #             self.current_time = next_task.deadline
    #             task.run_next_task = run_next_task.__get__(task)
    #             task.run_next_task()