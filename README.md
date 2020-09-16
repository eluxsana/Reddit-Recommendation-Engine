# Reddit_Recommedation_Engine
- Used Celery and RabbitMQ to asynchronously

Tasks To Do:
- Create a list of all the subreddits per category to a dataframe
- Use the list of reddits to classify which category your current reddit falls under
- If not part of the list what do we do??
- Go through each subreddit part of that category giving priority to your own first and go through the top go through the posts and compare the title
- If the titles yield similar accuracy then check out those article bodies and select top 10 recommendations of related articles
- Of the ones that give the top score 
- return the answer in text

Future Goals:
- Make it available as a Chrome Extension using Brython 
