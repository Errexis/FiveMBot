import os
import discord
import asyncio
import time
#discord ext
from discord import reaction
from discord.ext import commands
from discord.ext import tasks
from mysql.connector import cursor
import requests as rq
from datetime import datetime
import mysql.connector 

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anakin123",
    database="blastbot"
)
mycursor = db.cursor()
db_info = db.get_server_info()
print(f'Database do bot Iniciada, Versão do MYSQL:{db_info}')


client = commands.Bot(command_prefix=['$'])
client.remove_command('help')

## Config
class config:
    serverIP = "blastrp.com.br:30120" #IP:PORT | Example: 87.98.246.41:30120 | Use 127.0.0.1:PORT if you're running it on same Server as FiveM Server.
    serverIPC = "blastrp.com.br"
    guildID = 829468262320177202 #Your Discord Server ID, must be int. | Example: 721939142455459902
    Token = "" #Your Discord Bot Token 


@client.event
async def on_ready():
    activity = discord.Streaming(name="Em breve novidades!", url="https://twitch.tv/rxrp_", type=1)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot has successfully logged in as: {}".format(client.user))
    print("Bot ID: {}\n".format(client.user.id))

#request
def pc():
    try:
        resp = rq.get('http://'+config.serverIP+'/players.json').json()
        return(len(resp))
    except:
        return('N/A')

## Say Commands
@client.command(pass_content=True, aliases=['s'])
@commands.has_permissions(administrator=True) 
async def say(ctx, *, text):

    try:
        await ctx.message.delete()
        embed=discord.Embed(title="Blast Academy", description=" ", color= discord.Colour.from_rgb(90,5,97), timestamp=datetime.now())
        embed.set_author(name="Blast Bot", url="", icon_url="https://images-ext-1.discordapp.net/external/DKb6qWSNVPhR-E4lMc5e74W_2s7DsYNUnp6oM7jtxJA/%3Fsize%3D2048/https/cdn.discordapp.com/icons/794341861413355520/a_36f54b448066c33bb40e09c89a695f73.gif")
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/DKb6qWSNVPhR-E4lMc5e74W_2s7DsYNUnp6oM7jtxJA/%3Fsize%3D2048/https/cdn.discordapp.com/icons/794341861413355520/a_36f54b448066c33bb40e09c89a695f73.gif")
        embed.add_field(name="Mensagem:", value=text, inline=False)
        embed.set_footer(text=f"{ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    except Exception as err:
        print(err)
    
@client.command(pass_context=True, aliases=['hs'])
@commands.has_permissions(administrator=True) 
async def hsay(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

@client.command()
@commands.has_permissions(administrator=True) 
async def online(ctx):
    await ctx.message.delete()
    content = "~~@everyone~~"
    embed=discord.Embed(title="Server Online !", description="O Servidor já se encontra online! para se conectar siga a instrução baixo e bom jogo.", color=discord.Colour.from_rgb(90,5,97), timestamp=datetime.now())
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/DKb6qWSNVPhR-E4lMc5e74W_2s7DsYNUnp6oM7jtxJA/%3Fsize%3D2048/https/cdn.discordapp.com/icons/794341861413355520/a_36f54b448066c33bb40e09c89a695f73.gif")
    embed.add_field(name="✅ Cole o comando no F8 ✅", value=f"connect {config.serverIPC}", inline=False)
    await ctx.send(embed=embed, content=content)

@client.command()
@commands.has_permissions(administrator=True)
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Informações do Servidor", timestamp=datetime.now(), color=discord.Colour.from_rgb(90,5,97))
    embed.add_field(name="Servidor criado em", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Proprietário do servidor", value=f"{ctx.guild.owner_id}")
    embed.add_field(name="Região do Servidor", value=f"{ctx.guild.region}")
    embed.add_field(name="ID do Servidor", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/DKb6qWSNVPhR-E4lMc5e74W_2s7DsYNUnp6oM7jtxJA/%3Fsize%3D2048/https/cdn.discordapp.com/icons/794341861413355520/a_36f54b448066c33bb40e09c89a695f73.gif")

    await ctx.send(embed=embed)

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
    announce.set_thumbnail(url="https://images-ext-1.discordapp.net/external/DKb6qWSNVPhR-E4lMc5e74W_2s7DsYNUnp6oM7jtxJA/%3Fsize%3D2048/https/cdn.discordapp.com/icons/794341861413355520/a_36f54b448066c33bb40e09c89a695f73.gif")
    await ctx.channel.send(embed=announce)

#####Moderação
@client.command() #Lista de jogadores banidos. 
@commands.has_permissions(administrator=True)
async def bans(ctx, option=0, nome=None, id=None):
    mycursor = db.cursor()
    if option==0:
        mycursor.execute('SELECT name, id FROM banidos')
        for x in mycursor:
          await ctx.channel.send(f'**Banido**:\n**ID**: {x[1]}\n**Nome**:{x[0]}')
        return
    if option==1:
        mycursor.execute(f'INSERT INTO banidos(name,id) VALUES(%s,%s)', (nome,id))
        db.commit()
        mycursor.execute('SELECT * FROM banidos')
        await ctx.channel.send(f'Jogador **{id} | {nome}** foi adicionado na lista de banidos.')
        print(f'{id} foi banido.')

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
    msg.set_thumbnail(url="https://images-ext-1.discordapp.net/external/DKb6qWSNVPhR-E4lMc5e74W_2s7DsYNUnp6oM7jtxJA/%3Fsize%3D2048/https/cdn.discordapp.com/icons/794341861413355520/a_36f54b448066c33bb40e09c89a695f73.gif")
    await canal.send(embed=msg)

@client.command()
@commands.has_permissions(administrator=True)
async def ip(ctx, *, ip=None):
    if not ip:
        await ctx.send('<@{}>, Especifique um endereço IP!'.format(ctx.message.author.id))
        return
    rsp = rq.get('http://ip-api.com/json/'+ip).json()
    if rsp['status'] == 'fail':
        embed=discord.Embed(color=0xFF0000)
        embed.add_field(name="❌ Falha na consulta", value="❓ Motivo: "+rsp['message'])
        embed.set_footer(text="Consulta: "+ip)
        await ctx.send(embed=embed)
        return
    embed=discord.Embed(color=0x00FFFF)
    embed.add_field(name="✅Status: "+rsp['status'], value=f"\n\n🌍Country: {rsp['country']} \n\n🌏CountryCode: {rsp['countryCode']} \n\n🔷Region: {rsp['region']} \n\n🔷Region Name: {rsp['regionName']} \n\n🔷City: {rsp['city']} \n\n🕑TimeZone: {rsp['timezone']} \n\n🏢ISP: {rsp['isp']}\n\n🏢ISP OrgName: {rsp['org']}\n\n🏢ISP MoreInfo: {rsp['as']}", inline=False)
    embed.set_footer(text="IP Solicitado: "+ip)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True) 
async def players(ctx):
    
    timenow = time.strftime("%H:%M")
    resp = rq.get('http://'+config.serverIP+'/players.json').json()
    total_players = len(resp)
    if len(resp) > 25:
        for i in range(round(len(resp) / 25)):
            embed = discord.Embed(title='FiveMBot Bot', description='Server Players', color=discord.Color.blurple())
            embed.set_footer(text=f'Total Players : {total_players} | FiveMBot | {timenow}')
            count = 0
            for player in resp:
                embed.add_field(name=player['name'], value='ID : ' + str(player['id']))
                resp.remove(player)
                count += 1
                if count == 25:
                    break
                else:
                    continue

            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='FiveMBot Bot', description='Server Players', color=discord.Color.blurple())
        embed.set_footer(text=f'Total Players : {total_players} | FiveMBot | {timenow}')
        for player in resp:
            embed.add_field(name=player['name'], value='ID : ' + str(player['id']))
        await ctx.send(embed=embed)

#comando de clear 
@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    if amount>100: 
        amount = 100
        await ctx.send(f"Você so pode apagar até {amount}.")
    else: 
        amount<=100  
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{amount} mensagens foram apagadas.")

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

@client.command(pass_context=True)
async def rename(ctx, member: discord.Member, *, newnick):
  await ctx.message.delete()
  await member.edit(nick=newnick)
  await ctx.channel.send(f'>>> Foi alterado o nome de {member.mention}')

client.run('')
