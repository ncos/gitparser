# gitparser
Get pull request statistics for 'infosec' project

- **pygithub.py** - looks for occurances of text specified in *PATTERN* variable in all .tex files in current directory, replaces the text found with the one specified in *REPLACEMENT* variable, than makes a separate branch and commits changes there. The name of the branch - value of *HASH* variable + number (*CURRENT_ID*). This script is also able to delete or reset branches (see commented lines at the bottom).  

- **pullscanner.py** - downloads all pull request information for a specified repository. Scans diffs and tries to label every pull request based on diff content. Check *REGEX* variable and *strdiff* function. 
  - The script will output verbose results to the screen, and dump *nickname - diif_link - label* for each pull request into **log.txt**.
  - Do not forget to specify your login data before using the script (see at the top of the file)
  
- logparser.py parses **log.txt** file to create an (arguably) beautiful statistics on the number of contributors making similar pull requests. The example of output is in the **stat.txt** file.
