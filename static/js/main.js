document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Add to cart
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', () => {
            const id = button.dataset.id;
            const name = button.dataset.name;
            const price = parseFloat(button.dataset.price);
            const item = cart.find(item => item.id === id);
            if (item) {
                item.quantity++;
            } else {
                cart.push({ id, name, price, quantity: 1 });
            }
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCart();
        });
    });

    // Update cart display
    function updateCart() {
        const cartItems = document.querySelector('#cart-items');
        if (cartItems) {
            cartItems.innerHTML = '';
            let total = 0;
            cart.forEach(item => {
                total += item.price * item.quantity;
                const div = document.createElement('div');
                div.className = 'cart-item';
                div.innerHTML = `${item.name} x${item.quantity} - $${(item.price * item.quantity).toFixed(2)}`;
                cartItems.appendChild(div);
            });
            document.querySelector('#cart-total').textContent = total.toFixed(2);
            document.querySelector('#cart-data').value = JSON.stringify(cart);
        }
    }

    updateCart();
});