import re


generic_urls = ["https://www.genericdomain.com/abc/def/1290aodwb23-ghi.img", 
				"https://www.genericdomain.com/ab-c/31287bdwakj-jkl.img", 
				"https://www.genericdomain.com/19unioawd02-jkl.img"
			]

# .*/  means find URL part upto last '/'
# ?! (negative lookahead)
# (?!.*/) means discard everything upto last '/' and work with rest
# (?!.*/).+ means match everything after last '/'
# ((?!.*/).+).*- means match upto '-' and after '/'
# ?= (positive lookahead)
# (?=((?!.*/).+).*-) means work with (lookahead) the left part (positive) of previous match
# (?=((?!.*/).+).*-).+  means match all characters from previous lookahead
pattern = re.compile(r"(?=((?!.*/).+).*-).+")


for url in generic_urls:
	print(pattern.search(url).group(1))