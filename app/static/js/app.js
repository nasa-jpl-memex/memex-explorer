var CrawlForm, crawl_form,
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

CrawlForm = (function(_super) {
  var crawler, data_model;

  __extends(CrawlForm, _super);

  function CrawlForm() {
    return CrawlForm.__super__.constructor.apply(this, arguments);
  }

  crawler = $('#crawler');

  data_model = $('#data_model');

  CrawlForm.prototype.initialize = function() {
    return data_model.prop("disabled", true);
  };

  crawler.change(function() {
    if (crawler.val() === 'achenyu') {
      return data_model.prop("disabled", false);
    } else {
      return data_model.prop("disabled", true);
    }
  });

  return CrawlForm;

})(Backbone.View);

crawl_form = new CrawlForm;
