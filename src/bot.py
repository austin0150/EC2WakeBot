
from re import S
from this import d
import discord
from discord.ext import commands
import boto3.ec2
from botocore.exceptions import ClientError
import time

TOKEN = "YOUR_BOT_TOKEN"
GUILD = "YOUR_GUILD_ID"

description = 'Bot that wakes the EC2 Instance'

intents = discord.Intents.default()
intents.members = True

# --- AWS Stuff

ec2 = boto3.client('ec2',
    region_name='us-east-1',
    aws_access_key_id='YOUR_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY'
  )
instance_id = "YOUR_INSTANCE_ID"

# ---

bot = commands.Bot(command_prefix='/', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def checkserver(ctx):
    """Checks the instance status"""
    result = await checkServerStatus()
    await ctx.send("Instance is: " + result)
    

@bot.command()
async def startserver(ctx):
  """Starts the EC2 Instance"""
  try:
    print("Starting instace")
    response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)

    statusResponse = await checkServerStatus()
    count = 0
    while((statusResponse != 'Running') and (count != 5)):
      time.sleep(5)
      statusResponse = await checkServerStatus()
      count += 1

    print(response)
    await ctx.send("Started Instance")
  except ClientError as e:
    print(e)
    await ctx.send("Error Starting Instance")

async def checkServerStatus():
  response = ec2.describe_instance_status(
      Filters=[],
      InstanceIds=[instance_id],
      DryRun=False,
      IncludeAllInstances=True
      )

  status = (response['InstanceStatuses'])[0]['InstanceState']['Name']
  return status
  

bot.run(TOKEN)