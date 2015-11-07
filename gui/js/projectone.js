$(document).ready(function(){
    $("#queryform").submit(function(e){
        e.preventDefault();
        query = $("#search").val()
        $("#loadinganim").show()
         $.ajax({
                url: "http://localhost:8000/cgi-bin/cgi_search.py",
                type: "post",
                datatype: "html",
                data: {"query":query},
                success: function(response){
                        $("#loadinganim").hide()
                        $(".result").html(response);    
                }
            });
    });
});