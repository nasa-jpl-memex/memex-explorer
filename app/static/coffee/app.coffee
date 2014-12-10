class CrawlForm extends Backbone.View

    crawler = $ '#crawler'
    data_model = $ '#data_model'

    config1 = $ '#config1'
    config2 = $ '#config2'
 
    initialize: ->            
        data_model.prop "disabled", true
        config2.prop "disabled", true

    crawler.change ->
        if crawler.val() == 'achenyu'
            data_model.prop "disabled", false
        else
            data_model.prop "disabled", true

    config1.change ->
        if config1.val() == ''
            config2.prop "disabled", false
        else
            config2.prop "disabled", true

crawl_form = new CrawlForm
