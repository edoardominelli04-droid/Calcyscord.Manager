import re


class SlotUtils:
    """Utility per la gestione degli slot tattici."""

    @staticmethod
    def family(slot):
        """
        Restituisce la famiglia dello slot.

        Esempi:
        CB1 -> CB
        CB2 -> CB
        CM3 -> CM
        DM1 -> DM
        ST2 -> ST
        GK -> GK
        LW -> LW
        """

        return re.sub(r"\d+$", "", slot)

    @staticmethod
    def department(slot):
        """
        Restituisce il reparto dello slot.
        """

        family = SlotUtils.family(slot)

        if family == "GK":
            return "Goalkeeper"

        if family in (
            "LB",
            "LWB",
            "CB",
            "RB",
            "RWB"
        ):
            return "Defence"

        if family in (
            "DM",
            "CM",
            "AM",
            "LM",
            "RM"
        ):
            return "Midfield"

        return "Attack"