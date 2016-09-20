var csrftoken = $.cookie('csrftoken');
var npaso = 1;
$(document).ready(function(){
    
    
    indicaciones();
    $("#guardar").click(guardarEnviar);
    $("#mostrar").click(mostrar);
    $("#navGuias span").eq(3).click(agregar);
    $("#navGuias span").eq(2).click(siguiente);
    $("#navGuias span").eq(0).click(anterior);
    $("#navGuias span").eq(4).click(eliminar);
    // $("#navGuias span").click(function () {
    //   alert($(this).html())
    // });
});

function indicaciones () {
  if($(".npasos").val()==0){
    var html1='<div class="paso1"><h2>Primera indicacion</h2><div class="indicacion">';
    html1+='<p>Todos los pasos para la indicacion1 del ejemplo1</p></div><div class= "procedimiento">';
    html1+='<p>Ejercicio1 que debe hacer para el ejemplo1</p></div><div class="evaluacion">';
    html1+='<input type="hidden" value=""></div></div>';
    $(".indicaciones").append(html1);
    $(".npasos").val(1);
    npaso=1;
  }
  $(".indicaciones > div").fadeOut(0);
  $(".nombreGuia").fadeOut(0);
  $("#pasos #nombreGuia").html($(".nombreGuia").text());
  $(".indicaciones").find(".paso"+npaso).fadeIn("fast");
  $("#avance").html(npaso +"/" + $(".npasos").val());  
  $("#navGuias span").eq(1).html("Ejercicio #"+npaso);
  $(".jqte-test").eq(0).val($(".indicaciones").find(".paso"+npaso).find(".indicacion").html());
  $(".jqte_editor").eq(0).html($(".indicaciones").find(".paso"+npaso).find(".indicacion").html());
  $(".jqte-test").eq(1).val($(".indicaciones").find(".paso"+npaso).find(".procedimiento").html());
  $(".jqte_editor").eq(1).html($(".indicaciones").find(".paso"+npaso).find(".procedimiento").html());
  $("#tituloejer").val($(".indicaciones").find(".paso"+npaso).find("h2").html());
}


function guardarEnviar () {
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
  //var bdatos={ejercicio:[]};

  // for(i=0;i<$(".npasos").val();i++)
  // {
  //   var num=i+1;
  //   bdatos.ejercicio.push(
  //     {num : num, tema:  $(".indicaciones > div").eq(i).find("h2").html()}
  //   );  
  // }

  $.ajax('/guardarEjercicios/', {
        type : 'POST',
        // contentType : 'application/json',
        // dataType: 'json',
        data : {codigo:$(".indicaciones").html(),
        numguia:$("#numguia").val(),
        curso:$("#curso").val()},
        success: function(datos){
          alert("guardado");
          
          
      }

    });
}

function siguiente () {
  if (npaso<$(".npasos").val()){
    npaso=npaso+1;
    indicaciones();
  }
}

function anterior () {
  if (npaso>1){
    npaso=npaso-1;
    indicaciones();
  }
}

function mostrar () {
  $(".indicaciones").find(".paso"+npaso).find("h2").html($("#tituloejer").val())
  $(".indicaciones").find(".paso"+npaso).find(".indicacion").html($(".jqte-test").eq(0).val());
  $(".indicaciones").find(".paso"+npaso).find(".procedimiento").html( $(".jqte-test").eq(1).val());
}
function agregar() {
  var html1='<div class="paso2"><h2>indicacion</h2><div class="indicacion">';
  html1+='<p>Todos los pasos para la indicacion del ejemplo</p></div><div class= "procedimiento">';
  html1+='<p>Ejercicio que debe hacer para el ejemplo</p></div><div class="evaluacion">';
  html1+='<input type="hidden" value=""></div></div>';
  $(".indicaciones").find(".paso"+npaso).after(html1)
  $(".npasos").val(parseInt($(".npasos").val())+1)
  npaso=npaso+1;
  for(i=0;i< parseInt($(".npasos").val());i++){
    $(".indicaciones > div").eq(i).removeClass().addClass("paso"+(i+1));
  }
  indicaciones();
}
function eliminar () {
  if(confirm("Desea eliminar el ejercicio")){
    $(".indicaciones").find(".paso"+npaso).remove();
    $(".npasos").val(parseInt($(".npasos").val())-1);
    if(npaso>parseInt($(".npasos").val()))
      npaso=npaso-1;
    for(i=0;i< parseInt($(".npasos").val());i++){
      $(".indicaciones > div").eq(i).removeClass().addClass("paso"+(i+1));
    }
    indicaciones();
  }
  
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}