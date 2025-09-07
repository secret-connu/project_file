document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------
    // 1. Withdraw confirmation popup
    // -------------------------------
    const withdrawForm = document.querySelector('form[action*="withdraw"]');
    if (withdrawForm) {
        withdrawForm.addEventListener('submit', (e) => {
            const amount = document.getElementById('amount').value;
            if (!confirm(`Are you sure you want to withdraw ₹${amount}?`)) {
                e.preventDefault(); // Stop form submission if user clicks Cancel
            }
        });
    }

    // -------------------------------
    // 2. Highlight inputs on focus
    // -------------------------------
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.style.borderColor = '#007bff'; // Blue border on focus
            input.style.boxShadow = '0 0 5px rgba(0,123,255,0.5)';
        });
        input.addEventListener('blur', () => {
            input.style.borderColor = ''; // Reset border
            input.style.boxShadow = '';
        });
    });

    // -------------------------------
    // 3. Hide success messages automatically
    // -------------------------------
    const msg = document.getElementById('success-message');
    if (msg) {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(() => msg.style.display = 'none', 500);
        }, 3000); // Hide after 3 seconds
    }

    // -------------------------------
    // 4. Button hover animation
    // -------------------------------
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
        btn.addEventListener('mouseover', () => {
            btn.style.transform = 'scale(1.05)';
            btn.style.transition = 'transform 0.2s';
        });
        btn.addEventListener('mouseout', () => {
            btn.style.transform = 'scale(1)';
        });
    });

    // -------------------------------
    // 5. Optional: log button clicks (for debugging)
    // -------------------------------
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log(`Button clicked: ${btn.innerText}`);
        });
    });
});
