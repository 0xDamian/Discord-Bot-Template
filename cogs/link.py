from discord.ext import commands
from discord import ui, ButtonStyle, Interaction

class LinkFilter(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.staff_channel_id = 1106677152289656852 # Replace with your staff channel ID
        self.channels = [1106652682946621460, 1095816946466967686, 1095818905215316088, 1099517647114227723] # Replace with your list of channel IDs for the dropdown menu

    @commands.Cog.listener()
    async def on_message(self, message):
        if "http" in message.content:
            try:
                await message.delete()
            except:
                pass
            staff_channel = self.client.get_channel(self.staff_channel_id)
            view = LinkFilterView(self.client, message.author, message.content, self.channels)
            await staff_channel.send(f"Link posted by {message.author.mention}: {message.content}", view=view)

class LinkFilterView(ui.View):
    def __init__(self, client, author, content, channels):
        super().__init__()
        self.client = client
        self.author = author
        self.content = content
        self.channels = channels
        self.add_item(ui.Select(placeholder="Select a channel", options=[ui.SelectOption(label=str(channel), value=str(channel)) for channel in channels], callback=self.select_callback))
        self.add_item(ui.Button(label="Allow", style=ButtonStyle.green, callback=self.allow_button))
        self.add_item(ui.Button(label="Deny", style=ButtonStyle.red, callback=self.deny_button))

    async def select_callback(self, select: ui.Select, interaction: Interaction):
        channel = self.client.get_channel(int(select.values[0]))
        await channel.send(f"{self.content} (posted by {self.author.mention})")
        await interaction.response.send_message("Link approved and posted in selected channel.", ephemeral=True)

    async def allow_button(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message("Please select a channel from the dropdown menu.", ephemeral=True)

    async def deny_button(self, button: ui.Button, interaction: Interaction):
        await self.author.send("Your link has been denied by the staff.")
        await interaction.response.send_message("Link denied and warning sent to original poster.", ephemeral=True)

async def setup(client):
    await client.add_cog(LinkFilter(client))
    print("LinkFilter Loaded")
