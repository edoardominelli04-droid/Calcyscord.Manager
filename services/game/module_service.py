from services.game.data.modules import MODULES


class ModuleService:
    """Gestisce i moduli tattici."""

    DEFAULT_MODULE = "4-3-3"

    def __init__(self):
        self.modules = MODULES

    # ==========================================================
    # MODULI
    # ==========================================================

    def get_module(self, module_name=None):

        if module_name is None:
            module_name = self.DEFAULT_MODULE

        module = self.modules.get(module_name)

        if module is None:
            raise ValueError(
                f"Il modulo '{module_name}' non esiste."
            )

        return module

    def get_slots(self, module_name=None):

        return self.get_module(module_name)

    def get_available_modules(self):

        return list(self.modules.keys())

    def exists(self, module_name):

        return module_name in self.modules