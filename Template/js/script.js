// Mở giỏ hàng nhỏ
let shoppingCart = document.querySelector('.small-cart')

document.querySelector('#cart-btn').onclick = () =>{
    shoppingCart.classList.toggle('active');
//     navbar.classList.remove('active');
}