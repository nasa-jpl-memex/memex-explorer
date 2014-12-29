var CrawlForm, crawl_form,
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

CrawlForm = (function(_super) {
  var crawler, data_model, model_options, model_radio, new_model;

  __extends(CrawlForm, _super);

  function CrawlForm() {
    return CrawlForm.__super__.constructor.apply(this, arguments);
  }

  crawler = $('#crawler');

  data_model = $('#data_model');

  new_model = $("#new_model");

  model_options = $('.model_options');

  model_radio = $(".model_radio");

  CrawlForm.prototype.initialize = function() {
    return model_options.prop("disabled", true);
  };

  crawler.change(function() {
    if (crawler.val() === "ache") {
      return model_options.prop("disabled", false);
    } else {
      return model_options.prop("disabled", true);
    }
  });

  model_radio.change(function() {
    if (model_radio.val() === "new") {
      new_model.prop("disabled", false);
      data_model.prop("disabled", true);
    }
    if (model_radio.val() === "existing") {
      new_model.prop("disabled", true);
      return data_model.prop("disabled", false);
    }
  });

  return CrawlForm;

})(Backbone.View);

crawl_form = new CrawlForm;
