class CrawlForm extends Backbone.View

    crawler = $ '#crawler'
    data_model = $ '#data_model'
    new_model = $ "#new_model"
    model_options = $ '.model_options'
    model_radio = $ ".model_radio"
 
    initialize: ->
        model_options.prop "disabled", true
        
    crawler.change ->
        if crawler.val() == "ache"
            model_options.prop "disabled", false
        else
            model_options.prop "disabled", true

    model_radio.change ->
        if model_radio.val() == "new"
            new_model.prop "disabled", false
            data_model.prop "disabled", true
        if model_radio.val() == "existing"
            new_model.prop "disabled", true
            data_model.prop "disabled", false

crawl_form = new CrawlForm
