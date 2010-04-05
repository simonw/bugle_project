jQuery(function($) {
    if (!$('form.blast').length) {
        return;
    }
    $('form.blast input:first')[0].focus();
    $('#extended,#attach').hide();
    var include_code = $('<a href="#">Include some code</a>');
    include_code.toggle(function() {
        $('#extended').show();
        return false;
    }, function() {
        $('#extended textarea').val('');
        $('#extended').hide();
        return false;
    });
    var attach_file = $('<a href="#">Attach a file</a>');
    attach_file.toggle(function() {
        $('#attach').show();
        return false;
    }, function() {
        $('#attach').hide();
        return false;
    });
    $('p.meta:first').append(' &middot; ');
    $('p.meta:first').append(include_code);
    $('p.meta:first').append(' &middot; ');
    $('p.meta:first').append(attach_file);
});
