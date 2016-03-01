from sopel import module, config, trigger, db
import re
import urllib
import datetime

@module.commands(r"timeleft")
def getTimeLeft(bot, trigger):
	page = urllib.urlopen("https://sfmlgamejam.com/jams/2")
	regexSearch = "RemainingTime = (\d+)"
	pattern = re.compile(regexSearch)
	results = re.findall(pattern,page.read())
	timeleft = datetime.timedelta(seconds = float(results[0]))
	bot.reply(str(timeleft.days) + " days, " + str(timeleft.seconds//3600) + ":" + str((timeleft.seconds % 3600) // 60) + ":" + str(timeleft.seconds % 60))
