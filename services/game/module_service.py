class ModuleService:
    """Gestisce tutti i moduli tattici del gioco."""

    MODULES = {

        "4-3-3": {

            "name": "4-3-3",

            "slots": [
                "GK",

                "LB",
                "CB1",
                "CB2",
                "RB",

                "CM1",
                "CM2",
                "CM3",

                "LW",
                "ST",
                "RW"
            ],

            "limits": {
                "Goalkeeper": 1,
                "Defence": 4,
                "Midfield": 3,
                "Attack": 3
            },

            "compatible_positions": {

                "GK": [
                    "Goalkeeper"
                ],

                "LB": [
                    "Left-Back",
                    "Left Wing-Back"
                ],

                "CB1": [
                    "Centre-Back"
                ],

                "CB2": [
                    "Centre-Back"
                ],

                "RB": [
                    "Right-Back",
                    "Right Wing-Back"
                ],

                "CM1": [
                    "Central Midfield",
                    "Defensive Midfield",
                    "Attacking Midfield"
                ],

                "CM2": [
                    "Central Midfield",
                    "Defensive Midfield",
                    "Attacking Midfield"
                ],

                "CM3": [
                    "Central Midfield",
                    "Defensive Midfield",
                    "Attacking Midfield"
                ],

                "LW": [
                    "Left Winger",
                    "Left Midfield"
                ],

                "ST": [
                    "Centre-Forward",
                    "Second Striker"
                ],

                "RW": [
                    "Right Winger",
                    "Right Midfield"
                ]
            }
        }
    }

    DEFAULT_MODULE = "4-3-3"

    def get_module(self, module_name=None):

        if module_name is None:
            module_name = self.DEFAULT_MODULE

        return self.MODULES.get(module_name)

    def get_slots(self, module_name=None):

        module = self.get_module(module_name)

        return module["slots"]

    def get_limits(self, module_name=None):

        module = self.get_module(module_name)

        return module["limits"]

    def get_compatible_positions(self, module_name=None):

        module = self.get_module(module_name)

        return module["compatible_positions"]

    def exists(self, module_name):

        return module_name in self.MODULES

    def get_available_modules(self):

        return list(self.MODULES.keys())