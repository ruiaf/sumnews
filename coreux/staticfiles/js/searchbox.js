jQuery(document).ready(function($){

    $("#searchform").submit(function( event ) {
        $("#searchform").attr("action","/search/"+$("#searchboxquery").val())
    });

    $('#searchbutton').click(function(){  // bind the link's click event
        $("#searchboxsumbmit").click(); //click the hidden button
        return false; //return false to stop the link from doing anything
    });

});