# eBay-Price-Graph
A Flask web app that when given an eBay search URL, uses BeautifulSoup to scrape the data and shows the user a Seaborn Boxplot graph on past sales.

link-form.html - The only HTML form on the web page. This is where users enter in their eBay URL

DashBoardFunctions.py - Functions created to web scrape eBay and create seaborn plots

WebApp.py - Where the flask webapp is initialized and contained. Dashboardfunctions.py is imported to scrape and create graphs
