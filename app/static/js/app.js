var CrawlForm, crawl_form,
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

CrawlForm = (function(_super) {
  var config1, config2, crawler, data_model;

  __extends(CrawlForm, _super);

  function CrawlForm() {
    return CrawlForm.__super__.constructor.apply(this, arguments);
  }

  crawler = $('#crawler');

  data_model = $('#data_model');

  config1 = $('#config1');

  config2 = $('#config2');

  CrawlForm.prototype.initialize = function() {
    data_model.prop("disabled", true);
    return config2.prop("disabled", true);
  };

  crawler.change(function() {
    if (crawler.val() === 'achenyu') {
      return data_model.prop("disabled", false);
    } else {
      return data_model.prop("disabled", true);
    }
  });

  config1.change(function() {
    if (config1.val() === '') {
      return config2.prop("disabled", false);
    } else {
      return config2.prop("disabled", true);
    }
  });

  return CrawlForm;

})(Backbone.View);

crawl_form = new CrawlForm;
