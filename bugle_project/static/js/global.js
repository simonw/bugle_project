jQuery(function($) {
    console.log( 'bugle 1' );
    if (!$('form#blast').length) {
        return;
    }
    console.log( 'bugle 2' );
    $('form#blast input:first')[0].focus();
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
    
    console.log( 'bugle 3' );
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
    
    console.log( 'bugle 4' );
    var extended_blasts = $( '<span class="extended"></span>' );
    extended_blasts.append(include_code);
    extended_blasts.append(attach_file);
    $( '#blast-base' ).append( extended_blasts );
    $('#extended,#attach').hide();

    console.log( 'bugle 5' );
    $('#blasts .bundle > div').css('cursor', 'pointer').click(function () {
        $(this).parent().children('ol').toggle();
    });
});
