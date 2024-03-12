# built in
import base64
import datetime
import json
import os
import sys
import time
import uuid

#3rd party
import requests

# from source
import LanguageWeaverUtil

def Init(server, user, password, source, target, flavor, useClientAuthentication):
	global _server
	global _useClientAuthentication
	global _user
	global _password
	global _source
	global _target
	global _flavor
	global _defaultHeader

	global _token
	global _tokenExpiry

	_server = server
	_useClientAuthentication = useClientAuthentication
	_user = user
	_password = password
	_source = source
	_target = target
	_flavor = flavor
	_defaultHeader = {}

	global _session
	_session = requests.Session()
	GetToken()

def SetLanguages(source, target):
	global _source
	global _target
	_source = source
	_target = target

## token handling
## it is expensive to create tokens, so buffer as long as possible

def GetToken():
	global _token
	global _tokenExpiry
	# create authorization header
	if (_useClientAuthentication):
		res = Execute('/token', 'POST', {'clientId':_user, 'clientSecret':_password})
	else:
		res = Execute('/token/user', 'POST', {'username':_user, 'password':_password})
	_token = LanguageWeaverUtil.GetNamedNode(res, 'accessToken')
	_tokenExpiry = LanguageWeaverUtil.GetNamedNode(res, 'expiresAt')
	_defaultHeader['Authorization'] = 'Bearer ' + _token;

	# optional: add a unique ID identifying your call. This can be sent to SDL support
	# in case of problems, to help identifying the data related to your call
	callId = "python-SampleCode-MyCompany-" + str(uuid.uuid4());
	_defaultHeader['Trace-ID'] = callId;

def VerifyToken():
	currentEpochTime = int(round(time.time() * 1000))
	remainingMilliseconds = _tokenExpiry - currentEpochTime
	remainingMilliseconds = 1
	# token no longer valid, refresh
	if (remainingMilliseconds < 5000): # give it 5 seconds to react
		GetToken();

## translation calls

def TranslateText(text):
	VerifyToken();
	res = UploadText(text);
	requestId = LanguageWeaverUtil.GetNamedNode(res, 'requestId')
	translationRes = WaitForTranslation(requestId)
	return LanguageWeaverUtil.GetNamedNode(translationRes, 'translation')[0]

def TranslateFile(inpath, outpath):
	VerifyToken();
	res = UploadFile(inpath)
	requestId = LanguageWeaverUtil.GetNamedNode(res, 'requestId')
	translationRes = WaitForTranslation(requestId)
	f = open(outpath, "wb")
	try:
		bytes = f.write(translationRes)
	finally:
		f.close()

## REST calls

def UploadText(text):
	parameters = {'input': [text], 
		'sourceLanguageId': _source, 
		'targetLanguageId' : _target,
		'model' : _flavor
		};
	return Execute('/mt/translations/async/', 'POST', parameters);


def UploadFile(path):
    # requests will generate a multipart/formdata under the hood
	command = "/mt/translations/async";
	payload = {
		'sourceLanguageId': _source, 
		'targetLanguageId' : _target,
		'model' : _flavor,
		'inputFormat' : LanguageWeaverUtil.GetFileType(path)
		};
	files = {'input': (os.path.basename(path), open(path, 'rb'), 'application/octet-stream')}
	return ExecuteFormData(command, payload, files)


def WaitForTranslation(id):
	state = 'UNKNOWN'
	while (state.lower() != 'done'): # check for 'fail' to handle errors
		res = Execute('/mt/translations/async/' + id, 'get', None)
		state = LanguageWeaverUtil.GetNamedNode(res, 'translationStatus')
	return Execute('/mt/translations/async/' + id + '/content', 'get', None)


def Execute(command, method, payload):
	headers = _defaultHeader.copy();
	headers['Content-Type'] = 'application/json';
	try:
		if (method == 'POST'):
			res = _session.post(_server + '/v4' + command, json=payload, headers=headers)
		else:
			res = _session.get(_server +  '/v4' + command, headers=headers)
		# if OK or Accepted
		if (res.status_code != 200 and res.status_code != 202): 
			print (command + ' failed: ' + res.reason + ' - ' + res.content.decode('utf-8'))
		else:
			return res.content
	except Exception as e:
		print (str(e))


# for file upload, no content type in the header
def ExecuteFormData(command, payload, files):
	try:
		# note the different way of passing in the payload!
		res = _session.post(_server + '/v4' + command, data=payload, headers=_defaultHeader, files=files)
		# if OK or Accepted
		if (res.status_code != 200 and res.status_code != 202): 
			print (command + ' failed: ' + res.reason + ' - ' + res.content.decode('utf-8'))
		else:
			return res.content
	except Exception as e:
		print (str(e))

