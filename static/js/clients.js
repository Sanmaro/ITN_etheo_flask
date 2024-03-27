$(document).ready(function () {
    $("#table_clients").DataTable( {
        responsive: true,
        columnDefs: [
        { orderable: false, targets: 0 },
        { className: "dt-center", targets: "_all" }
        ],
        order: [[1, "asc"]],

        });
    });
        $("#table_clients").on('draw.dt', function(){
            let n = 0;
            $(".number").each(function () {
                    $(this).html(++n + ".");
        })
    })