to ensure that the application can be executed, make sure that all the packages within requirements.txt are installed properly

you can do this in 1 step:
pip install -r requirements.txt
(you might have to use cd to get into the folder then use ls to check)

current functions:
- recieves input ticker
- gives an output of buy/sell/hold based on analysis
- provides reasoning for each choice
- customtkinter displays modern gui
- backtesting (wip)
- uses weighted analysis to gather a centralized decision based off several indicators

future functions:
- advanced visualization/better gui
- displays prediction data over a graph
- interactive visualization of graphs/data
- user customization of info layout
- integration of more data sources
- possible data storage?
- (this is super far ahead) alerts for stock movements
