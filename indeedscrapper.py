from bs4 import BeautifulSoup # For HTML parsing
import urllib2 # Website connections
import re # Regular expressions
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
import pandas as pd # For converting results to a dataframe and bar chart plots
def text_cleaner(website):
	'''
	This function just cleans up the raw html so that I can look at it.
	Inputs: a URL to investigate
	Outputs: Cleaned text only
	'''
	try:
		site = urllib2.urlopen(website).read() # Connect to the job posting
	except: 
		return   # Need this in case the website isn't there anymore or some other weird connection problem 
	
	soup_obj = BeautifulSoup(site,"lxml") # Get the html from the site
	
	for script in soup_obj(["script", "style"]):
		script.extract() # Remove these two elements from the BS4 object
	text = soup_obj.get_text() # Get the text from this
	lines = (line.strip() for line in text.splitlines()) # break into lines
	chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
	def chunk_space(chunk):
		chunk_out = chunk + ' ' # Need to fix spacing issue
		return chunk_out  
	text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line
	# Now clean out all of the unicode junk (this line works great!!!)	
	try:
		text = text.decode('unicode_escape').encode('ascii', 'ignore') # Need this as some websites aren't formatted
	except:															# in a way that this works, can occasionally throw
		return														 # an exception	
	text = re.sub("[^a-zA-Z.+3]"," ", str(text))  # Now get rid of any terms that aren't words (include 3 for d3.js)
												# Also include + for C++
	text = text.lower().split()  # Go to lower case and split them apart
	stop_words = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now'] # Filter out any stop words
	text = [w for w in text if not w in stop_words]	
	text = list(set(text)) # Last, just get the set of these. Ignore counts (we are just looking at whether a term existed
							# or not on the website)	
	return text

keyword = 'data+scientist' # searching for data scientist exact fit("data scientist" on Indeed search)

joblist = ['http://www.indeed.com/jobs?q="', keyword, '"']

joblist_site = ''.join(joblist) # Merge the html address together into one string

print (joblist_site)
base_url = 'http://www.indeed.com'
html = urllib2.urlopen(joblist_site).read()
soup = BeautifulSoup(html, "lxml")
num_jobs_area = soup.find(id = 'searchCount').string.encode('utf-8') # Now extract the total number of jobs found
num_jobs_area
job_numbers = re.findall('\d+', str(num_jobs_area)) # Extract the total jobs found from the search result
if len(job_numbers) > 3: # Have a total number of jobs greater than 1000
	total_num_jobs = (int(job_numbers[2])*1000) + int(job_numbers[3])
else:
	total_num_jobs = int(job_numbers[2]) 
num_pages = total_num_jobs/10
job_descriptions1 = []
filename="indeed-"
count=1
for i in range(1,337): # Loop through all of our search result pages
	print ('Getting page', i)
	start_num = str(i*10) # Assign the multiplier of 10 to view the pages we want
	current_page = ''.join([final_site, '&start=', start_num])
	# Now that we can view the correct 10 job returns, start collecting the text samples from each
		
	html_page = urllib2.urlopen(current_page).read() # Get the page
		
	page_obj = BeautifulSoup(html_page, "lxml") # Locate all of the job links
	job_link_area = page_obj.find(id = 'resultsCol') # The center column on the page where the job postings exist
		
	job_URLS = [base_url + link.get('href') for link in job_link_area.find_all('a') if link.get('href') is not None] # Get the URLS for the jobs
		
	job_URLS = list(filter(lambda x:'clk' in x, job_URLS)) # Now get just the job related URLS
	for j in range(0,len(job_URLS)):
		final_description = text_cleaner(job_URLS[j])
		if final_description: # So that we only append when the website was accessed correctly
			job_descriptions1.append(" ".join(final_description))
			#sleep(1) # So that we don't be jerks. If you have a very fast internet connection you could hit the server a lot! 
		#print ('Done with collecting the job postings!')  
	if i%50==0:
		out=open(filename+str(count)+".csv","w")
		out.write("\n".join(job_descriptions1))
		out.close()
		count+=1
		job_descriptions1=[]