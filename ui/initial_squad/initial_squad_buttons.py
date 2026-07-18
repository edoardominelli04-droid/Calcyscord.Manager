import discord


class RoleButton(discord.ui.Button):
    def __init__(self, label, emoji, role, row):
        self.role = role
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.secondary, row=row)
    async def callback(self, interaction: discord.Interaction):
        await self.view.open_player_list(self.role).show(interaction)


class GoalkeepersButton(RoleButton):
    def __init__(self): super().__init__("Portieri", "🥅", "Goalkeeper", 0)


class DefendersButton(RoleButton):
    def __init__(self): super().__init__("Difensori", "🛡️", "Defender", 0)


class MidfieldersButton(RoleButton):
    def __init__(self): super().__init__("Centrocampisti", "🎯", "Midfield", 1)


class ForwardsButton(RoleButton):
    def __init__(self): super().__init__("Attaccanti", "⚽", "Attack", 1)


class ConfirmSquadButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Conferma rosa", emoji="✅", style=discord.ButtonStyle.success, row=2, disabled=True)

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        await interaction.response.defer()

        confirmed, result_message = view.service.confirm_squad(view.manager_id)
        if not confirmed:
            await interaction.followup.send(f"❌ {result_message}", ephemeral=True)
            return

        try:
            draft = view.service.get_draft(view.manager_id)
            counts = view.service.get_role_counts(view.manager_id)
            from ui.initial_squad.manager_statement_view import ManagerStatementView
            statement_view = ManagerStatementView(view.manager_id)

            # Dopo un defer, questa è l'API corretta per sostituire il
            # messaggio sul quale è stato premuto il pulsante.
            await interaction.edit_original_response(
                embed=view.embed_builder.build_confirmed(draft, counts),
                view=statement_view
            )
            statement_view.message = await interaction.original_response()

            # Arrestiamo la vecchia view soltanto dopo che Discord ha
            # confermato la sostituzione dei componenti.
            view.stop()
        except Exception as error:
            print("ERRORE TRANSIZIONE DOPO CONFERMA ROSA:", repr(error))
            try:
                await interaction.followup.send(
                    "⚠️ La rosa è stata confermata, ma non sono riuscito ad "
                    "aprire automaticamente il passaggio successivo. "
                    "Usa `!riprendi`.\n"
                    f"Errore: `{type(error).__name__}: {error}`",
                    ephemeral=True
                )
            except discord.HTTPException:
                pass
