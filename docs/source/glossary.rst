.. glossary::

   Service
      Anything that provides an external functionality not included directly in Memex Explorer.  Current examples include particular Docker containers holding specific versions of applications such as Tika, Kibana, Elasticsearch.

   Stack
      A particular set of Services in a working configuration.  An example might be a stack containing a Docker container providing Kibana 4.1.0 and another Docker container providing Elasticsearch 1.4.4.

   Instance
      A version of Memex Explorer running on a given host as well as its associated stack and databases.  An instance may have multiple projects.

   Project
      An in-Memex Explorer data and application warehouse.  Each project usually has its own copies of a stack.
      
   Domain Challenge
      A problem set like human trafficking, MRS, ebola.

   Skin
      A particular UI (Text, CSS, etc...) on a particular webpage for a domain challenge
      
   Celery
      A task manager build with Python, which manages several tasks in Memex Explorer, including the crawlers.
   
   Redis
      A key-value store database which is required by Celery to keep information about task history and task queues.
   
   Django
      A python web application framework. Django is the core of the memex explorer application.
      
   Crawl Space
      An application which provides service for crawling the web using Nutch or Ache.

