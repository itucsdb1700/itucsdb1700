function myFunction() {
    document.getElementById("Button1").innerHTML = "Hello World";
}
function myFunction2(){
  document.getElementById("Button2").innerHTML = "Hello World";
}
var InfoCard ='<div class="modal fade" id="myModal" role="dialog"> ' +
                  '<div class="modal-dialog">' +
                    '<div class="modal-content">' +
                      '<div class="modal-header">' +
                        '<button type="button" class="close" data-dismiss="modal">&times;</button>' +
                        '<h4 class="modal-title">Modal Header</h4>' +
                      '</div>' +
                      '<div class="modal-body">' +
                        '<form>' +
                          '<div class="form-group">' +
                            '<label for="exampleInputEmail1">Email address</label>' +
                            '<input class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" type="email">' +
                          '</div>' +
                          '<div class="form-group">' +
                            '<label for="exampleInputPassword1">Password</label>' +
                            '<input class="form-control" id="exampleInputPassword1" placeholder="Password" type="password">' +
                          '</div>' +
                          '<div class="form-group">' +
                            '<div class="form-check">' +
                              '<label class="form-check-label">' +
                              '<input class="form-check-input" type="checkbox"> Remember Password</label>' +
                            '</div>' +
                          '</div>' +
                        '</form>' +
                      '</div>'+
                      '<div class="modal-footer">' +
                        '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>' +
                      '</div>' +
                    '</div>' +
                  '</div>' +
                '</div>';







