      var gridster;

      $(function(){
        gridster = $(".gridster ul").gridster({
          widget_base_dimensions: [200, 200],
          widget_margins: [6, 6],
          //helper: 'clone'
        }).data('gridster');

        gridster.$el
          .on('mouseenter', '> li', function() {
              gridster.resize_widget($(this), 2, 2);
          })
          .on('mouseleave', '> li', function() {
              gridster.resize_widget($(this), 1, 1);
          });

      });
