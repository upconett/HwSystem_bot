# <---------- Configuration Messages ---------->
mscf_MainToken = (
    "\n<1/5>\n"
	"Bot [TOKEN] is required to work with TelegramAPI.\n"
	"You can get it from: https://t.me/BotFather."
    )

mscf_LogToken = (
    '\n<2/5>\n'
	'Logger is minimal bot that outputs runtime info of your main bot.\n'
	'Get another [TOKEN] for this one.'
    )

mscf_Creators = (
    '\n<3/5>\n'
	'Bots need to know who their creators are!\n'
	'You need to provide [user_ids] (a sequence of numbers).\n'
	'You can learn your [id] from: https://t.me/getmyid_bot.'
    )

mscf_ApiHashId = (
    '\n<4/5>\n'
	'For certain bot functions to work properly you need to provide [api_hash] and [api_id]\n'
	'To get these follow the guide: https://core.telegram.org/api/obtaining_api_id'
    )

mscf_DBProperties = (
    "\n<5/5>\n"
	"Now it's time to initialize databases!\n"
	"The bot uses PostgreSQL and MongoDB so you need to set them running on your host.\n"
	"You have to specify [db_host], [db_user], [db_password] and [db_name].\n"
	"Required columns will be created automatically"
    )


# <---------- Error Messages ---------->
mscf_ErrorMainToken = (
    '\nERROR > [TOKEN] should be 46 chars long and looking like this:\n'
	'6933313572:dde6NYrts2jVfgpUdmEWynxliSdMnsVkfLM'
    )

mscf_ErrorCreators = '\nERROR > Your [id] should look like this: 3815494825'

mscf_ErrorApiId = '\nERROR > [api_id] should look like this: 12306494'

mscf_ErrorDBHost = (
	'\nERROR > [db_host] has to look like this:\n'
	'32.124.53.56 or be "localhost"'
    )