# Created by leon at 28/12/2017

import wikipedia

# print(wikipedia.summary("Wikipedia"))
# wikipedia.set_lang('zh')
# print(wikipedia.search("中国"))

ny = wikipedia.page("模式识别")
print(ny.title)
print(ny.url)
print(ny.content)
print(ny.links[0])