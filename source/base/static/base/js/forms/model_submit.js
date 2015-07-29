(function(){
  $(document).ready(function(){

    var addCrawlModelForm = $("#addCrawlModelForm");

    function updateModelFields(jsonResponse){
      var template = _.template($("#crawlFormModel").html())
      $("#id_crawl_model").append(template(JSON.parse(jsonResponse)))
    }

    function updateModelTable(jsonResponse){
      if (!$("#modelTable").length){
        var tableTemplate = _.template($("#modelTableBody").html());
        $("#modelTableDiv").append(tableTemplate(JSON.parse(jsonResponse)));
        $("#noModels").attr("hidden", true);
      } else {
        var template = _.template($("#modelTableItem").html());
        $("#modelTable > tbody:last-child").append(template(JSON.parse(jsonResponse)));
      }
    }

    addCrawlModelForm.submit(function(event){
      event.preventDefault();

      var xhr = ajaxForms.xhrFactory(window.location.href + "add_crawl_model/", "addCrawlModelForm");
      xhr.onreadystatechange = function(){
        if ((xhr.readyState == 4) && (xhr.status == 200)){
          updateModelFields(xhr.response);
          updateModelTable(xhr.response);
          $("#crawlModelModal").modal('hide');
        }
      }

      var formData = ajaxForms.toFormData(addCrawlModelForm);
      var model = $("#id_model")[0].files[0];
      var features = $("#id_features")[0].files[0];
      if (typeof model != 'undefined'){
        formData.append("model", model, model.name)
      }
      if (typeof model != 'undefined'){
        formData.append("features", features, features.name)
      }

      crispyFormErrors.clearErrors([
        "name",
        "features",
        "model",
      ]);

      xhr.send(formData);
    });

  });
})();
