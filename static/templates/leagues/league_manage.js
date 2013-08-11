$( function() {
    $('#participant_form').submit( function() {
        $.post( '/league_manage/' + $('#slug').text() + '/create_participant', $('form#participant_form').serialize() )
        return false;
    })
})
