/** $('#photo').on('change', function() {

            const size =
               (this.files[0].size / 1024 / 1024).toFixed(2);

            if (size > 4 || size < 2) {
                alert("File must be between the size of 2-4 MB");
            } else {
                $("#output").html('<b>' +
                   'This file size is: ' + size + " MB" + '</b>');
            }
        });
**/
/**
  function fileValidation() {
            var fileInput =
                document.getElementById('file');

            var filePath = fileInput.value;

            // Allowing file type
            var allowedExtensions =
                    /(\.jpg|\.jpeg|\.png|\.gif)$/i;

            if (!allowedExtensions.exec(filePath)) {
                alert('Invalid file type');
                fileInput.value = '';
                return false;
            }
            else
            {

                // Image preview
                if (fileInput.files && fileInput.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        document.getElementById(
                            'imagePreview').innerHTML =
                            '<img src="' + e.target.result
                            + '"/>';
                    };

                    reader.readAsDataURL(fileInput.files[0]);
                }
            }
        }
        **/

        $('input[type="file"]').each(function() {
    // get label text
    var label = $(this).parents('.form-group').find('label').text();
    label = (label) ? label : 'Upload File';

    // wrap the file input
    $(this).wrap('<div class="input-file"></div>');
    // display label
    $(this).before('<span class="btn">'+label+'</span>');
    // we will display selected file here
    $(this).before('<span class="file-selected"></span>');

    // file input change listener
    $(this).change(function(e){
        // Get this file input value
        var val = $(this).val();

        // Let's only show filename.
        // By default file input value is a fullpath, something like
        // C:\fakepath\Nuriootpa1.jpg depending on your browser.
        var filename = val.replace(/^.*[\\\/]/, '');

        // Display the filename
        $(this).siblings('.file-selected').text(filename);
    });
});

// Open the file browser when our custom button is clicked.
$('.input-file .btn').click(function() {
    $(this).siblings('input[type="file"]').trigger('click');
});