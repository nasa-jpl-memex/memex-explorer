      var gridster, static_grid;

      $(function(){
        gridster = $(".gridster ul").gridster({
          widget_base_dimensions: [100, 100],
          widget_margins: [6, 6],
          //helper: 'clone'
        }).data('gridster');
      });
