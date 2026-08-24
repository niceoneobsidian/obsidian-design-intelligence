from odi.bootstrap import ODIKernel
from odi.core.types import Intent, ExecutionResult

class ODIApplication:
    """Thin application boundary; orchestration remains inside the kernel."""
    def __init__(self, kernel: ODIKernel):
        self.kernel = kernel

    def submit(self, intent: Intent) -> ExecutionResult:
        raise NotImplementedError("Wire a production planner and capability selector at the application boundary.")
