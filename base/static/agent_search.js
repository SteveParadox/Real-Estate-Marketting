$(document).ready(function(){
    $("#livebox").keyup(function(e){
                text= $("#livebox").val();
            console.log(text);

               $.ajax({
                method: "post",
                url: '/search/agent',
                data: {text: text},
                success: function(res){

                var data = "<ul>";
                $.each(res,function(index,value){
                if(value.first_name != -1 ){

                data += '<li class="btn"><a  href="profile/'+value.first_name+'/'+value.last_name+'"><span >'+value.first_name+' '+value.last_name+'  </span> | <span class="text-muted"> '+value.email+'  '+value.phone_no+' </span></a> </li>';
               }
                });
                data += "</ul>";
                $("#datalist").html(data);
            }
          });
          });
          });
