import discord
import requests
from discord.ext import commands

def is_token_valid(token):
    headers = {
        'Authorization': f'Bot {token}'
    }

    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    return response.status_code == 200

token = input("Please enter your discord bot's token: ")

if not is_token_valid(token):
    print("Invalid token. Please provide a valid bot token.")
else:
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='.', intents=intents)

    @bot.command(name='stats')
    async def stats_command(ctx, *args):
        user_input = " ".join(args)
        if not user_input:
            await ctx.send("Please provide a player name with the `.stats` command.")
            return
        API_URL = f"https://www.balldontlie.io/api/v1/players?search={user_input}"
        response = requests.get(API_URL)
        data = response.json()

        if data.get("data"):
            player_data = data["data"][0]
            player_name = f"{player_data['first_name']} {player_data['last_name']}"
            team = player_data["team"]["full_name"]
            height = f"{player_data['height_feet']}'{player_data['height_inches']}"
            weight = f"{player_data['weight_pounds']} lbs"
            position = player_data["position"]
            id = player_data["id"]
            BALL_STATS = f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={id}"
            balljsonified = requests.get(BALL_STATS)
            ballData = balljsonified.json()
            if ballData.get("data"):
                latest_season_data = ballData["data"][0]
                games_played = latest_season_data["games_played"]
                points = latest_season_data["pts"]
                assists = latest_season_data["ast"]
                rebounds = latest_season_data["reb"]            
                embed = discord.Embed(title=player_name, description=f"Player Stats for(this season + these are just averages per game) `{user_input}`", color=0x3498DB)
                embed.add_field(name="`Team`", value=team, inline=True)
                embed.add_field(name="`Height`", value=height, inline=True)
                embed.add_field(name="`Weight`", value=weight, inline=True)
                embed.add_field(name="`Position`", value=position, inline=True)
                embed.add_field(name="`Games Played`", value=games_played, inline=True)
                embed.add_field(name="`Points`", value=points, inline=True)
                embed.add_field(name="`Assists`", value=assists, inline=True)
                embed.add_field(name="`Rebounds`", value=rebounds, inline=True)            
                await ctx.send(embed=embed)
            else:
                await ctx.send("Ball data not found for this player.")
        else:
            await ctx.send("Player not found.")

    bot.run(token)
