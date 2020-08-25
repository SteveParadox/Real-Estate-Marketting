$(document).ready(function(){
    $("#livebox,#livebox2,#livebox3, #livebox4").keyup(function(e){
                text= $("#livebox").val();
                 text2= $("#livebox2").val();
                  text3= $("#livebox3").val();
                  text4= $("#livebox4").val();
            console.log(text);



               $.ajax({
                method: "post",
                url: '/search',
                data: {text: text, text2:text2, text3:text3, text4:text4},
                success: function(res){

               console.log(res);
                var data = "<ul>";
                $.each(res,function(index,value){
                if(value.apartment_name != -1 ){

                data += '<li class="btn"><a  href="/property/detail/'+value.public_id+'"><span >'+value.apartment_name+' '+value.city+'  </span> | <span class="text-muted"> '+value.location+'  '+value.neighbourhood+'  </span></a> </li>';
               }
                });
                data += "</ul>";
                $("#datalist").html(data);
               }
          });
          });

  });

