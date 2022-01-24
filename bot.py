import discord

TOKEN = 'OTM1MjM0NzI3NTQ2MzM5NDc5.Ye7rNg.Tlq1QDlcqgmei5PiODfOGgBlJ_g'

client = discord.Client(intents=discord.Intents.all())

counting_channel = 935235330221703189
command_channel = 783893061385977930

current_count = 0
previous_sender = None

rankings = {} # ID, count


@client.event
async def on_ready():
    print(f'{client.user} is up and running.')

    with open("savefile.txt", "r") as f:
        lines = f.readlines()
        current_count = int(lines[0])
        if len(lines) > 1:
            for line in lines[1:]:
                line = line.split(",")
                rankings[int(line[0])] = int(line[1])


@client.event
async def on_message(message):
    global current_count, rankings

    if message.author == client.user: return

    if message.channel.id == counting_channel:
        if message.author == previous_sender:
            await message.delete()
            return
            
        try:
            num = int(message.content, 16)
            if num == current_count + 1:
                current_count = num
                if message.author.id in rankings:
                    rankings[message.author.id] += 1
                else:
                    rankings[message.author.id] = 1
                save_rankings()
                return
        except Exception as e:
            print(f"Deleted \"{message.content}\" from {message.author.name} because: {e}")
        
        await message.delete()
        return
    
    if message.channel.id == command_channel:
        if "Kurius Executive" in [role.name for role in message.author.roles]:
            if message.content.startswith("hexcount set"):
                try:
                    current_count = int(message.content.split()[2], 16)
                    await client.get_channel(counting_channel).send(f"Set count to {message.content.split()[2]}")
                except Exception as e:
                    await message.channel.send(f"Error: {e}")
                return

        if message.content == "hexcount rankings":
            sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
            output = "Hexcount Rankings:\n"
            for i in range(min(len(rankings), 5)):
                username = client.get_user(sorted_rankings[i][0]).name
                output += f"{i+1}. {username} : {sorted_rankings[i][1]} hexcounts\n"
            await message.channel.send(f"```{output}```")
            return
        
    
def save_rankings():
    with open("savefile.txt", "w") as f:
        f.write(str(current_count))
        for key, value in rankings.items():
            f.write(f"\n{key},{value}")


    

if __name__ == '__main__':
    client.run(TOKEN)
