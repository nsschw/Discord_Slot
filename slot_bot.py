
import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import ffmpeg
import time
import json
import pandas as pd
from dotenv import load_dotenv
import os

#utility
from youtube import download_video

#for spin
from slot_machine import play
from plot_bild import plot_image

#for stats
from get_metrics import get_rarity, get_daily_big_hit



#Initialize Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix = "!", intents=intents)


async def deafen(ctx, usr:discord.Member, dauer):
    dauer = dauer * 60
    await usr.edit(mute=True)
    await asyncio.sleep(int(dauer))
    await usr.edit(mute=False)

       
@bot.command(name="free")
async def free_user_from_mute(ctx, usr:discord.Member):
    react_message = await ctx.send(f"Soll {usr.mention} wieder reden? \n Ab jetzt kann 15 Sekunden lang abgestimmt werden, ob {usr.mention} wieder reden darf")
    await react_message.add_reaction('✅')
    await react_message.add_reaction('❌')

    await asyncio.sleep(15)

    reactions_count = {}
    cache_msg = discord.utils.get(bot.cached_messages, id=react_message.id)
    reactions = cache_msg.reactions    
    for reaction in reactions:
        reactions_count[reaction.emoji] = reaction.count

    if (reactions_count['✅'] > reactions_count['❌']) and (reactions_count['✅'] + reactions_count['❌'] > 4):
        await usr.edit(mute=False)
        await ctx.send(f"{usr.mention} darf wieder reden")
    else:
        await ctx.send(f"{usr.mention} muss weiter seine Schnauze halten")  



@bot.command(name="spin")
async def foo(ctx, member: discord.Member=None):
    #check whether player is muted himself or player he wants to mute is already muted
    if ctx.author.voice == None:
        await ctx.message.reply("Komm doch online wenn du spielen willst.")
    elif ctx.author.voice.mute:
        await ctx.message.reply("Auf der stillen Treppe darf nicht gespielt werden.")    
    elif member.voice == None:
        await ctx.message.reply("{} ist doch garnicht da?".format(member.mention))
    elif member.voice.mute:
        await ctx.message.reply("{} ist doch schon gemuted.".format(member.mention))
    

    else:        
        #spin the slot_machine
        bild, reward = play()
        plot_image(bild, ctx.message.author)

        #save spin to log file
        spin_data = {"date": str(pd.Timestamp.now()), "user": str(ctx.message.author), "mute_target":str(member), "reward": reward}

        with open(f"Daten/log.jsonl", "a") as file:
            file.write(json.dumps(spin_data) + "\n")

        #return the  image and text + stats
        await ctx.send(file=discord.File('Bilder/Slot_Bilder/{}.png'.format(ctx.message.author))) #send image

        #send text + execute mute command
        if reward == 0:
            await ctx.send("{} hat 1 Minute stille Treppe für sich gewonnen!".format(ctx.author.mention))
            await deafen(ctx, ctx.message.author, 1)   

        else:
            await ctx.send(f"{ctx.author.mention} hat {reward} Minute(n) stille Treppe für {member.mention} gewonnen!")
            #check highscore
            big_hit_check = get_daily_big_hit(reward)
            if big_hit_check == 1:
                await ctx.send("Highscore! Das war der bisher höchste Hit.")
            #check probability
            if reward >= 8:
                await ctx.send("Die Wahrscheinlichkeit einen Hit wie diesen oder höher zu erzielen liegt bei {}%".format(get_rarity(reward)))
            await deafen(ctx, member, reward)    



@bot.command(name="play", help="Lädt das Youtube Video herunter und spielt es anschließend ab - einfach Leerzeichen und Link an den Befehl anhängen")
async def play_music(ctx):

    #get videolink and download video
    link = str(ctx.message.content).split()[1]  
    await ctx.send(f"Mooin Meister! Ich lade das Video noch kurz vor und komme dann.")
    video_name = download_video(link)    

    #join channel and play music
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio(f'Musik/{video_name}', executable="ffmpeg/bin/ffmpeg.exe")
    player = voice.play(source)    


@bot.command(name="disconnect")
async def leavevoice(ctx):
    for x in bot.voice_clients:
        await x.disconnect()




if __name__ == "__main__":
    load_dotenv()
    TOKEN =  os.getenv('TOKEN')
    bot.run(TOKEN)