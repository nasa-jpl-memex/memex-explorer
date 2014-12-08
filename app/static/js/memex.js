var __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

$(function() {
  var CrawlFormView, crawl_form;
  CrawlFormView = (function(_super) {
    __extends(CrawlFormView, _super);

    function CrawlFormView() {
      return CrawlFormView.__super__.constructor.apply(this, arguments);
    }

    CrawlFormView.prototype.crawler = $('#crawler');

    CrawlFormView.prototype.data_model = $("#data_model");

    crawler.val().not('achenyu');

    return CrawlFormView;

  })(Backbone.View);
  return crawl_form = new CrawlFormView;
});
