from funcs import *

# ------- MAIN -------

start = timeit.default_timer()
print("Started the program")

# ADD THE LINK TO YOUR OWNED LIST PAGE BELOW
urlOwnedListLinks = "<OWNED_LIST_LINK>"

#ADD THE LINK TO YOUR WISHLIST PAGE BELOW
wishlistLinks = "<WISHLIST_LINK>"

writeFullPackage("Owned_List", "Owned_Split", "Wishlist_List", "Wishlist_Split", "Owned", "Wishlist", "Buylist", urlOwnedListLinks, wishlistLinks)

stop = timeit.default_timer()
print(f"Ended the program after: {stop - start} seconds.")