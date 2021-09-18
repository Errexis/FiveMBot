import discord
import asyncio
from discord import reaction
from discord.ext import commands, tasks
from datetime import datetime
import time
import os
import random
import fivem

client = commands.Bot(command_prefix="ba!")

server: fivem.getServer("177.54.145.74:30120") # teste para puxar as info do servidor 
print(server.players)

@client.event
async def on_ready():
    activity = discord.Streaming(name="Em breve novidades!", url="https://twitch.tv/rxrp_", type=1)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot has successfully logged in as: {}".format(client.user))
    print("Bot ID: {}\n".format(client.user.id))
    

@client.command()  # teste para puxar as info do servidor ( ainda em desenvolvimento )
async def players(ctx):
    await ctx.message.delete() 
    players = server.players
    player = discord.Embed(
        title = "Players Online",
        description = players,
        color = discord.Colour.from_rgb(90,5,97))
    await ctx.message.send(embed=player)

@client.command()
async def say(ctx, *, teste):
    await ctx.message.delete()
    if ctx.message.author.id == 248516756463681536:
        await ctx.channel.send(teste)
    else:
        await ctx.channel.send(f'{ctx.message.author.mention}, você não tem permissão para esse comando')

@client.command()
async def rx(ctx):
    await ctx.message.delete()
    await ctx.send(f'{ctx.message.author.mention}, https://twitch.tv/rxrp_')

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def anuncio(ctx,titulo,message,r=0,g=0,b=255):
    await ctx.message.delete()
    announce = discord.Embed(
        title = titulo,
        description = message,
        color = discord.Colour.from_rgb(r,g,b),
        timestamp = datetime.now())
    announce.set_footer(text=ctx.message.author.display_name)
    announce.set_thumbnail(url="https://cdn.discordapp.com/icons/827574690145894462/a_34c4acd6e628e056a47a07fc8190020d.gif?size=2048")
    await ctx.channel.send(embed=announce)

@client.command()
@commands.has_permissions(administrator=True)
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Informações do Servidor", timestamp=datetime.now(), color=discord.Color.blue())
    embed.add_field(name="Servidor criado em", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Proprietário do servidor", value=f"{ctx.guild.owner_id}")
    embed.add_field(name="Região do Servidor", value=f"{ctx.guild.region}")
    embed.add_field(name="ID do Servidor", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/827574690145894462/a_34c4acd6e628e056a47a07fc8190020d.gif?size=2048")

    await ctx.send(embed=embed)

#####Moderação
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick()
    await ctx.channel.send(f'{member.mention} foi kickado!')

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban()
    await ctx.channel.send(f'{member.mention} foi banido!')

@client.command()
@commands.has_permissions(administrator=True)
async def puni(ctx, member: discord.Member, id, punicao, reason=None):
    canal =  client.get_channel(id=827574692998283282)
    msg = discord.Embed(
        title = 'Punição',
        description = f'**ID:** {id} {member.mention}\n**Motivo:** {reason}\n**Punição:** {punicao}\n\n**Se você achar sua punição incoerente, basta abrir um ticket e aguarde a resposta da administração.**',
        #setAuthor = 'Punições',
        color = discord.Colour.from_rgb(90,5,97),
        timestamp = datetime.now())
    msg.set_footer(text=f'enviado por: {ctx.message.author.display_name}')
    msg.set_thumbnail(url="https://cdn.discordapp.com/icons/827574690145894462/a_34c4acd6e628e056a47a07fc8190020d.gif?size=2048")
    await canal.send(embed=msg)

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=20):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(manage_channels = True)
async def mutechannel(ctx):
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send( ctx.channel.mention + " canal mutado.")

@client.command()
@commands.has_permissions(manage_channels = True)
async def unmutechannel(ctx):
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send( ctx.channel.mention + " canal desmutado.")

@client.command()
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: int):
    await ctx.message.delete()
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"O Slow Mode foi atualizado para {seconds} segundos.")

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name="[💢] Mutado")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_role(name="[💢] Mutado", permissions=perms)
        await member.add_roles(role)
        await ctx.send(f"{member} foi mutado.")
    else:
        await member.add_roles(role)
        await ctx.send(f"{member} foi mutado")

@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name="[💢] Mutado")
    guild = ctx.guild
    await member.remove_roles(role)
    await ctx.send(f"{member} foi desmutado.")

#messagem automatica a cada 8hrs
@tasks.loop(hours=8)
async def send():
    channel = await client.fetch_channel(861451613737975818)
    automsg = discord.Embed(
        title = 'Adquira já seu VIP conosco!',
        description = f'**Está cansado de pegar fila, ou quer um carro melhor? confira já nossos pacotes de VIPs, caso tenha alguma dúvida abra um ticket!**',
        color = discord.Colour.from_rgb(90,5,97),
        timestamp = datetime.now())
    automsg.set_footer(text=f'Blast Academy©')
    automsg.set_thumbnail(url="https://cdn.discordapp.com/icons/827574690145894462/a_34c4acd6e628e056a47a07fc8190020d.gif?size=2048")
    await channel.send(embed=automsg)

@send.before_loop
async def before():
    await client.wait_until_ready()

@client.command(pass_context=True)
async def rename(ctx, member: discord.Member, *, newnick):
  await ctx.message.delete()
  await member.edit(nick=newnick)
  await ctx.channel.send(f'>>> Foi alterado o nome de {member.mention}')

@client.event
async def on_message(ctx):
    if ctx.channel.id == 867624467177013258 and not ctx.author.bot:
        msg = ctx.content.lower()
        lin1 = msg.splitlines(1)[0]
        lin2 = msg.splitlines(1)[1]
        nome = ""
        pid = ""
        if lin1.startswith("nome"):
            nome = lin1.split("nome:")[1]
            pid = lin2.split("id:")[1]
        elif lin1.startswith("id"):
            pid = lin1.split("id:")[1]
            nome = lin2.split("nome:")[1]

        if nome.startswith(" "):
            nome = nome[1:]
        if pid.startswith(" "):
            pid = pid[1:]

        pnick = f"{pid} | {nome.title()}"
        if "\n" in pnick:
          pnick = pnick.replace("\n","").replace("  "," ")
        await ctx.add_reaction('✅')
        await ctx.author.edit(nick=f'{pnick}')
        await ctx.add_reaction('❌')        
        """ await ctx.channel.send(pnick) """

    if ctx.channel.id == 883411060525260911 and not ctx.author.bot:
        await ctx.add_reaction('✅')
        await ctx.add_reaction('❌')

send.start()

client.run('')
