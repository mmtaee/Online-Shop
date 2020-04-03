$("#validationServer013").change(function () {
var input = $("#validationServer013").val();
var model = $("#validationServer013").attr("model");;
    $.ajax({
      url: "/ajax/check_name/",
      data: {
        'input': input,
        // 'model': 'Manufacturer',
        'model': model,
      },
      success: function (response) {
                  if(!response["valid"]){
                    document.getElementById("validationServer013").setAttribute('class', 'form-control is-invalid');
                  }else{
                    document.getElementById("validationServer013").setAttribute('class', 'form-control is-valid');
                  }
                },
                error: function (response) {
                    document.getElementById("validationServer013").setAttribute('class', 'form-control');
                }
          });
});

$("#validationServer014").change(function () {
var input = $("#validationServer014").val();
    $.ajax({
      url: "/ajax/check_username/",
      data: {
        'input': input,
      },
      success: function (response) {
                  if(!response["valid"]){
                    document.getElementById("validationServer014").setAttribute('class', 'form-control is-invalid');
                  }else{
                    document.getElementById("validationServer014").setAttribute('class', 'form-control is-valid');
                  }
                },
                error: function (response) {
                    document.getElementById("validationServer014").setAttribute('class', 'form-control');
                }
          });
});
