import discord
import asyncio

prefix = "."
status = discord.Status.online
playing = ["Molotov", "Selfbot"]
client = discord.Client(intents=discord.Intents.all())

def check(message, command):
    if message.author.id == client.user.id and message.content.startswith(prefix + command):
        return True
    else:
        return False

@client.event
async def on_ready():
    print("Ready!")
    async def game(playing):
      await client.wait_until_ready()
      while not client.is_closed():
            for i in playing:
                await client.change_presence(status=status, activity=discord.Game(i))
                await asyncio.sleep(10)
    await game(playing)

@client.event
async def on_message(message):
    global prefix, status, playing

    if check(message, "도움말"):
        await message.reply(f"## Molotov Selfbot\n```{prefix}도움말 ㅣ 이 메세지를 보여줍니다.\n{prefix}접두사 [글자] ㅣ 접두사를 변경합니다.\n{prefix}상태 [온라인, 자리비움, 방해금지, 오프라인] ㅣ 온라인 상태를 변경합니다.\n{prefix}상메 [추가, 삭제, 초기화, 리스트] ㅣ 하는중 상태메세지를 변경합니다.\n{prefix}전술핵투하 [숫자] ㅣ 팀원까지 공격하는 전술핵을 투하합니다.```")

    if check(message, "접두사"):
        response = message.content[len(prefix)+4:]
        prefix = response
        await message.reply(f"> 성공적으로 접두사를 **{prefix}**로 변경했습니다.")

    if check(message, "상태"):
        response = message.content[len(prefix)+3:]
        if response == "온라인":
            status = discord.Status.online
        elif response == "자리비움":
            status = discord.Status.idle
        elif response == "방해금지":
            status = discord.Status.dnd
        else:
            response = "오프라인"
            status = discord.Status.offline
        await message.reply(f"> 성공적으로 상태를 **{response}**으로 변경했습니다.")

    if check(message, "상메"):
        try:
            response1 = message.content.split()[1]
            if response1 == "추가":
                response2 = message.content[len(prefix)+6:]
                playing.append(response2)
                await message.reply(f"> 성공적으로 **{response2}** 상메를 추가했습니다.")
            elif response1 == "삭제":
                try:
                    response2 = int(message.content[len(prefix)+6:])
                    await message.reply(f"> 성공적으로 **{playing[response2-1]}** 상메를 삭제했습니다.")
                    playing.pop(response2-1)
                except:
                    await message.reply("> 올바른 인수를 입력해주세요.")
            elif response1 == "초기화":
                playing = ["Molotov", "Selfbot"]
                await message.reply("> 상메를 초기화했습니다.")
            else:
                await message.reply(f"> 현재 상메 리스트는 **{playing}**입니다.")
        except:
            await message.reply("> 올바른 인수를 입력해주세요.")

    if check(message, "전술핵투하"):
        try:
            for i in range(int(message.content[len(prefix)+6:])):
                await message.channel.send("https://molotovserver.netlify.app/img/roh3.png")
            await message.reply("> 성공적으로 전술핵을 투하하였습니다.")
        except:
            await message.reply("> 올바른 인수를 입력해주세요.")

client.run("token", bot=False)
