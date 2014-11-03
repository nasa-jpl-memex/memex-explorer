Gridster Dashboard Interface
----------------------------

Gridster is a javascript library that allows the designer to set up a dashboard
interface with moving parts. It is simple and easy to use. The full documentation
can be found at (http://gridster.net/)

Here are the steps for getting gridster set up on your web development project. 

1.  Download gridster from (http://gridster.net/)
2.  Download the latest JQuery from (http://jquery.com/)
3.  Load the JQuery JavaScript file, the Gridster JavaScript file, and the Gridster
	CSS file into your HTML document. 
4.  Create a new file JavaScript file with the following code. The name can be 
	anything you want:

	```
	$(function(){ //DOM Ready
    	$(".gridster ul").gridster({
        	widget_margins: [10, 10],
        	widget_base_dimensions: [140, 140]
    	});
	});
	```

	This is where you will place your gridster options, which are available through
	the official documentation.
5.  Include the gridster HTML markup in your document:

	```
	<div class="gridster">
    	<ul>
    	    <li data-row="1" data-col="1" data-sizex="1" data-sizey="1"></li>
    	    <li data-row="2" data-col="1" data-sizex="1" data-sizey="1"></li>
    	    <li data-row="3" data-col="1" data-sizex="1" data-sizey="1"></li>
    	    <li data-row="1" data-col="2" data-sizex="2" data-sizey="1"></li>
    	    <li data-row="2" data-col="2" data-sizex="2" data-sizey="2"></li>
    	    <li data-row="1" data-col="4" data-sizex="1" data-sizey="1"></li>
    	</ul>
	</div>
	```

	Inside the li tags, place any HTML markup or JavaScript objects. 

	`data-row` and `data-col` correspond to the rows and columns of the grid layout.

	`data-sizex` and `data-sizey` alter the size of the grid in relation to the
	dimensions defined in the gridster JavaScript config file. 


