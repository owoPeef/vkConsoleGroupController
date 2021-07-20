import os
import vk
import debug
import vk_api
import config
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token=config.vk_token, api_version=config.api_version)
lp = VkBotLongPoll(vk_session, config.group_id)
vkApi = vk_session.get_api()

session = vk.Session()
api = vk.API(session, access_token=config.vk_access_token, v='5.60', lang='ru')

debugger = debug.Logger()
debugger.directoryCreate()

def newPost():
	post_text = input("Post Text: ")
	if len(post_text) == 0:
		image_input = input("Image Location: " + os.getcwd() + "\\")
		try:
			getUploadServer("", image_input)
		except Exception as e:
			print("Len0 exception: " + str(e))
	else:
		post_split = str(post_text).split(" ")
		if post_split[len(post_split)-1] == "photo":
			image_input = input("Image Location: " + os.getcwd() + "\\")
			try:
				getUploadServer(post_text, image_input)
			except Exception as e:
				print("Len0Else Exception: " + str(e))
		else:
			post_info = api.wall.post(
				owner_id=-config.group_id,
				from_group=1,
				message=post_text
			)
			print("Post link: https://vk.com/wall-" + str(config.group_id) + "_" + str(post_info['post_id']))

def getUploadServer(message, file):
	photosServer = api.photos.getWallUploadServer(group_id=config.group_id)
	try:
		print(photosServer['upload_url'])
		response = requests.post(photosServer['upload_url'], files={'file': open(file, 'rb')})
		jsonResponse = response.json()
		photoSave = api.photos.saveWallPhoto(
			group_id=config.group_id,
			photo=jsonResponse['photo'],
			server=jsonResponse['server'],
			hash=jsonResponse['hash']
		)
		if len(message) != 0:
			post_info = api.wall.post(
				owner_id=-config.group_id,
				from_group=1,
				message=message,
				attachments="photo" + str(photoSave[0]['owner_id']) + "_" + str(photoSave[0]['id'])
			)
			print("Post link: https://vk.com/wall-" + str(config.group_id) + "_" + str(post_info['post_id']))
		if len(message) == 0:
			post_info = api.wall.post(
				owner_id=-config.group_id,
				from_group=1,
				attachments="photo" + str(photoSave[0]['owner_id']) + "_" + str(photoSave[0]['id'])
			)
			print("Post link: https://vk.com/wall-" + str(config.group_id) + "_" + str(post_info['post_id']))
	except Exception as e:
		return print("getUploadServer() exception: " + str(e) + "\n" + str(photoSave))
	return print(jsonResponse)

def setGroupTitle(title):
	try:
		vkApi.groups.edit(
			group_id=config.group_id,
			title=title
		)
		print("New group title: " + title)
	except Exception as e:
		print("Group title change failed: " + str(e))

def setGroupDescription(description):
	try:
		vkApi.groups.edit(
			group_id=config.group_id,
			description=description
		)
		print("New group description: " + description)
	except Exception as e:
		print("Group description change failed: " + str(e))

def setGroupScreenName(screen_name):
	try:
		vkApi.groups.edit(
			group_id=config.group_id,
			screen_name=screen_name
		)
		print("New group screen_name: " + screen_name)
	except Exception as e:
		print("Group screen_name change failed: " + str(e))

def getGroupInfo():
	try:
		groupInfo = vkApi.groups.getById(
			group_id=config.group_id,
			fields="description"
		)
		groupStatus = api.status.get(
			group_id=config.group_id
		)
		if groupInfo['groups'][0]['is_closed'] == 0:
			privacy = "\033[32mOpened\033[0m"
		if groupInfo['groups'][0]['is_closed'] == 1:
			privacy = "\033[90mClosed\033[0m"
		if groupInfo['groups'][0]['is_closed'] == 2:
			privacy = "\033[31mPrivate\033[0m"
		print("Name: «" + str(groupInfo['groups'][0]['name']) + "»\nDescription: «" + str(groupInfo['groups'][0]['description']) + "»\nStatus: «" + str(groupStatus['text']) + "»\nPrivacy: " + str(privacy) + "\nLink: https://vk.com/" + str(groupInfo['groups'][0]['screen_name']) + "\nAvatar Link: " + str(groupInfo['groups'][0]['photo_200']))
	except Exception as e:
		print("Failed to get group information: " + str(e))

yes = False

while True:
	yes = False
	action = input("Command: ")
	if action == "exit()":
		debugger.lineLog('Command called="' + str(action) + '"')
		yes = True
		exit()
	if action == "newPost()":
		debugger.lineLog('Command called="' + str(action) + '"')
		yes = True
		newPost()
	if action == "getUploadServer()":
		debugger.lineLog('Command called="' + str(action) + '"')
		yes = True
		getUploadServer()
	if action == "getGroupInfo()":
		debugger.lineLog('Command called="' + str(action) + '"')
		yes = True
		getGroupInfo()
	if action == "setGroupTitle()":
		debugger.lineLog('Command called="' + str(action) + '"')
		yes = True
		newTitle = input("New Title: ")
		if newTitle != "Deny":
			setGroupTitle(newTitle)
	if action == "setGroupDescription()":
		debugger.lineLog('Command called="' + str(action) + '"')
		yes = True
		newDesc = input("New Description: ")
		if newDesc != "Deny":
			setGroupDescription(newDesc)
	if action == "setGroupScreenName()":
		debugger.lineLog('Command called="' + str(action) + '"')
		yes = True
		newScreenName = input("New ScreenName: ")
		if newScreenName != "Deny":
			setGroupScreenName(newScreenName)
	if yes == False:
		debugger.lineLog('Command called="' + str(action) + '"')
		print("Command «" + str(action) + "» not found.")