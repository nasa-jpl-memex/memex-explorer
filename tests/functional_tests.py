
# User stories

# Use Case #1: Researcher studies algorithms
# A researcher, Abby, is developing crawling and extraction algorithms. She needs to show how different crawls at
# different times are affecting the results. Furthermore, she wants to monitor how well her algorithms are doing during
# the crawl, so if things are completely wrong Abby is able to stop the crawl and fix the issue. Finally, Abby needs
# to set up crawlers and extractors, her code is working but currently a pretty manual process. To help build the
# crawlers and extractors, she needs to be able to connect to the existing examples but also have a visual crawl builder.

# - Abby navigates to the main page of the Memex Explorer.

# - She registers a new project.

# - In that new project she registers a new crawl with one of her models and seed list.

# - She starts the crawl.

# - She gets stats on the crawl.

# - She visualizes the results.

# - She downloads the results.

# Use Case #2: Analyst studies data from researchers
# An analyst, Juan, is looking for new leads for a domain specific search. He has three different crawlers,
# all from researchers with different crawling strategies. He wants to start these crawlers and see which parts of the
# web they are migrating to and how quickly they are getting relevant pages. Finally, Juan would like to build
# visualizations for his team showing the most relevant results.

# - Juan navigates to the main page of the Memex Explorer.

# - He registers a new project

# - He needs data for a specific domain, so he registers a new crawl (ache) by selecting the appropriate domain focused crawler
# with one of the models Abby has prepared for him and a seed list.

# - He starts the crawl

# - He gets stats on the crawl.

# - He visualizes the results.

# - He downloads the list of relevant urls for his domain search.

# Juan also wants to compare that focused crawler with a common crawl.

# - He registers a new common crawl (nutch) with the same seed list.

# - He runs the crawl

# - He gets stats on the crawl

# - He downloads the results

# - He indexes the images from the crawl

# Use Case #3: Investigator wants to find information on similar images
# An investigator, Jada, is searching for similar images to the ones she has been given. Jada wants to search for
# similar images and find other details about where those images are coming from.
# With the data from Juan that was indexed, Jada uploads her image and starts to find similar images, cameras linked to
# those images, web pages and information linked to those web pages.

# - Jada navigates to the main page of the Memex Explorer.

# - She navigates to Juan's project.

# - She navigates to the image space.

# - She uploads her image.

# - She gets back similar images.

# - She goes to a specific crawl image space and takes a look at the table by exif information

# - She finds an interesting image and clicks over it, to find similar images in the project.
