import discord
import asyncio
from discord.ext import commands
import csv
#https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#discord-converters
client = commands.Bot(command_prefix='h~')

monsters = {}
monsterParts = {}
armorSkills = {}

with open('minfo.csv') as myFile: #detects the file for usage later
  lines=csv.DictReader(myFile, delimiter = ',')
  for line in lines:
    monsters[line['Name']] = line

with open('mparts.csv') as myFile:
    lines=csv.DictReader(myFile, delimiter = ',')
    for line in lines:
      monsterParts[line['Part']] = line

with open('skills.csv') as myFile:
    lines=csv.DictReader(myFile, delimiter = ',')
    for line in lines:
      armorSkills[line['Skill']] = line      

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Monster Hunter Rise'))
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event #client.event declares whenever something happens based on discord commands
async def on_member_remove(member):
    print(f'{member} has left the server.')

#help function
client.remove_command("help")
@client.group(invoke_without_command = True)

async def help(ctx):
    embed = discord.Embed(title = "Hinoa Help", description = f'Here is a list of my commands!')
    embed.add_field(name = "h~help", value = f"Returns a list of Hinoa Bot commands", inline = True)
    embed.add_field(name = "h~part 'monster part'", value = f"Returns information on searched monster part", inline = True)
    embed.add_field(name = "h~info 'monster name'", value = f"Returns information on searched mosnter", inline = True)
    embed.add_field(name = "h~skill", value = f"Returns all armor pieces with the desired skill", inline = True)
    embed.add_field(name = "h~boop 'username'", value = f"Boops your friend", inline = True)
    embed.add_field(name = "h~ping", value = f"Returns your current ping", inline = True)
    embed.add_field(name = "h~AraAra", value = f"You know what this means ya filthy weeb", inline = True)
    embed.add_field(name = "If you would liked to report a bug or suggest an improvement, please follow the link to the google form:", value = '[Feedback Form](https://forms.gle/VvDnCeVwqfAK4o7e7 )', inline = False)
    embed.set_footer(text = 'Hinoa Bot v0.3.0')
    await ctx.send(embed = embed)


@client.event #responds to funny question.
async def on_message(message): #easter egg function
    if client.user.id != message.author.id:
        if 'where can i get elder dragon blood?' in message.content:
            await message.channel.send('Where do you think? (￣^￣)')
            emoji = '🇩'
            await message.add_reaction(emoji)
            emoji = '🇺'
            await message.add_reaction(emoji)
            emoji = '🇲'
            await message.add_reaction(emoji)
            emoji = '🇧'
            await message.add_reaction(emoji)
            emoji = '🇾'
            await message.add_reaction(emoji)
    await client.process_commands(message)

@client.command()   #command function
async def ping(ctx):
    await ctx.send(f'Here\'s your ping: {round(client.latency * 1000)} ms')

@client.command()
async def boop(ctx, member : discord.Member):
    embed = discord.Embed(title = 'Boop!', description = f'{ctx.author.mention} booped {member.mention}!')
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Booped by {ctx.author.name}")
    await ctx.send(embed = embed)


@client.command() #returns information on searched monster part (SpreadSheet WIP)
async def part(ctx, *, part):
    part = part.title()
    await ctx.message.add_reaction('👍')
    matchingParts = []
    if part.find("Wyvern Gem") != -1 and part.find("Bird") == -1:
        for key in monsterParts:
            if key.find("Wyvern Gem") != -1 and key.find("Bird") == -1:
                matchingParts.append(key)
    elif part.find("Bird Wyvern Gem") != -1:
        for key in monsterParts:
            if key.find("Bird Wyvern Gem") != -1:
                matchingParts.append(key)
    else:
        for key in monsterParts:
            if key.find(part) != -1:
                matchingParts.append(key)
    
    if len(matchingParts) == 0:
        await ctx.send("Monster part not found.")
        return

    def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == "1️⃣" or "2️⃣" or "3️⃣" or "4️⃣" or "5️⃣"  or "6️⃣"  or "7️⃣"  or "8️⃣" or "9️⃣" or "➡️")
    length = len(matchingParts) #Optimized Code
    options = 0
    newLength = 0
    while(length > 1):
        choiceEmbed = discord.Embed(title = 'Multiple instances found.', description = f'I found multiple instances. Please choose which one you would like.')
        if(length > 9):
            options = round(length/2)
            while(options > 9):
                options = round(options/2)
            newLength = length - options
        else:
            options = length
        if(options >= 2):
            choiceEmbed.add_field(name = f'{matchingParts[0]}', value = 'Option 1', inline = False)
            choiceEmbed.add_field(name = f'{matchingParts[1]}', value = 'Option 2', inline = False)
        if(options >= 3):
            choiceEmbed.add_field(name = f'{matchingParts[2]}', value = 'Option 3', inline = False)
        if(options >= 4):
            choiceEmbed.add_field(name = f'{matchingParts[3]}', value = 'Option 4', inline = False)
        if(options >= 5):
            choiceEmbed.add_field(name = f'{matchingParts[4]}', value = 'Option 5', inline = False)
        if(options >= 6):
            choiceEmbed.add_field(name = f'{matchingParts[5]}', value = 'Option 6', inline = False)
        if(options >= 7):
            choiceEmbed.add_field(name = f'{matchingParts[6]}', value = 'Option 7', inline = False)
        if(options >= 8):
            choiceEmbed.add_field(name = f'{matchingParts[7]}', value = 'Option 8', inline = False)
        if(options == 9):
            choiceEmbed.add_field(name = f'{matchingParts[8]}', value = 'Option 9', inline = False)
        msg = await ctx.send(embed = choiceEmbed)
        if(options >= 2):
            await msg.add_reaction("1️⃣")
            await msg.add_reaction("2️⃣")
        if(options >= 3):
            await msg.add_reaction("3️⃣")
        if(options >= 4):
            await msg.add_reaction("4️⃣")
        if(options >= 5):
            await msg.add_reaction("5️⃣")
        if(options >= 6):
            await msg.add_reaction("6️⃣")
        if(options >= 7):
            await msg.add_reaction("7️⃣")
        if(options >= 8):
            await msg.add_reaction("8️⃣")
        if(options == 9):
            await msg.add_reaction("9️⃣")
        if(length > 9):
                await msg.add_reaction("➡️")
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
        except TimeoutError:
            await ctx.send('Oops! You ran out of time!')
        else:
            if str(reaction.emoji) == '1️⃣':
                part = matchingParts[0]
                break
            elif str(reaction.emoji) == '2️⃣':
                part = matchingParts[1]
                break
            elif str(reaction.emoji) == '3️⃣':
                part = matchingParts[2]
                break
            elif str(reaction.emoji) == '4️⃣':
                part = matchingParts[3]
                break
            elif str(reaction.emoji) == '5️⃣':
                part = matchingParts[4]
                break
            elif str(reaction.emoji) == '6️⃣':
                part = matchingParts[5]
                break
            elif str(reaction.emoji) == '7️⃣':
                part = matchingParts[6]
                break   
            elif str(reaction.emoji) == '8️⃣':
                part = matchingParts[7]
                break
            elif str(reaction.emoji) == '9️⃣':
                part = matchingParts[8]
                break
            elif str(reaction.emoji) == '➡️':
                while(options != 0):
                    del matchingParts[0]
                    options = options - 1
        msg = ""
        choiceEmbed.clear_fields       
        length = newLength

    monsterName = monsterParts[part]['Monster']
    targetReward = monsterParts[part]['Target Rewards']
    captureReward = monsterParts[part]['Capture Rewards']
    brokenReward = monsterParts[part]['Broken Parts']
    carveRewards = monsterParts[part]['Carve']
    dropRewards = monsterParts[part]['Drops']
    monsterRank = monsterParts[part]['Rank']
    embed = discord.Embed(title = f'{part}', description = f'Here\'s the info for {part} ({monsterRank} rank)!')
    embed.add_field(name = "Monster Name", value = f"\u2022 {monsterName}", inline = True)
    embed.add_field(name = "Target Reward", value = f"\u2022 {targetReward}", inline = True)
    embed.add_field(name = "Capture Reward", value = f"\u2022 {captureReward}", inline = True)
    embed.add_field(name = "Broken Parts Reward", value = f"\u2022 {brokenReward}", inline = True)
    embed.add_field(name = "Carves", value = f"\u2022 {carveRewards}", inline = True)
    embed.add_field(name = "Dropped Material", value = f"\u2022 {dropRewards}", inline = True)

    embed.set_footer(text = 'Hinoa Bot v0.3.0')
    await ctx.send (embed = embed)

@client.command() #returns information on searched mosnter
async def info(ctx, *, monster):
    await ctx.message.add_reaction('👍')
    monster.lower()
    monsterCheck = True
    def check(reaction, user):
        return user == ctx.author and (str(reaction.emoji) == "1️⃣" or "2️⃣")
    if monster == "narwa":
        msg = await ctx.send("Do you mean 1. Thunder Serpent Narwa or 2. Narwa the Allmother?")
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except TimeoutError:
            await ctx.send('timeout')
        else:
            if str(reaction.emoji) == '1️⃣':
                monster = "thunder serpent narwa"
            elif str(reaction.emoji) == '2️⃣':
                monster = "narwa the allmother"
    monster = monster.title()
    try:
        print(f'{monsters[monster]}')
    except KeyError: 
        monsterCheck = False
        print("Error! Monster isn't in list.")
    if monsterCheck == True:
        monsterElement = monsters[monster]['Elements']
        monsterAilment = monsters[monster]['Ailments']
        monsterFW = monsters[monster]['Fire Weakness']
        monsterWW = monsters[monster]['Water Weakness']
        monsterEW = monsters[monster]['Electric Weakness']
        monsterIW = monsters[monster]['Ice Weakness']
        monsterDW = monsters[monster]['Dragon Weakness']
        monsterSW = monsters[monster]['Sword Weakpoint']
        monsterSWDMG = monsters[monster]['SW Damage']
        monsterHW = monsters[monster]['Hammer Weakpoint']
        monsterHWDMG = monsters[monster]['HW Damage']
        monsterGW = monsters[monster]['Gun Weakpoint']
        monsterGWDMG = monsters[monster]['GW Damage']
        monsterPoison = monsters[monster]['Poison Weakness']
        monsterStun = monsters[monster]['Stun Weakness']
        monsterParalysis = monsters[monster]['Paralysis Weakness']
        monsterSleep = monsters[monster]['Sleep Weakness']
        monsterBlast = monsters[monster]['Blast Weakness']
        monsterExhaust = monsters[monster]['Exhaust Weakness']
        embed = discord.Embed(title = f'{monster}', description = f'Here\'s the info for {monster}!')
        embed.add_field(name = "Elements and Ailments", value = f"\u2022 Elements: {monsterElement}\n  \u2022 Ailments: {monsterAilment}", inline = True)
        embed.add_field(name = "Element Weaknesses", value = f"\u2022 Fire: {monsterFW}\u22C6\n  \u2022 Water: {monsterWW}\u22C6\n \u2022 Electric: {monsterEW}\u22C6\n  \u2022 Ice: {monsterIW}\u22C6\n  \u2022 Dragon: {monsterDW}\u22C6", inline = True)
        embed.add_field(name = "Sword Weakpoints", value = f"\u2022 Weakpoint: {monsterSW}\n  \u2022 Damage: {monsterSWDMG}", inline = True)
        embed.add_field(name = "Hammer Weakpoints", value = f"\u2022 Weakpoint: {monsterHW}\n  \u2022 Damage: {monsterHWDMG}", inline = True)
        embed.add_field(name = "Gun Weakpoints", value = f"\u2022 Weakpoint: {monsterGW}\n  \u2022 Damage: {monsterGWDMG}", inline = True)
        embed.add_field(name = "Ailment Weaknesses", value = f"\u2022 Poison: {monsterPoison}\u22C6 \n \u2022 Stun: {monsterStun}\u22C6 \n  \u2022 Paralysis: {monsterParalysis}\u22C6 \n  \u2022 Sleep: {monsterSleep}\u22C6 \n  \u2022 Blast: {monsterBlast}\u22C6 \n  \u2022 Exhaust: {monsterExhaust}\u22C6", inline = True)
        
        embed.set_footer(text = 'Hinoa Bot v0.3.0')
        await ctx.send(embed = embed)
    else:
        await ctx.send("Monster is not in list.")

@client.command() #user searches for a skill, and it returns all armor pieces with said skill and level along with a description.
async def skill(ctx, *, skill):
    await ctx.message.add_reaction('👍')
    skillName = armorSkills[skill]['Skill']
    skillDesc = armorSkills[skill]['Description']
    newDesc = ""
    period = '.'
    for i in range(0, len(skillDesc)):
        if skillDesc[i] == period:
            newDesc += ".\n"
        else:
            newDesc += skillDesc[i]
    embed = discord.Embed(title = f'{skillName}', value = f'Here\'s the description and armor pieces for {skillName}!')
    embed.add_field(name = f'Description', value = f'{newDesc}', inline = False)
    pieceParts = armorSkills[skill]['Armor Pieces']
    newPieces = ""
    comma = ','
    for i in range(0, len(pieceParts)):
        if pieceParts[i] == comma:
            newPieces += "\n"
        else:
            newPieces += pieceParts[i]
    embed.add_field(name=f'Armor Pieces', value =f'{newPieces}', inline=True)
    await ctx.send(embed=embed)

#must insert your own pin within the client.run() for the bot to run properly
#client.run('')
