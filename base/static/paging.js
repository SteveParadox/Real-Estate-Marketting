 $(document).ready(function(){
    $("#livebox").on("click",function(e){
    $('#count').html(function(i, val) {
{ return val*1+1 }
});
                 text=$("#count").html();
            console.log(text);

               $.ajax({
                method: "post",
                url: '/property/details/{{apartment.public_id}}',
                data: {text: text},
                success: function(res){
                console.log(res)
                     var data = "<ul>";
                $.each(res,function(index,value){
                if(value.name != -1 ){

                data += ' <li style="display: block;"> <div class="pd-review"> <div class="pr-item"><div class="pr-avatar"><div class="pr-pic"><img alt="" src="{{ url_for("static", filename="img/property/details/review/review-1.jpg") }}"></div>  <div class="pr-text"><h6>'+value.first_name+'</h6><span > '+value.email+' </span><span > '+value.date_comment+' </span>  </div>  </div><span class="text-muted"> '+value.message+' </span>  </div> </li></a>';
               }
                });
                data += "</ul>";
                $("#datalist").html(data);
                }
                });
                });
                });
