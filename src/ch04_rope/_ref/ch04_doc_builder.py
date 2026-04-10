from src.ch04_rope.rope import create_rope


def get_ropeterm_description_md() -> str:
    amy_str = "amy"
    casa_rope = create_rope(amy_str, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    vacuum_rope = create_rope(clean_rope, "vacuum")
    appearance_rope = create_rope(casa_rope, "appearance")
    dirty_rope = create_rope(appearance_rope, "dirty")
    un_str = "UN"
    usa_str = "USA"
    texas_str = "Texas"
    usa_rope = create_rope(un_str, usa_str)
    un_usa_texas_rope = create_rope(usa_rope, texas_str)
    un_texas_rope = create_rope(un_str, texas_str)
    usa_texas_rope = create_rope(usa_str, texas_str)
    paris_str = "Paris"
    dallas_str = "Dallas"
    un_usa_texas_dallas_rope = create_rope(un_usa_texas_rope, dallas_str)
    un_usa_texas_paris_rope = create_rope(un_usa_texas_rope, paris_str)
    south_str = "The South"
    usa_south_rope = create_rope(usa_str, south_str)
    usa_south_texas_rope = create_rope(usa_south_rope, texas_str)
    france_str = "France"
    germany_str = "Germany"
    berlin_str = "Berlin"
    un_france_rope = create_rope(un_str, france_str)
    un_france_paris_rope = create_rope(un_france_rope, paris_str)
    un_germany_rope = create_rope(un_str, germany_str)
    un_germany_berlin_rope = create_rope(un_germany_rope, berlin_str)
    usa_un_rope = create_rope(usa_str, un_str)
    usa_un_france_rope = create_rope(usa_un_rope, france_str)
    usa_un_france_paris_rope = create_rope(usa_un_france_rope, paris_str)
    usa_un_germany_rope = create_rope(usa_un_rope, germany_str)
    usa_un_germany_berlin_rope = create_rope(usa_un_germany_rope, berlin_str)
    usa_texas_dallas_rope = create_rope(usa_texas_rope, dallas_str)
    usa_texas_paris_rope = create_rope(usa_texas_rope, paris_str)

    football_str = "Football"
    football_place_love_rope = create_rope(football_str, "Places that love football")
    football_place_love_midwest_rope = create_rope(football_place_love_rope, "Midwest")
    fb_love_thesouth_rope = create_rope(football_place_love_rope, "The South")
    fb_love_thesouth_texas_rope = create_rope(fb_love_thesouth_rope, texas_str)
    fb_no_love_rope = create_rope(football_str, "Places that do not love football")
    fb_no_love_france_rope = create_rope(fb_no_love_rope, france_str)
    fb_no_love_berlin_rope = create_rope(fb_no_love_rope, berlin_str)
    compelling_str = "Compelling things"
    not_compelling_str = "Non-compelling things"
    i_formation_str = "i formation"
    metaethics_str = "metaethics philosophy"
    baking_str = "baking"
    fb_compelling_rope = create_rope(football_str, compelling_str)
    fb_not_compelling_rope = create_rope(football_str, not_compelling_str)
    fb_i_formation_rope = create_rope(fb_compelling_rope, i_formation_str)
    fb_metaethics_rope = create_rope(fb_not_compelling_rope, metaethics_str)
    fb_baking_rope = create_rope(fb_not_compelling_rope, baking_str)
    fb_like_things_rope = create_rope(football_str, "Things I like to do")
    fb_recruit_rope = create_rope(
        fb_like_things_rope, "tell players to play at my favorite team"
    )
    fb_demps_rope = create_rope(fb_like_things_rope, "tell stories about Quetin Demps")
    # football_ ;Football;my favorite;tell players to play there;

    return f"""# Ropes


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
vacuum_rope = "{vacuum_rope}"
dirty_rope = "{dirty_rope}"
usa_texas_rope = "{un_usa_texas_rope}"
un_texas_rope = "{un_texas_rope}"
- **FirstLabel**: The first label in a RopeTerm. Example "UN" in "{un_usa_texas_rope}"

# Ropes that have the same FirstLabel can create meaning
Consider these 3 ropes: 
1. {un_usa_texas_rope} 
2. {usa_texas_rope}
3. {usa_south_texas_rope}

Each rope arrives at the concept of Texas in a different way and connotes something different. Now consider these UN FirstLabel :

Here each Rope has the FirstLabel "UN"
1. {un_france_paris_rope}
2. {un_germany_berlin_rope}
3. {un_usa_texas_dallas_rope}
4. {un_usa_texas_paris_rope}

vs 

Here each Rope has the FirstLabel "USA"
1. {usa_un_france_paris_rope}
2. {usa_un_germany_berlin_rope}
3. {usa_texas_dallas_rope}
4. {usa_texas_paris_rope}

The ropes give different meaning to the concepts of Dallas and Paris
"""
