$(document).ready(function () {
    $("#table_insurances").DataTable( {
        responsive: true,
        searching: false,
        columnDefs: [
        { orderable: false, targets: 0 },
        { className: "dt-center", targets: "_all" }
        ],
        order: [[5, "desc"]],

        });
    });
        $("#table_insurances").on('draw.dt', function(){
            let n = 0;
            $(".number").each(function () {
                    $(this).html(++n + ".");
        })
    })