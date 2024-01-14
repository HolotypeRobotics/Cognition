import threading

class Scheduler:
    def __init__(self):
        self.hierarchy = None
        self.tasks = []

    def set_hierarchy(self, hierarchy):
        self.hierarchy = hierarchy

    def run(self):
        if self.hierarchy is None:
            raise RuntimeError("No hierarchy set for scheduler")
        
        call_stack = self.hierarchy.call_stack()
        threads = []

        # First, process data in all blocks
        for block in call_stack:
            thread = threading.Thread(target=block.process_data, args=(self.current_time,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Then, transfer data in all blocks
        for block in call_stack:
            thread = threading.Thread(target=block.transfer_data)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


