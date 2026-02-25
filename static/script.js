const orderForm = document.getElementById('orderForm');
const typeSelect = document.getElementById('type');
const priceGroup = document.getElementById('priceGroup');
const responsePanel = document.getElementById('responsePanel');
const responseContent = document.getElementById('responseContent');
const submitBtn = document.getElementById('submitBtn');

// Show/hide price fields based on order type
typeSelect.addEventListener('change', function() {
    const orderType = this.value;
    
    if (orderType === 'MARKET') {
        priceGroup.style.display = 'none';
        document.getElementById('price').required = false;
    } else if (orderType === 'LIMIT') {
        priceGroup.style.display = 'block';
        document.getElementById('price').required = true;
    }
});

// Handle form submission
orderForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(orderForm);
    const data = Object.fromEntries(formData.entries());
    
    // Convert symbol to uppercase
    data.symbol = data.symbol.toUpperCase().trim();
    
    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading"></span> Placing Order...';
    
    try {
        const response = await fetch('/api/place-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        // Show response panel
        responsePanel.style.display = 'block';
        
        if (result.success) {
            responseContent.innerHTML = `
                <div class="response-success">
                    <strong>SUCCESS: Order Placed</strong>
                    <div class="response-detail">
                        <p><strong>Order ID:</strong> ${result.data.orderId}</p>
                        <p><strong>Status:</strong> ${result.data.status}</p>
                        <p><strong>Symbol:</strong> ${result.data.symbol}</p>
                        <p><strong>Side:</strong> ${result.data.side}</p>
                        <p><strong>Type:</strong> ${result.data.type}</p>
                        <p><strong>Quantity:</strong> ${result.data.origQty}</p>
                        ${result.data.price ? `<p><strong>Price:</strong> ${result.data.price}</p>` : ''}
                        ${result.data.stopPrice ? `<p><strong>Stop Price:</strong> ${result.data.stopPrice}</p>` : ''}
                    </div>
                </div>
            `;
        } else {
            responseContent.innerHTML = `
                <div class="response-error">
                    <strong>ERROR: Order Failed</strong>
                    <div class="response-detail">
                        <p>${result.error}</p>
                    </div>
                </div>
            `;
        }
        
        // Scroll to response
        responsePanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
    } catch (error) {
        responsePanel.style.display = 'block';
        responseContent.innerHTML = `
            <div class="response-error">
                <strong>ERROR: Network Connection Failed</strong>
                <div class="response-detail">
                    <p>${error.message}</p>
                </div>
            </div>
        `;
    } finally {
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Place Order';
    }
});
