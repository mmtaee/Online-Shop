
  $( document ).ready(function(){
      $('#message').fadeIn('slow', function(){
         $('#message').delay(4000).fadeOut();
      });
  });



  // $(function () {
  //     $('#finalize').on('click', function () {

  //       var id_list = [];
  //       var quantity_list = [];

  //       $('.product-id').each(function () {
  //         var ID = $(this).text();
  //         id_list.push(ID);
  //       });

  //       $('.quantity').each(function () {
  //         var quantity = $(this).val();
  //         quantity_list.push(quantity);
  //       });

  //       $("#id").val(id_list.toString());
  //       $("#quantity").val(quantity_list.toString());
  //       $(".form").attr("visibility","visible");
  //       $("#finalize").hide();
  //       $("#checkout_button").show();

  //     });
  // });



$(".product-id").hide();

$(document).ready(function() {

/* Set rates + misc */
// var taxRate = 0.05;
var fadeTime = 300;

/* Assign actions */
$('.product-quantity input').change( function() {
  updateQuantity(this);
  var cquantity =  $(this).parent().children('.quantity').val();
  var cname = $(this).parent().siblings('.product-removal').children('.remove-product').attr('id');
  var cvalue = $(this).parent().siblings('.product-removal').children('.remove-product').val();
  var d = new Date();
  d.setTime(d.getTime() + (24*60*60*1000));
  var expires = "expires=" + d.toGMTString();
  document.cookie = cname + "=" + [cvalue , cquantity] + ";" + expires + ";path=/";
});

$('.product-removal button').click( function() {
  removeItem(this);
  var cookie = $(this).parent().siblings('.product-details').children('.product-title').html().toString();
  document.cookie = cookie +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
});

/* Recalculate cart */
function recalculateCart()
{
  var subtotal = 0;

  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseInt($(this).children('.product-line-price').text().replace(/,/g, ''));
  });

  /* Calculate totals */
  // var tax = subtotal * taxRate;
  // var total = subtotal + tax + shipping;

  var total = subtotal;

  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-subtotal').html(subtotal.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,'));
    $('#cart-total').html(total.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,'));
    if(total == 0){
      $('.checkout').fadeOut(fadeTime);
      // $("#checkout_button").hide();
      // $("#finalize").hide();
      location.reload()
    }else{
      $('.checkout').fadeIn(fadeTime);
      $("#checkout_button").hide();
    }
    $('.totals-value').fadeIn(fadeTime);
  });
}

/* Update quantity */
function updateQuantity(quantityInput)
{
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseInt(productRow.children('.product-price').text().replace(/,/g, ''));

  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;

  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,'));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });
}

/* Remove item from cart */
function removeItem(removeButton)
{
  /* Remove row from DOM and recalc cart total */
  var productRow = $(removeButton).parent().parent();

  productRow.slideUp(fadeTime, function() {
    productRow.remove();
    recalculateCart();
  });
}
});
