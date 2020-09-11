$(document).ready(function(){
        var textx;
        var texty;
        var text4;

        $("#livebox").keyup( function(e){
             $("#livebox").val();

 });

    $(" #slider").on('input', function(e){
             $('#slider_value').html( $(this).val() );

 });



$("#slider2").on('input', function(e){
    $('#slider_value2').html( $(this).val() );
 });


      $("#select_val").change(function(){

        text4 = $("#select_val option:selected").val();
console.log(text4);


    });



    $("#cliq").on('click',function(e){
                    text= $("#livebox").val();

                  textx= $('#slider_value').html( );
                   texty= $('#slider_value2').html( );
                   console.log(textx);
                    console.log(texty);
                    console.log(text);
                    console.log(text4);

               $.ajax({
                method: "post",
                url: '/search',
                data: {text: text, textx:textx, texty:texty, text4:text4},
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





