      var gridster;

      $(function(){
        gridster = $(".gridster ul").gridster({
          widget_base_dimensions: [500, 500],
          widget_margins: [6, 6],
          //helper: 'clone'
        }).data('gridster');
      });