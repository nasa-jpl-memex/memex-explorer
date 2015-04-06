#############
Crawler Guide
#############
Memex Explorer uses two crawlers, Ache and Nutch.

****************
Crawler Overview
****************
Memex explorer uses two crawlers, `Nutch`_ and `Ache`_. Both crawlers have their own unique resigns, and both use the data they collect in unique ways.

There is some commonality between the two, however. They both require a list of URLs to crawl, called a seeds list.

Creating a Seeds List
=====================
The common point between the two crawls is that they both use the same kind of seed list for their crawling. The seed list is comprised ot a list of urls separated by line breaks. Both Nutch and Ache use them in different ways, and the result you get directly from the crawlers is different for each of them. Here is a sample seed list:

.. code-block:: html

   http://www.reddit.com/r/aww
   http://gizmodo.com/of-course-japan-has-an-island-where-cats-outnumber-peop-1695365964
   http://en.wikipedia.org/wiki/Cat
   http://www.catchannel.com/
   http://mashable.com/category/cats/
   http://www.huffingtonpost.com/news/cats/
   http://www.lolcats.com/

Simply put, the seeds list should contain pages that are relevant to the topics you are searching. Both Nutch and Ache provide insight into the relevance of your seed list, but in different ways.

For the purposes of memex-explorer, the extenstion and name of your seeds list does not matter. It will be automatically renamed and stored according to the specifications of the crawler.

*****
Nutch
*****
`Nutch <http://nutch.apache.org/>`_ is developed by Apache, and has 

Nutch Dashboard
=======================

.. image:: _static/img/nutch_dashboard.png

****
Ache
****
Ache is developed by...

Ache Dashboard
======================

.. image:: _static/img/ache_dashboard1.png

.. image:: _static/img/ache_dashboard2.png

Building a Crawl Model
======================
This is how you build a crawl model.

