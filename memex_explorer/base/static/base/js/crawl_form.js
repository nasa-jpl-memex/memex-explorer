$(document).ready(function(){
    var crawler = $('input[name="crawler"]');
    var nutch = $('#id_crawler_1');
    var crawl_model = $('#id_crawl_model');
    var model_div = $('#div_id_crawl_model');

    var on_crawler_change = function(){
        if (nutch[0].checked){
            crawl_model.prop("disabled", true);
            model_div.css('background-color', '#f5f5f5');
            model_div.css('margin', '0px');
            model_div.css('padding', '12px 8px');
            model_div.css('border-radius', '8px');
        } else {
            crawl_model.prop("disabled", false);
            model_div.css('background-color', '#ffffff');
        }
    }

    // In case the form is reloaded with ACHE set, fire once
    on_crawler_change();

    crawler.change(on_crawler_change);
});
