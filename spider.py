import urllib, urllib2, cookielib, re

NAME = 'xxx@xxx.com'
PWD = 'xxxxxxxx'
BASE_URL = 'https://oj.leetcode.com/'

def login(user, password):
	login_page = BASE_URL + 'accounts/login/'
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [
		('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko')
	]
	ptn = re.compile(".*name='csrfmiddlewaretoken' value='(.*)'.*")
	login_page_data = opener.open(login_page).read()
	csrfmiddlewaretoken = ptn.search(login_page_data).group(1)
	data = urllib.urlencode({"csrfmiddlewaretoken":csrfmiddlewaretoken, "login":user, "password":password})
	opener.addheaders.append(('Referer', 'https://oj.leetcode.com/accounts/login/'))
	opener.open(login_page, data)
	if opener == None:
		print 'Failed to login.'
		exit(-1)
	return opener
	
def get_links(opener):
	links = {}
	page_num = 1
	while True:
		print 'Getting submissions...page %d' % page_num
		submissions_url = BASE_URL + 'submissions/%d/' % page_num
		pattern = 'href="/problems/(.*)/".*\s*</td>\s*<td>\s*.*href="/(submissions/detail/[0-9]*/).*Accepted.*\s*</td>\s*<td>\s*(.*) ms'
		submissions = re.findall(pattern, opener.open(submissions_url).read())
		if not submissions:
			break
		for submission in submissions:
			key = submission[0]
			if not links.has_key(key) or int(links[key][1]) > int(submission[2]):
				links[key] = submission[1:3]
		page_num += 1
	return links
	
def save_accepted_code(opener, problem_name, url):
	print 'Querying %s...' % url
	pattern = "scope.code.*'([\s\S]*)';"
	code = re.findall(pattern, opener.open(url).read())[0].decode("unicode-escape")
	f = file('%s.txt' % problem_name, 'wb')
	f.write(code)
	f.close()
	print 'Saved %s.' % problem_name
	
if __name__ == '__main__':
	print 'Login...'
	opener = login(NAME, PWD)
	links = get_links(opener)
		
	for key in links.keys():
		save_accepted_code(opener, key, BASE_URL + links[key][0])