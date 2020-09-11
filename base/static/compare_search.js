$(document).ready(function(){


                            $("#livebox").keyup(function(e){
                text= $("#livebox").val();


               $.ajax({
                method: "get",
                url: '/compare/{{apartment_name}}',

                success: function(rest){
                console.log(rest.apartment_name);
                var das= rest.apartment_name;
                  $.ajax({
                method: "post",
                url: '/property/compare/{{apartment_name}}/search',
                data: {text: text},
                success: function(res){

                var data = "<ul>";
                $.each(res,function(index,value){
                if(value.apartment_name != -1 ){

                data += '<li class="btn"><a  href="/property/compare/'+das+'/with/'+value.apartment_name+'"><span >'+value.apartment_name+' '+value.city+'  </span> | <span class="text-muted"> '+value.location+'  '+value.neighbourhood+'  </span></a> </li>';
               }
                });
                data += "</ul>";
                $("#datalist").html(data);
            }
          });
                }
                });
    });

                            });