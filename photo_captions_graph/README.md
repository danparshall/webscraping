# Social Graph of New York Social Diary

This was a miniproject I completed as part of the Data Incubator bootcamp.  This project isn't assigned any more, so I feel it's okay to post the code.

The overall project was to build a social graph by parsing the captions of photos taken at parties.  At the time there was an index at `http://www.newyorksocialdiary.com/party-pictures` (the website has a different structure now).  From there I downloaded all of the party pages, and then wrote a parser to identify the photo captions, parse them for the names of individuals, and then construct a weighted graph (with each shared photo increasing the weight between two individuals).


