var csrftoken = $.cookie('csrftoken');
$(document).ready(function(){
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $("#tablaInscritos tr").clone().appendTo("#tablaInscritosCopia");
    $("#tablaInscritosCopia").fadeOut(0);
    $("#guardarIns").fadeOut(0);
    $('header, article').css({
      'padding':$("nav").css("height"),
      'color':'black'
    });

    $('#tablaInscritos tr').each(function(idx, el) {
        var $celda=$(el).find("td");
        var $usuario=$celda.eq(1);
        var $nombre=$celda.eq(2);
        var $apellido=$celda.eq(3);
        var $correo=$celda.eq(4);
        var opcion=0;
        if(idx>0){
            $celda.eq(5).append("<select><option></option></select>") 
            $('#cursos > div').each(function (id,el2) {
                $celda.eq(5).find("select").append("<option value='/guias/prg/"+$("#idcurso").val()+"/"+(id+1)+"/"+$celda.eq(5).find(".edita").attr('value')  +"'>Guia" + (id+1) +"</a></option>") ;   
            })
        }
        $celda.eq(5).find("select").on('change select',function () {
            window.location.replace(this.value);
            
        })
    });

    $("#agregar span").click(function () {
        $("#formulario").fadeIn("slow");
        $("input[name='op']").val("guardar");
    });
    $("#cancelar,#guardar").click(function () {
        $("#formulario").fadeOut("slow");
    });


    $("#modificarIns").click(function () {
        $(".edicion").attr("contenteditable","true");
        $("#guardarIns").fadeIn("slow");
    });
    $("#agregarIns").click(function () {
        var cont=0;
        for(i=1;i<=$("#cantAgregar").val();i++){
            $("#tablaInscritos tr").eq(1).clone().appendTo("#tablaInscritos");
            $("#tablaInscritos tr:last").find("td").html("");
            $("#tablaInscritos tr:last").find("td:last").html("eliminar");
            cont++;
        }
        if(cont==1){
            $("#tablaInscritos").append("<tr><td class=''></td><td contenteditable=false class='edicion usuario'></td><td contenteditable=false class='edicion nombre'></td><td contenteditable=false class='edicion apellido'></td><td contenteditable=false class='edicion email'></td><td><span class='' value='' id=''></span></td><td><span class='' id=''>Eliminar</span></td></tr>");
            $("#tablaInscritos tr:last").find("td").html("");
            $("#tablaInscritos tr:last").find("td:last").html("eliminar");
        }
    });
    $("#guardarIns").click(function () {
        $('#tablaInscritos tr').each(function(idx, el) {
            var $celda=$(el).find("td");
            var $usuario=$celda.eq(1);
            var $nombre=$celda.eq(2);
            var $apellido=$celda.eq(3);
            var $correo=$celda.eq(4);
            var opcion=0;
            if(idx>0){
                if($celda.eq(0).html()){
                    var $celda2=$("#tablaInscritosCopia tr").eq(idx).find("td");
                    if($celda2.eq(1).html()!=$usuario.html()||$celda2.eq(2).html()!=$nombre.html()||$celda2.eq(3).html()!=$apellido.html()||$celda2.eq(4).html()!=$correo.html()){
                            opcion=1;
                    }else{
                        opcion=0;
                    }
                }else{
                    opcion=2;
                }
                if(opcion!=0){
                    $.ajax('/guardaInscritos/', {
                          type : 'POST',
                          data : {opcion:opcion,
                          usuario:$usuario.html(),
                          nombre:$nombre.html(),
                          apellido:$apellido.html(),
                          correo:$correo.html(),
                          idcurso:$("#idcurso").val(),
                          idalumno:$celda.eq(6).find("span").attr("id")},
                          success: function(datos){
                            // alert(datos.message);
                            alert("Guardado");
                            location.reload();
                        }

                    });
                }
            }
        });
        $("#guardarIns").fadeOut("slow");
    });

    $(".eliminarIns").click(function () {
        if(confirm('Desea eliminar el curso "',"Advertencia")){
            $.ajax('/guardaInscritos/', {
                  type : 'POST',
                  data : {opcion:"3",
                  idcurso:$("#idcurso").val(),
                  idalumno:$(this).attr("id")},
                  success: function(datos){
                    alert(datos.message);
                    location.reload();
                }

            });
        }
    })
    

    $("#cursos .edita:contains(Editar)").click(function () {
        var selector=$(this).attr('name');
        var $divSel = $(".guia"+selector);
        var tema = $divSel.find("h3").text();
        var descripcion = $divSel.find("p").text();
        var numguia = $divSel.find("span").eq(0).text();

        $('#formulario input[name=numguia]').val(numguia);
        $('#formulario input[name=tema]').val(tema);
        $('#formulario textarea[name=descripcion]').text(descripcion); 
        $("#formulario").fadeIn("slow");
        $("#formulario input[name='op']").val("actualizar");
        $("#formulario input[name='id']").val(selector);

    });

    $("#cursos .edita:contains(Eliminar)").click(function () {
        var selector=$(this).attr('name');
        var $divSel = $(".guia"+selector);
        var nombre_curso = $divSel.find("h3").text();
        $("#formulario2 input[name='op']").val("eliminar");
        $("#formulario2 input[name='id']").val(selector);
        if(confirm('Desea eliminar el curso "' + nombre_curso + '"',"Advertencia"))
            $("#formulario2 form").submit();
    });
    
    
});



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}