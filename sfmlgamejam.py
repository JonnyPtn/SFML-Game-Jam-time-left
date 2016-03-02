from sopel import module, config, trigger, db
from sopel.db import SopelDB
import re
import urllib
import datetime

@module.commands(r"timeleft")
def timeLeft(bot, trigger):
	timeleft = getTimeLeft()
	hours = timeleft.seconds//3600
	minutes = (timeleft.seconds % 3600) // 60
	seconds = timeleft.seconds % 60
	bot.reply(str(timeleft.days) + " days, %02d:%02d:%02d" % (hours, minutes, seconds) + " remaining!")

@module.interval(10)
def checkTimeLeft(bot):
	timeleft = getTimeLeft()
	hoursleft = timeleft.seconds//3600
	db = SopelDB(bot.config)
	lasthoursleft = db.get_nick_value(bot.nick,"hoursleft")
	if lasthoursleft is not hoursleft :	
		bot.say("Less than " + str(lasthoursleft) + " hours remaining!" ,"#sfmlgamejam")
		db.set_nick_value(bot.nick,"hoursleft",hoursleft)

def getTimeLeft() :
	page = urllib.urlopen("https://sfmlgamejam.com/jams/2")
	regexpattern = "RemainingTime = (\d+)"
	reg = re.compile(regexpattern)
	results = re.findall(reg,page.read())
	timeleft = datetime.timedelta(seconds = float(results[0]))
	return timeleft

