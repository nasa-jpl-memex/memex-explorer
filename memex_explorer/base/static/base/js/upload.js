    options = {
        url: "/{{ project.slug }}/upload_image",
        success:  function(file, response) {
             if (this.getUploadingFiles().length === 0
                 && this.getQueuedFiles().length === 0) {
                window.location.replace(response.album_path)}},
        failure: function(file, response) {
            alert(response);
        }
    }

    Dropzone.options.filedrop = options;
