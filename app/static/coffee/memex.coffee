$ ->

    class CrawlFormView extends Backbone.View

        crawler: $ '#crawler'
        data_model: $ "#data_model"

        crawler.val().not('achenyu')


    crawl_form = new CrawlFormView
