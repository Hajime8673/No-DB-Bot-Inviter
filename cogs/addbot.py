import discord
import os
import config
from discord.ext import commands

class AddBot(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def addbot(self,ctx,id=None,*,desc=None):
        if id is None:
            return await ctx.send(f'Please make sure to follow this format, `{ctx.prefix}addbot [Bot ID] [Description and Prefix]`')
        if desc is None:
            return await ctx.send(f'Please make sure to follow this format, `{ctx.prefix}addbot [Bot ID] [Description and Prefix]`')
        try:
            bot = await self.client.fetch_user(int(id))
        except:
            return await ctx.send(f'You have provided an invalid bot id, please follow this, `{ctx.prefix}addbot [Bot ID] [Description and Prefix]`')
        if bot.bot is False:
            return await ctx.send('You have provided user id instead of bot id')
        if bot in ctx.guild.members:
            return await ctx.send(f"Bot {bot.name} already in this server!")
        emb = discord.Embed(title=f'New bot {bot.name} (ID: {bot.id})',color=0x7289da)
        emb.description = 'No Description is Provided' if desc is None else f"Added by: {str(ctx.author)}\nInvite: [Click Here to Invite](https://discord.com/oauth2/authorize?client_id={bot.id}&scope=bot&guild_id=720365448809545742)\n\nDescription: {desc[:1200]}"
        emb.set_footer(text=f'{bot.id} | {ctx.author.id}')
        try:
            chan = self.client.get_channel(config.invite_log_id)
            await chan.send(content='<@&{config.mention_on_submit_role_id}> New Invite Request!',embed=emb)
            await ctx.send('Submitted successfully, you will receive a dm once accepted or rejected.')
        except Exception as e:
            print(e)
            return await ctx.send('Something went went wrong, please try again later.')

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def accept(self,ctx):
        if ctx.message.reference is None:
            return await ctx.send(f'You need to reply to the message and type `{ctx.prefix}accept` to accept or `{ctx.prefix}reject` to reject.')
        m = ctx.message.reference
        try:
            e = await ctx.fetch_message(m.message_id)
            if e.author != ctx.me:
                return await ctx.send('Make sure it is my message...')
            e = await ctx.fetch_message(m.message_id)
            emb_dict = e.embeds[0].to_dict()
            try:
                bot = ctx.guild.get_member(int(emb_dict['footer']['text'].split('|')[0].replace(' ','')))
            except:
                return await ctx.send('Bot not found in the server, make sure you invite it first before accept/reject.')
            if bot is None:
                return await ctx.send('Bot not found in the server, make sure you invite it first before accept/reject.')
            try:
                if 840597403647082516 in [i.id for i in bot.roles]:
                    return await ctx.send('This bot is already approved!')
            except:
                pass
            try:
                owner = ctx.guild.get_member(int(emb_dict['footer']['text'].split('|')[1].replace(' ','')))
            except:
                return await ctx.send('Bot Owner left the server.')
            try:
                await owner.add_roles(ctx.guild.get_role(config.bot_owner_role_id))
            except:
                pass
            await bot.add_roles(ctx.guild.get_role(config.bot_role_id))
            try:
                await owner.send(f'Your bot ({bot.name}) has been approved!')
            except:
                pass
            return await ctx.send(f'{bot.name} has been approved succesfully!')
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description='Something went wrong: '+str(e)))

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def reject(self,ctx):
        if ctx.message.reference is None:
            return await ctx.send(f'You need to reply to the message and type `{ctx.prefix}accept` to accept or `{ctx.prefix}reject` to reject.')
        m = ctx.message.reference
        try:
            e = await ctx.fetch_message(m.message_id)
            if e.author != ctx.me:
                return await ctx.send('Make sure it is my message...')
            emb_dict = e.embeds[0].to_dict()
            try:
                bot = ctx.guild.get_member(int(emb_dict['footer']['text'].split('|')[0].replace(' ','')))
            except:
                pass
            try:
                if config.bot_role_id in [i.id for i in bot.roles]:
                    return await ctx.send('This bot is already approved!')
            except:
                pass
            try:
                owner = ctx.guild.get_member(int(emb_dict['footer']['text'].split('|')[1].replace(' ','')))
            except:
                return await ctx.send('Bot Owner left the server.')
            try:
                await owner.send(f"Your bot ({emb_dict['footer']['text'].split('|')[0].replace(' ','')}) has been rejected!")
            except:
                pass
            return await ctx.send(f"{emb_dict['footer']['text'].split('|')[0].replace(' ','')} has been rejected succesfully!")
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description='Something went wrong: '+str(e)))


def setup(client):
    client.add_cog(AddBot(client))