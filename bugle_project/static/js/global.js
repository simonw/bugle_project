var Bugle = {};

Bugle.Live = function (selector, url, channel) {
    var self = this;
    self.selector = $(selector);
    self.url = url;
    self.channel = channel;

    self.client = new Faye.Client(self.url);
    self.client.subscribe(self.channel, function (message) {
        self.handle(message);
    });
};

Bugle.Live.prototype.handle = function (message) {
    var blast;
    var insert = false;
    if (message.short) {
        blast = this.selector.children().eq(0);
        if (!blast.hasClass('bundle')) {
            blast = $('<li class="bundle"><div></div><ol></ol>').appendTo(
                this.selector
            );
            insert = true;
        }
        else {
            blast.children('div').text(', ' + blast.children('div').text());
        }
        blast.children('div').text(message.short + blast.children('div').text());
        blast.children('ol').append('<li>'+message.content+'</li>');

    }
    else {
        blast = $('<li>'+message.content+'</li>');
        insert = true;
    }
    if (insert) {
        blast.hide();
        this.selector.prepend(blast);
        blast.slideDown();
    }
};


jQuery(function($) {
    if (!$('form#blast').length) {
        return;
    }
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
    $('#extended,#attach').hide();

    $('#blasts .bundle > div').live('click', function () {
        $(this).parent().children('ol').toggle();
    });
});


