var csrftoken = $.cookie('csrftoken');
var npaso = 1;
var altoMostrar=25;
var codigoEj="";

//### arrastrar elementos
var xInic, yInic;
var estaPulsado = false;
//######################


$(document).ready(listo);
//######################################################################################
function listo(){
  //################# Indicaciones #########################

  indicaciones();
  $("#guardar").click(guardarEnviar);
  $("#next").click(siguiente);
  $("#ant").click(anterior);

  //################# Editor de Texto ########################
  $('section').css({
    'paddingTop':$("nav").css("height"),
    'color':'black'
  });
  
  $('#play').click(compilarCodigo);
  
  $('#cerrar').click(cerrarConsola);

  editor();
  $("#pantalla").fadeOut("slow");


  var el = document.getElementById("v_consola");
  if (el.addEventListener){
      el.addEventListener("mousedown", ratonPulsado, false);
      el.addEventListener("mouseup", ratonSoltado, false);
      document.addEventListener("mousemove", ratonMovido, false);
  } else { //Para IE
      el.attachEvent('onmousedown', ratonPulsado);
      el.attachEvent('onmouseup', ratonSoltado);
      document.attachEvent('onmousemove', ratonMovido);
  }        
}


function indicaciones () {
  $("#indicaciones > div").fadeOut(0);
  $(".nombreGuia").fadeOut(0);
  $("#pasos #nombreGuia").html($(".nombreGuia").text());
  $("#indicaciones").find(".paso"+npaso).fadeIn("fast");
  $("#avance").html(npaso +"/" + $(".npasos").val());
  $("#texto").val("");
  $("#mostrar").html("");
  $("mostrar2").html("");
  $("#e_num").html("1");

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
  $.ajax('/codigoEjer/', {
      type : 'POST',
      data : {codigo:$("#texto").val(),guiaid:$("#guiaid").val(),nejercicio:npaso,idalumno:$("#idalumno").val()},
      success: function(datos){
      if (datos.estado=="correcto"){
        $("#texto").val(datos.message);
        coloreo();
        $("#estado").attr("class","ok")
      }
      else{
        $("#estado").removeAttr("class")
      }
      if(datos.estado=="error"){
        
      }
      
    }

  });
}


function guardarEnviar () {
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
  $.ajax('/guardarEnviar/', {
      type : 'POST',
      data : {codigo:$("#texto").val(),guiaid:$("#guiaid").val(),nejercicio:npaso},
      success: function(datos){
      if (datos.estado=="correcto"){
        alert(datos.message);
        indicaciones();
      }
      if(datos.estado=="error"){
        $("#logs").html(datos.codigo)
      }
      
    }

  });
  // if (npaso<$(".npasos").val()){
  //   npaso=npaso+1;
  //   indicaciones();
  // }
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

//######################################################################################
function cerrarConsola () {
  $('#v_consola').css({
      'display':'none'
    });
  $("#pantalla").fadeOut("slow");
}



function compilarCodigo() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $('#consola').html("");
    $('#logs').html("");
    $.ajax('/compilador/', {
        type : 'POST',
        // contentType : 'application/json',
        // dataType: 'json',
        data : {codigo:$("#texto").val()},
        success: function(datos){
        if (datos.estado=="correcto"){
          $("#pantalla").fadeIn("slow");
          $('#v_consola').css({
           'display':'inline'
          });
          codigoEj=datos.codigo;
          alert(codigoEj); 
	   eval(codigoEj);
           main();
          // //para multiple linea en un arreglo
          // for(i in datos.codigo){
          //   $('#consola').append(datos.codigo[i] + "<br>");
          // }
        }
        if(datos.estado=="error"){
          $("#logs").html(datos.codigo);
        }
        
      }

    });
}



function editor () {
  //########## editor coloreo
  $("#texto").bind('keydown',function(e){
    if ( e.which == 9 ) {
      e.preventDefault();
    }
  });
  $("#texto").on('change keyup paste input',coloreo);

  $("#texto").scroll(function () {
      $("#mostrar, #e_num").scrollTop($("#texto").scrollTop());
  });
}

function coloreo () {
  var newText = $("#texto").val()
  var newtext2=newText;  
      var endl = /\n/g;
      var espacio = /\s\s/g;
      var tabulador = /\t/g;
      var iostream = /\bcout\b|\bcin\b|\bendl\b/g;
      var reservada = /\bstring\b|\bnamespace\b|\bwhile\b|\bint\b|\bauto\b|\bconst\b|\bdouble\b|\bfloat\b|\bshort\b|\bstruct\b|\bunsigned\b|\bbreak\b|\bcontinue\b|\belse\b|\bfor\b|\blong\b|\bsigned\b|\bswitch\b|\bvoid\b|\bcase\b|\bdefault\b|\benum\b|\bgoto\b|\bregister\b|\bsizeof\b|\busing\b|\btypedef\b|\bvolatile\b|\bchar\b|\bdo\b|\bextern\b|\bif\b|\breturn\b|\bstatic\b|\bunion\b/g;
      var reservada1 =/\basm\b|\bdynamic_cast\b|\btry\b|\bbool\b|\bexplicit\b|\bnew\b|\btypeid\b|\bcatch\b|\bfalse\b|\boperator\b|\btemplate\b|\btypename\b|\bfriend\b|\bprivate\b|\bthis\b|\binline\b|\bpublic\b|\bthrow\b|\bvirtual\b|\bdelete\b|\bmutable\b|\bprotected\b|\btrue\b|/g;
      var especiales = /<|>|&/g;
      var directivas=/^#(.)*$/gm;
      var operadores=/\+|\-|\*|\=|\\|\/|\;/g;


      newText = newText.replace(especiales,function myFunction(x){
        if (x=="<")
          return "&lt";
        if (x==">")
          return "&gt";
        if (x=="&")
          return "&amp";
      });
      

      newText = newText.replace(operadores,function myFunction(x){return "<span class='operadores'>"+x+"</span>";});
    
      newText = newText.replace(iostream,function myFunction(x){return "<span class='iostream'>"+x+"</span>";});
      newText = newText.replace(reservada,function myFunction(x){return "<span class='palabrareservada'>"+x+"</span>";});
      newText = newText.replace(directivas,function myFunction(x){return "<span class='directivas'>"+x+"</span>";});   
      newText = newText.replace(endl,function () {
        return "<br>";
      });
      newText = newText.replace(tabulador,function myFunction(x){
        return " &nbsp&nbsp&nbsp&nbsp ";});
      newText = newText.replace(espacio,function myFunction(x){
        return "&nbsp ";});
      newText = newText.replace(espacio,function myFunction(x){
        return "&nbsp ";});
      
      $("#mostrar,#mostrar2").html(newText);
      $("#mostrar, #e_num").scrollTop($("#texto").scrollTop());
      if(altoMostrar!= parseInt($("#mostrar2").css("height"))){
        altoMostrar= parseInt($("#mostrar2").css("height"))
        var altoMostrar2=altoMostrar;
        var cont=0;
        while(altoMostrar2>0){
          cont+=1;
          if(cont%2==0){
            altoMostrar2-=26;
          }else{
            altoMostrar2-=25;
          }
        }
        $("#e_num").html("");
        for (var i = 1; i <= cont; i++) {
          $("#e_num").append(i+"<br>");
        };
      }
}


//############### Arrastrar elementos

function ratonPulsado(evt) { 
  //Obtener la posición de inicio
  xInic = evt.clientX;
  yInic = evt.clientY;    
  estaPulsado = true;
  //Para Internet Explorer: Contenido no seleccionable
  document.getElementById("v_consola").unselectable = true;
}

function ratonMovido(evt) {
  if(estaPulsado) {
      //Calcular la diferencia de posición
      var xActual = evt.clientX;
      var yActual = evt.clientY;    
      var xInc = xActual-xInic;
      var yInc = yActual-yInic;
      xInic = xActual;
      yInic = yActual;
      
      //Establecer la nueva posición
      var elemento = document.getElementById("v_consola");
      var position = getPosicion(elemento);
      elemento.style.top = (position[0] + yInc) + "px";
      elemento.style.left = (position[1] + xInc) + "px";
  }
}

function ratonSoltado(evt) {
  estaPulsado = false;
}

/*
* Función para obtener la posición en la que se encuentra el
* elemento indicado como parámetro.
* Retorna un array con las coordenadas x e y de la posición
*/
function getPosicion(elemento) {
  var posicion = new Array(2);
  if(document.defaultView && document.defaultView.getComputedStyle) {
      posicion[0] = parseInt(document.defaultView.getComputedStyle(elemento, null).getPropertyValue("top"))
      posicion[1] = parseInt(document.defaultView.getComputedStyle(elemento, null).getPropertyValue("left"));
  } else {
      //Para Internet Explorer
      posicion[0] = parseInt(elemento.currentStyle.top);             
      posicion[1] = parseInt(elemento.currentStyle.left);               
  }      
  return posicion;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
