jQuery(document).ready(function($){

    $("#editionform").submit(function( event ) {
        $("#editionform").attr("action","/edition/"+$("#edition").val())
    });

    $('#edition').change(function(){  // bind the link's click event
        $("#editionsumbmit").click(); //click the hidden button
        return false; //return false to stop the link from doing anything
    });

});