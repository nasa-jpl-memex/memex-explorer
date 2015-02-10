$(document).ready(function(){
    var crawler = $('input[name="crawler"]');
    var nutch = $('#id_crawler_1');
    var crawl_model = $('#id_crawl_model');

    function on_crawler_change(){
        if (nutch[0].checked){
            crawl_model.prop("disabled", true);
        } else {
            crawl_model.prop("disabled", false);
        }
    }

    // In case the form is reloaded with ACHE set, fire once
    on_crawler_change();

    crawler.change(on_crawler_change);
});
