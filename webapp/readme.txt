Authors:
Thomas Lund, Luke Poley 

Data: 
A scraped dataset of top 1000 rated games, as well as game id 0-5000 with overlap removed as pulled from BGG using BG1Tools. 

STATUS:
testingTL is working with all major systems. The only caviat is that mechanics tagging has had some persistant id missmatch somewhere in the data pipeline, 
as such mechanics may be missaligned with the labels presented on the dropdown. This is a known problem, seeming to depend on the exact database 
arrangment at the time of testing, but we have been unable to consistently locate and fix the problem. 

NOTES: 
We have had quite a time with version managment schenanigans. At one point the above problem was fixed. There have been quite a few 
problems that came from this, but I think we both have had sucess pulling this as a fresh repo and running it.
