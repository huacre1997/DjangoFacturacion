// $(document).ready(function () {
//     $("#table").DataTable({
//       "lengthMenu": [
//         [10, 25, 50, -1],
//         [10, 25, 50, "All"]
//       ],
//       "language": {
//         "sSearch": "Buscar",
//         "emptyTable": "No hay datos disponibles para esta tabla",
//         "lengthMenu": "Mostrando _MENU_ entradas",
//         "loadingRecords": "Cargando...",
//         "processing": "Procesando...",
//         "zeroRecords": "No se encontraron resultados",
//         "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ entradas",
//         "infoEmpty":      "Mostrando 0 al 0 de 0 entradas",


//       },
//       "processing": true,
//       "order": [[ 0, 'asc' ]]
  
//     });
    
//   });
$(function() {

    var newHash      = "",
        $mainContent = $("#main-content"),
        $pageWrap    = $("body"),
        baseHeight   = 0,
        $el;
        
    $pageWrap.height($pageWrap.height());
    baseHeight = $pageWrap.height() - $mainContent.height();
    
    $("#accordionSidebar").delegate("a", "click", function() {
        window.location.hash = $(this).attr("href");
        return false;
    });
    
    $(window).bind('hashchange', function(){
    
        newHash = window.location.hash.substring(1);
        
        if (newHash) {
            $mainContent
                .find("#guts")
                .fadeOut(200);
        };
        
    });
    
    $(window).trigger('hashchange');

});