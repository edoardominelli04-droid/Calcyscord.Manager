import discord


class PlayerListEmbedBuilder:
    """Embed che visualizza una lista di giocatori."""

    def build(
        self,
        role,
        players,
        selected_players,
        required
    ):

        role_titles = {
            "Goalkeeper": "🥅 Portieri",
            "Defender": "🛡️ Difensori",
            "Midfield": "🎯 Centrocampisti",
            "Attack": "⚽ Attaccanti"
        }

        embed = discord.Embed(
            title=role_titles.get(role, role),
            colour=discord.Colour.blurple()
        )

        if not players:

            embed.description = (
                "Nessun giocatore disponibile."
            )

        else:

            lines = []


            for index, player in enumerate(players[:25], start=1):


                value = player.get("market_value") or 0

                tier = player.get("initial_tier", "D")

                cost = player.get("initial_cost", 1)


                lines.append(


                    f"**{index}.** {player['name']}\n"
                    f"🏷️ Fascia **{tier}** • ⭐ **{cost}**\n"
                    f"💰 {value:,.0f} €".replace(",", ".")


                )


            embed.description = "\n\n".join(lines)


        selected_names = (
            "\n".join(
                f"• {player['name']} — "
                f"{player.get('initial_tier', 'D')}, "
                f"⭐ {player.get('initial_cost', 1)}"
                for player in selected_players
            )
            if selected_players
            else "Nessun giocatore selezionato."
        )

        if role in ("Goalkeeper", "Defender", "Midfield", "Attack"):

            required_selected = min(
                len(selected_players),
                required
            )

            flexible_selected = max(
                0,
                len(selected_players) - required
            )

            selection_status = (
                f"Obbligatori: **{required_selected}/{required}** • "
                f"Flessibili: **{flexible_selected}**\n\n"
                f"{selected_names}"
            )

            field_name = f"✅ Selezionati ({len(selected_players)} totali)"

        else:

            selection_status = selected_names

            field_name = f"✅ Selezionati ({len(selected_players)}/{required})"

        embed.add_field(
            name=field_name,
            value=selection_status,
            inline=False
        )

        embed.set_footer(

            text=(
                f"{len(players)} giocatori disponibili • "
                "usa il secondo menu per rimuovere"
            )

        )

        return embed
