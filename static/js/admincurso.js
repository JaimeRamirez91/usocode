var csrftoken = $.cookie('csrftoken');
$(document).ready(function(){
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('header, article').css({
      'padding':$("nav").css("height"),
      'color':'black'
    });

    $("#agregar").click(function () {
        $("#formulario").fadeIn("slow");
        $("input[name='op']").val("guardar");
    });
    $("#cancelar,#guardar").click(function () {
        $("#formulario").fadeOut("slow");
    });
    
    

    $("#cursos .edita:contains(Editar)").click(function () {
        var selector=$(this).attr('name');
        var $divSel = $(".curso"+selector);
        var nombre_curso = $divSel.find("h3").text();
        var descripcion = $divSel.find("p").text();
        var ciclo = $divSel.find("span").eq(0).text();

        $('#formulario input[name=ciclo]').val(ciclo);
        $('#formulario input[name=nombre]').val(nombre_curso);
        $('#formulario textarea[name=descripcion]').text(descripcion); 
        $("#formulario input[name='op']").val("actualizar");
        $("#formulario input[name='id']").val(selector);

        $("#formulario").fadeIn("slow");

    });

    $("#cursos .edita:contains(Eliminar)").click(function () {
        var selector=$(this).attr('name');
        var $divSel = $(".curso"+selector);
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