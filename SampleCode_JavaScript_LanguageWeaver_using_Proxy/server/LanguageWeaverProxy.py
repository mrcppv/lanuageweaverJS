#!/usr/bin/env python
import base64
import web

import LanguageWeaverTranslator
import LanguageWeaverUtil

LanguageWeaverTranslator.Init(
	'https://api.languageweaver.com',
# replace the next two lines with your own client id/secret
	'1234567890abcdefghij1234567890abcdefghij',
	'1234567890abcdefghij1234567890abcdefghij1234567890abcdefghij',
	'eng',
	'fra',
	'generic',
	True
	)


urls = (
	'/translate/(.+)/(.+)/(.+)', 'translate_text'
)

app = web.application(urls, globals())

class translate_text:
	def GET(self, text, src, trg):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Content-Type', 'text/plain')
		decoded = str(base64.b64decode(text), 'utf-8')
		LanguageWeaverTranslator.SetLanguages(src, trg);
		translation = LanguageWeaverTranslator.TranslateText(decoded)
		encodedBytes = bytes(translation, 'utf-8');
		encodedStr = base64.b64encode(encodedBytes);
		return encodedStr;

if __name__ == '__main__':
	app.run()