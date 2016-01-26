# Suggestions for code improvement

Improvement suggestions including commit sha so you can cherrypick and replay the review process if you like.


## Don't put binary files under version control

**commit** 9e80119

* Add a .gitignore file so you don't have to think about accidently commiting non source code to your repo


## Code style: PEP8

**commit** fff84ac

Python uses PEP8 code style convention. It won't change the behaviour of your code but it will increase readability and consistency. Check the internet for guides. Use a PEP8 (or flake8) plugin in your editor so your code gets checked on save.


## Don't put logic in \_\_main\_\_

**commit** c41d8bd

Put all logic into their own function or class so you can easily reuse it and your script now becomes usable from the command line as well as from other scripts importing it as a module.

I removed the Qgis trick at the end. It's a nice quirk but doesn't really belong in this script. What if someone is calling your script remotely? It will throw an exception while actually the script ran just fine. You confuse error handling of calling scripts.


## Refactor main function places_to_shape()

**commit** 6406c5a

You have a nice function for saving the shapefile, why didn't you also make a function for reading the txt file? Your line of thought is good but not always consistent.

Don't support two syntaxes: comma delimited and newline. Just go for newline for consistency and flexibility. Then you can easily extend the input format into eg csv adding a column(s). Don't add complexity to your program when don't really need to.

Assign the txt filename to a variable.

Use the `.strip()` functione once.

You see the main function looks a lot cleaner now. Reading our source became independent of the main loop allowing us to easily plug into different data sources: we just replace the `read_txt()` function. Moreover, we saved a call to `.strip()`.

I also added some poor mans debugging info by printing the place names and coordinates so I know what's going on. Up to your preference.


## Refactor get_latlng() function

**commit** 24f47d2

Provide an else for the if statement. It's very nice that you check the status code of the request. But what happens when the status code is not `200`?
Let's return `None` if something goes wrong.

Don't use the `+` operator to concatenate strings. Use a template with the `format()` function to have more control and flexibility.

Why not return the lat, lng as a dictionary, as the (zen of python)[http://www.thezenofpython.com/] suggests: `Explicit is better than implicit`.


## Refactor store_shape() function

**commit** 617c5b8

Don't put file handling, moving, renaming, copying logic into this function, pass the path as an argument.

Replace hard coded 'places.txt' in `remove_shape()` function call with variable name.

I added some comments to the main program.


## Add docstrings

**commit** 3e4813d

Actually, this shouldn't be something you do at the end but at the beginning. Before you write any code for a function, start with writing the docstring. It makes you think about the structure of the function. If you think the docstring is too complicated, probably your function design needs to be refactored.

Writing these docstrings made me find another refactoring candidate: hard coded layer name in `store_shape()` function.

I recommend using Google style docstrings, easy to remember and they look nice: http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html


## Summary

Looking at the code by now I find it more consistent, modular and easier to understand. We cleaned up the syntax, moved some logic around, let functions be responsible for 1 thing only, replaced hard coded assumptions with varriables and added docstrings so our future self still knows what we meant with all those functions.

There's two things still bothering me though:

* We are looping over the `places` list twice
* The remove_shape() function somehow looks out of place

The bonus section below solves these issues.


## Bonus: know which libraries to use

**commit**

This really doesn't do anything to your program other than make it more readable and make your life easier. When you gain experience you will have your own favourite toolbelt of libraries for daily use. Don't worry about it for now.

what is nice is that we got rid of the double loop (and reduced the `store_shape()` from about 30 to 3 lines of code) and the `remove_shape()` function :).

**(requests)[http://docs.python-requests.org/en/latest/]** a famous library from Armin Ronacher. in this case, it doesn't really add much to the standard urrllib2. But please use it when doing HTTP requests, it will make your life less miserable.

**(shapely)[https://github.com/Toblerity/Shapely]** pythonic wrapper around the GEOS library, written by Sean Gillies.

**(fiona)[https://github.com/Toblerity/Fiona]** pythonic wrapper around the OGR library also written by Sean Gillies.
