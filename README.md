# BGG-owned-wishlist-analyzer
A Python program that scrapes some data from your BGG Owned and Wishlist pages and compiles an analysis on them.

## How to use
In the driver.py file you will find ``` urlOwnedListLinks = "<OWNED_LIST_LINK>" ``` and ``` wishlistLinks = "<WISHLIST_LINK>" ```. Replace ``` <OWNED_LIST_LINKS> ``` with the link to your Owned page, and replace ``` <WISHLIST_LINK> ``` with the link to your Wishlist page. Finally, run the program.

The output files containing the analysis will be generated in the output folder.

## Output files explained
** Owned_List.txt ** - contains all the games you own, and for each one it writes its type, mechanics, categories and families. <br />
** Owned_Split.txt ** - sorts all your owned games by category, type, mechanic and family. <br />
** Wishlist_List.txt ** - contains all the games you put on your wishlist, and for each one it writes its type, categories, mechanics and families. <br />
** Wishlist_Split.txt ** - sorts all your wishlisted games by category, type, mechanic and family. <br />
** Owned.xlsx ** - contains all the games you own and sorts them by their type, mechanics, categories and families. <br />
** Wishlist.xlsx ** - contains all the games you put on your wishlist and sorts them by their type, mechanics, categories and families. <br />
** Buylist.txt ** - sorts your wishlist by how many owend games' mechanics/categories you already have, and suggests the order in which you should buy games from your wishlist. <br />

The ** Buylist_Normal.txt **, ** Buylist_Indexed.txt **, ** Buylist_AvgToScore.txt ** and ** Buylist_2AvgToAvgToScore.txt ** do roughly the same thing as Buylist.txt, but each sorts your wishlist in different ways (by different criteria). Check them out if you want a different sorting of your wishlist.


