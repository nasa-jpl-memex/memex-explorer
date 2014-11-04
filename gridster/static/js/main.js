      var gridster, static_grid;

      $(function(){
        gridster = $(".gridster ul").gridster({
          widget_base_dimensions: [310, 350],
          widget_margins: [5, 5],
          //resize.enabled: true,
          //helper: 'clone'
        }).data('gridster');
      });
