$(document).ready(function() {
    
    var levelDimensions = JSON.parse(document.getElementById('level-dimensions').textContent);

    $('id_level').trigger('change');

    $('id_level').change(function() {
        var selectedLevel = $(this).val();

        $('id_dimension').empty();

        $.each(levelDimensions[selectedLevel], function(key, value) {
            $('id_dimension').append($('<option></option>').attr('value', key).text(value));
        });
    });
});
