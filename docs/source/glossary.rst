########
Glossary
########

   Service
      Anything that provides an external functionality not included
      directly in Memex Explorer.  Current examples include particular
      applications such as DDT, Tika, Kibana, and Elasticsearch.

   Stack
      A particular set of Services in a working configuration.  This
      term is not used frequently in the documentation.

   Instance
      A version of Memex Explorer running on a given host as well as
      its associated stack and databases.  An instance may have
      multiple projects. 

   Project
      An in-Memex Explorer data and application warehouse.  Each
      project usually shares its application stack with other projects.
      
   Domain Challenge
      A problem set like human trafficking, MRS, ebola.

   Skin
      A particular UI (Text, CSS, etc...) on a particular webpage for a domain challenge
      
   Celery
      A task manager implemented in Python which manages several tasks in Memex Explorer, including the crawlers.
   
   Redis
      A key-value store database which used by Celery to keep information about task history and task queues.
   
   Django
      A python web application framework. Django is the core of the Memex Explorer application.
      
   Crawl Space
      Provides service for crawling the web using Nutch or Ache.

   Task Manager
      Manages the application tasks, like running crawls. Task manager is not available from the Memex Explorer GUI interface.
      
   
