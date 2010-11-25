jQuery(function($) {
    if (!$('form#blast').length) {
        return;
    }
    $('form#blast input:first')[0].focus();
    $('#extended,#attach').hide();
    var include_code = $('<a href="#" id="include-code">Include some code</a>');
    include_code.toggle(function() {
        $('#extended').show();
        $(this).addClass( 'active' );
        return false;
    }, function() {
        $('#extended textarea').val('');
        $('#extended').hide();
        $(this).removeClass( 'active' );
        return false;
    });
    var attach_file = $('<a href="#" class="attach-file">Attach a file</a>');
    attach_file.toggle(function() {
        $('#attach').show();
        $(this).addClass( 'active' );
        return false;
    }, function() {
        $('#attach').hide();
        $(this).removeClass( 'active' );
        return false;
    });
    var extended_blasts = $( '<span class="extended"></span>' );
    extended_blasts.append(include_code);
    extended_blasts.append(attach_file);
    $( '#blast-base' ).append( extended_blasts );

    $('#blasts .bundle > div').css('cursor', 'pointer').click(function () {
        $(this).parent().children('ol').toggle();
    });
});
