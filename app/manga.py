from discord.ext import commands
import discord
from api.data import load_page, find_manga, reader_cap, search_manga

class Manga(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.messages = []

    async def button_callback(self, interaction, ctx, title, manga_url, img_url, page=0):
        chapters = find_manga(title)
        
        items_per_page = 6  # Número de capítulos por página
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        chapters_page = chapters[start_idx:end_idx]
        
        chapters_content = "\n".join([f"[{ch_title}]({ch_url})" for (ch_title, ch_url) in chapters_page])
        embed_chapters = discord.Embed(title=title, description=chapters_content)
        embed_chapters.set_thumbnail(url=img_url)
        
        number_buttons = []
        for i, (ch_title, ch_url) in enumerate(chapters_page):
            number_buttons.append(await self.create_number_button(ctx, ch_title.split(" ")[1], ch_url))
        
        left_arrow = discord.ui.Button(label="◀️", style=discord.ButtonStyle.primary, custom_id=f"left_{title}_{page}")
        right_arrow = discord.ui.Button(label="▶️", style=discord.ButtonStyle.primary, custom_id=f"right_{title}_{page}")
        first_page_button = discord.ui.Button(label="<<", style=discord.ButtonStyle.primary, custom_id=f"first_{title}")
        last_page_button = discord.ui.Button(label=">>", style=discord.ButtonStyle.primary, custom_id=f"last_{title}")
        
        left_arrow.callback = lambda interaction: self.left_callback(interaction, ctx, title, manga_url, img_url, page)
        right_arrow.callback = lambda interaction: self.right_callback(interaction, ctx, title, manga_url, img_url, page)
        first_page_button.callback = lambda interaction: self.first_page_callback(interaction, ctx, title, manga_url, img_url)
        last_page_button.callback = lambda interaction: self.last_page_callback(interaction, ctx, title, manga_url, img_url, chapters)
        
        view = discord.ui.View()
        view.add_item(first_page_button)
        view.add_item(left_arrow)
        for button in number_buttons:
            view.add_item(button)
        view.add_item(right_arrow)
        view.add_item(last_page_button)
        
        await interaction.response.edit_message(embed=embed_chapters, view=view)

    async def create_thread(self, ctx, user_name, manga_title):
        channel = ctx.channel
        thread_name = f"{user_name}-{manga_title}"
        thread = await channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
        return thread

    async def create_number_button(self, ctx, ch_title, ch_url):
        button = discord.ui.Button(label=ch_title, style=discord.ButtonStyle.secondary)
        
        async def number_callback(interaction):
            try:
                user_name = interaction.user.name
                thread = await self.create_thread(ctx, user_name, ch_title)
        
                images = reader_cap(ch_url)
                if images:
                    for img_url in images:
                        embed_img = discord.Embed()
                        embed_img.set_image(url=img_url)
                        await thread.send(embed=embed_img)
                else:
                    await thread.send("No se encontraron imágenes para este capítulo.")
            except Exception as e:
                print(f"Error en number_callback: {e}")
        
        button.callback = number_callback
        return button

    async def left_callback(self, interaction, ctx, title, manga_url, img_url, page):
        new_page = max(page - 1, 0)
        await self.button_callback(interaction, ctx, title, manga_url, img_url, new_page)

    async def right_callback(self, interaction, ctx, title, manga_url, img_url, page):
        new_page = page + 1
        await self.button_callback(interaction, ctx, title, manga_url, img_url, new_page)

    async def first_page_callback(self, interaction, ctx, title, manga_url, img_url):
        await self.button_callback(interaction, ctx, title, manga_url, img_url, 0)

    async def last_page_callback(self, interaction, ctx, title, manga_url, img_url, chapters):
        num_pages = (len(chapters) + 5) // 6  # Calculate number of pages with 6 items per page
        await self.button_callback(interaction, ctx, title, manga_url, img_url, num_pages - 1)

    @commands.command(name="latestUpdate")
    async def latestUpdate(self, ctx):
        mangas = load_page()
        
        self.messages.clear()  # Clear previous messages tracking
        for title, manga_url, img_url in mangas:
            await self.send_manga_embed(ctx, title, manga_url, img_url)

    async def send_manga_embed(self, ctx, title, manga_url, img_url):
        embed = discord.Embed(title=title, description=f"[Ver Manga]({manga_url})")
        embed.set_thumbnail(url=img_url)
        button = discord.ui.Button(label="Ver más", style=discord.ButtonStyle.green, emoji="📖")
        
        button.callback = lambda interaction, title=title, manga_url=manga_url, img_url=img_url: self.local_button_callback(interaction, ctx, title, manga_url, img_url)

        view = discord.ui.View()
        view.add_item(button)
        msg = await ctx.send(embed=embed, view=view)
        self.messages.append(msg)

    async def local_button_callback(self, interaction, ctx, title, manga_url, img_url):
        # Delete all previous messages in the search result except the selected one
        for message in self.messages:
            if message.id != interaction.message.id:
                await message.delete()
        self.messages.clear()
        await self.button_callback(interaction, ctx, title, manga_url, img_url)

    @commands.command(name="search")
    async def search(self, ctx, *, query):
        if query != None:
            mangas = search_manga(query)
        
            if not mangas:
                await ctx.send(f"No se encontraron resultados para '{query}'.")
                return
        
            self.messages.clear()  # Clear previous messages tracking
            for i, (title, img_url, manga_url) in enumerate(mangas):
                await self.send_manga_embed(ctx, title, manga_url, img_url)
        else:
            await ctx.send("Por favor, introduce un término de búsqueda.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Manga(bot))
