repo: https://github.com/jschalk/keg

![keg logo](https://github.com/jschalk/keg/tree/main/logo/keg_64.png) keg

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


KEG Version 0.0.0

`keg` is a python library for listening to the climate of a community.

## 0.0 About keg

'keg' is a tool that helps me listen to the people important to me in my life.  I hope it can help you too. Let's assume I want to listen to you. If you give me a list of things that are important to you I want to be able to take your list, combine it with the lists of all the others I am about and get a output of a list of things I should do and metrics that describe my ability to do things . keg does this for all   

'keg' is based on the philosohpy of Emmanuel Levinas (1906-1995) as expressed in his book "Totality and Infinity: An Essay on Exteriority" (translated by Lingis, 1969) and taught to me by Jules Simon PhD (born 1959) Professor at The University of Texas at El Paso (UTEP). I took Jules's course "Levinas: Phenomenology of the Ethical" in 2014 and am still working through the implications. The most important idea that motivated keg was how Levinas describes murder as the act of not listening. It is painful to really listen, to listen in such a rope as to not know what is going to be said. To take in the suffering of the Other and bring them into myself and change myself in ropes that are by definition imaginable. Because if I could imagine them then they would not be a change. By definition I'm only listening if it changes me in ropes I can't predict. 

So how do I listen? keg has an engine for converting the declarations (as data) into pledge lists. How to input the data? The most accessible method is using excel sheets. 

# 0.0.1 "Moments" The foundation of keg
For Levinas all of reality is born from the face to face encounter. The same (me) welcomes the Other through the Face. The Face of the other tells me it's suffering and it's suffering becomes me. I then MOMENT to change who I am to ease that suffering. The suffering is infinitely deep and beyond my complete understanding so when I moment to respond to that suffering I am acting with confidence that I understand what the suffering is and that I know how to respond. That confidence stops the listening process, the Moment cuts the infinite into the finite and is the foundation for a world. When that Moment is created it can create a world. Worlds can hold a infinite amount of human experience. A small subset of that is logical systems. keg is uses programming to build that logic.

A Moment can create a world or change a current world. Each person can only make one moment at a time so a world that has been built by multiple moments implies each moment is from a different time. Keg indexs time by *spark_nums* with the assumption that *spark_num* is always an integer. A discrete indivisible unit of time. 

For keg all data must have *spark_num*, *spark_face*, and a rope, either *moment_rope* or *plan_rope*. These are the required keys.

  
## 0.1 Short introduction to keg excel sheets

`keg` is a python library for listening to the needs of my neighbors and in turn letting them know what I need. Needs can be expressed in Excel sheets that range in complexity from a simple five column single row (example below) to 10+ columns that include configuration options that are usually set to defaults. Each row is translated and used to build the "lynx" data set. Even sheet with a single row like the example 0.1.0 below can be processed by keg. 

# Input Example Excel file 0.1.0: fizz0.xlsx with sheet "br00000_buzz" 
| spark_num | spark_face | moment_rope | person_name | contact_name | tran_time | amount |
|-----------|-----------|-----------|------------|-----------|-----------|--------|
|    77     | Emmanuel  | OxboxDean |  Emmanuel  |    Dean   |    891    |  7000  |

When keg processes example 0.1.0 it creates a Moment labeled "OxboxDean" that contains persons Emmanuel and Dean and a single transaction of 7000 OxboxDean from Emmanuel to Dean. Here's a metric:
| moment_rope | person_name | moment_fund_amount | moment_fund_rank | moment_pledges |
|--------------|---------------|--------------------|------------------|--------------|
|  OxboxDean   |    Emmanuel   |       -7000        |         2        |       0      |
|  OxboxDean   |      Dean     |        7000        |         1        |       0      |


Output stance: emmanuel_stance.xlsx, sheet "br00000"
| spark_num | spark_face | moment_rope | person_name | contact_name | tran_time | amount |
|-----------|-----------|--------------|---------------|-----------|-----------|--------|
|    77     | Emmanuel  |   OxboxDean  |    Emmanuel   |    Dean   |    891    |  7000  |


<!-- # Input Example Excel file 0.1.2: fizz2.xlsx with sheet "br00000_buzz2" 
| spark_num | spark_face | moment_rope | person_name | contact_name | contact_cred_points | contact_debt_points |
|-----------|-----------|-----------|------------|-----------|---------------|---------------|
|    77     | Emmanuel  | OxboxDean |  Emmanuel  |    Dean   |      100      |      15       |
|    77     | Emmanuel  | OxboxDean |  Emmanuel  |  Emmanuel |       50      |      75       |
|    78     |    Sue    | OxboxDean |     Sue    |     Sue   |       2       |       7       |
|    78     |    Sue    | OxboxDean |     Sue    |     Sue   |       50      |      75       |

 -->

`keg` is a python library for listening to the climate of a community. Individual 
positions are aggregated by a listener into a coherant agenda that can include pledges 
to do and pledges of  of existence. Listening and acting on it.

A contact's agenda in the community is built by the the stared intreprtation of
1. Other contacts' agendas 
2. Their own independent agenda

Each agenda is saved as a JSON file. 

This is mostly a one man projeect. Femi has significantly helped. 

 
### 1.0 Installing `keg`

<!-- TODO: add dependencies -->

Future enhancement: `keg` can be installed using `pip`

<!-- TODO: Get pip install to function correctly

    pip install keg

If you have installed `keg` before, and you should ensure `pip` downloads the latest version (rather than using cache) you can use the follow ing commands:

    pip uninstall keg
    pip install --no-cache keg

-->

### 1.1 Hello 

<!-- TODO: Add simplest example

Should examples be found in a separate repository to ensure the `keg` repository stays 
relatively small, whilst still providing a thorough knowledgebase of code-samples, 
screenshots and elucidatory text.

-->

## 1.2 Notes about data structure

<!-- TODO: Add elucidations -->
base attributes vs reason attributess

PersonUnit objects

PersonUnit ContactUnit objects

PersonUnit GroupUnit objects

PersonUnit PlanUnit objects

PersonUnit PlanUnit hierarchical structure

PersonUnit PlanUnit AwardUnit objects

PersonUnit PlanUnit AwardLine objects

PersonUnit PlanUnit AwardHeir objects

PersonUnit PlanUnit AwardHeir objects

PersonUnit PlanUnit Reason CaseUnit objects

PersonUnit PlanUnit Reason CaseHeir objects

PersonUnit PlanUnit FactUnit objects

PersonUnit PlanUnit FactHeir objects1


## 1.3 Test-Driven-Development

keg was developed using Test-Driven-Development so every feature should have a test. 
Tests can be hard to comprehend. Some tests have many variables and can be hard to follow.

<!-- TODO: Add examples 
Should examples be in a separate repository to ensure the `keg` repository stays 
relatively small? (whilst still providing a thorough knowledgebase of code-samples, 
screenshots and elucidatory text.)
-->



## 2. License

<!-- TODO: Consider which license to pick -->


## 3. Acknowledgements

<!-- TODO: Consider which license to pick -->





<!-- TODO: Find out how to autopopulate the below modeled after the borb library
[![Corpus Coverage : 100.0%](https://img.shields.io/badge/corpus%20coverage-100.0%25-green)]()
[![Public Method Documentation : 100%](https://img.shields.io/badge/public%20method%20documentation-100%25-green)]()
[![Number of Tests : 615](https://img.shields.io/badge/number%20of%20tests-615-green)]()
[![Python : 3.8 | 3.9 | 3.10 ](https://img.shields.io/badge/python-3.8%20&#124;%203.9%20&#124;%203.10-green)]() 

[![Downloads](https://pepy.tech/badge/borb)](https://pepy.tech/projeect/borb)
[![Downloads](https://pepy.tech/badge/borb/month)](https://pepy.tech/projeect/borb)
-->


## Testing