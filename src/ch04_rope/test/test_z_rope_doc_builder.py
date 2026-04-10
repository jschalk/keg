from src.ch00_py.file_toolbox import open_file
from src.ch04_rope._ref.ch04_doc_builder import get_ropeterm_description_md


def test_get_ropeterm_description_md_ReturnsObj():
    # ESTABLISH / WHEN
    ropeterm_description_md = get_ropeterm_description_md()

    # THEN
    assert ropeterm_description_md
    # print(ropeterm_description_md)
    expected_ropeterm_description_md = """# Ropes


# Introduction
Imagine all the things in the world and how they are related. Most things are not related to other things. But we as humans can create those connections. For example an apple that I eat and the moon seem completely seperate but we can create the connection arbitrarily: the apple is in an orchard, the orchard is loved by Sue, Sue loves the moon: "apple-orchard-things Sue loves-moon".

There are infinitely many connections that can be possibly experienced. When we're living the infinite is open to us but only some connections are actually experienced. In keg I define terms that are connections "Ropes". Imagine there is a rope connecting all things that are related to each other. Examples:
1. My cat and her food dish. 
2. A mountain as a concept and Wy'East (an actual mountain).
3. My cat and a cat you know.

There are infinitely many ways of defining a rope between to things:
1. My cat, and her food dish. 
2. My cat, all cats in the world, all cat dishs in the world, and her food dish. 
3. My cat, all the things she wants, and her food dish.

The way those ropes are made creates context that changes what exactly is being talked about. 
1. My cat, all basic cat food, and her food dish. 
2. My cat, all fancy cat food, and her food dish. 
In the first situation my cat's food has a conext of "basic" food., in the second situation the food context is "fancy". But its not explicit that the food dish has any food in it or what type it is. 

In the example of "My cat, all basic cat food, and her food dish." it is intuitive that there are three things (My cat) (all basic cat food) (her food dish) but its also reasonable to say there are two things: (My cat) (all basic cat food, her dish). To clearly express what things the rope is connecting to and through we must use separator characters. I call them "knots". (In Data Science they are call delimiters or separators) Every rope that connects two things can tie itself a knot and that knot defines the seperation and connection between two things. 
- Example with knot ";" and three things: ;My Cat;all basic cat food;her food dish;
- Example with knot ";" and two things: ;My Cat all basic cat food;her food dish;

Knots cannot be part of things' labels. Otherwise it becomes impossible to know what is a real knot and what is part of the thing's label. 
- ";" knot and 3 things: ;apples, oranges, pears;supermarket fruits;yogurt;
- "," knot and an undefined number of things: ,apples, oranges, pears,supermarket fruits,yogurt,

The first step to making connections is to define the knot. Then label things that never use the knot. 

# Definitions: 
- **Term**: Any sequence of letters. "a" or "apple" of "Apple is good"
- **LabelTerm**: A Term describing a thing. Examples: "apple", "December", "My grandmother", "Romeo, where art thou Romeo?" 
- **KnotTerm**: A special Term used to separate LabelTerms in a RopeTerm. Examples: ",", ";", "/", "\\", "sep"
- **RopeTerm**: A Term that has Labels seperated by Knots. 
Example RopeTerms with knot ";":
apple_moon_rope = ";apple;orchard;things Sue loves;moon;"
vacuum_rope = ";amy;casa;clean;vacuum;"
dirty_rope = ";amy;casa;appearance;dirty;"
usa_texas_rope = ";UN;USA;Texas;"
un_texas_rope = ";UN;Texas;"
- **FirstLabel**: The first label in a RopeTerm. Example "UN" in ";UN;USA;Texas;"

# Ropes that have the same FirstLabel can create meaning
Consider these 3 ropes: 
1. ;UN;USA;Texas; 
2. ;USA;Texas;
3. ;USA;The South;Texas;

Each rope arrives at the concept of Texas in a different way and connotes something different. Now consider these UN FirstLabel :

Here each Rope has the FirstLabel "UN"
1. ;UN;France;Paris;
2. ;UN;Germany;Berlin;
3. ;UN;USA;Texas;Dallas;
4. ;UN;USA;Texas;Paris;

vs 

Here each Rope has the FirstLabel "USA"
1. ;USA;UN;France;Paris;
2. ;USA;UN;Germany;Berlin;
3. ;USA;Texas;Dallas;
4. ;USA;Texas;Paris;

The ropes give different meaning to the concepts of Dallas and Paris
"""
    # print(ropeterm_description_md)
    assert ropeterm_description_md == expected_ropeterm_description_md
