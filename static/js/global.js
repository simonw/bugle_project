jQuery(function($) {
    if (!$('form.blast').length) {
        return;
    }
    $('form.blast input:first')[0].focus();
    $('#extended').hide();
    var a = $('<a href="#">Include some code</a>');
    a.toggle(function() {
        $('#extended').show();
        return false;
    }, function() {
        $('#extended textarea').val('');
        $('#extended').hide();
        return false;
    });
    $('p.meta:first').append(' &middot; ');
    $('p.meta:first').append(a);
});
