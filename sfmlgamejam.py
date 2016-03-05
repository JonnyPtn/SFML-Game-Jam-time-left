from sopel import module, config, trigger, db
from sopel.db import SopelDB
import re
import urllib
import datetime
import requests

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
	daysleft = timeleft.days
	db = SopelDB(bot.config)
	lastdaysleft = db.get_nick_value(bot.nick,"daysleft")
	if lastdaysleft is not daysleft :	
		bot.say("Less than " + str(lastdaysleft) + " Days remaining!" ,"#sfmlgamejam")
		db.set_nick_value(bot.nick,"daysleft",daysleft)

def getTimeLeft() :
	page = urllib.urlopen("https://sfmlgamejam.com/jams/2")
	regexpattern = "RemainingTime = (\d+)"
	reg = re.compile(regexpattern)
	results = re.findall(reg,page.read())
	timeleft = datetime.timedelta(seconds = float(results[0]))
	return timeleft

@module.commands("apicheck")
def apiRequest(bot, trigger):
	response = requests.post("https://sfmlgamejam.com/api/v1/jams")
	bot.reply(response.text)
