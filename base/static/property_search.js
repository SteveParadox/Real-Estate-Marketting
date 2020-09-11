$(document).ready(function(){
    $("#cliq").on('click',function(e){
                text= $("#livebox").val();
            console.log(text);

               $.ajax({
                method: "post",
                url: '/search/apartment',
                data: {text: text},
                success: function(res){

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


