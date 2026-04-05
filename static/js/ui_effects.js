/**
 * FocusVault Premium UI Effects
 * Handles 3D Tilt interaction for the Hero heading
 */

document.addEventListener('DOMContentLoaded', () => {
    const heroHeading = document.getElementById('heroHeading');
    const heroText = document.querySelector('.hero-3d-text');

    if (heroHeading && heroText) {
        heroHeading.addEventListener('mousemove', (e) => {
            const rect = heroHeading.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within element
            const y = e.clientY - rect.top;  // y position within element

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            // Calculate rotation values (max 15 degrees)
            const rotateX = ((y - centerY) / centerY) * -15;
            const rotateY = ((x - centerX) / centerX) * 15;

            heroText.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        heroHeading.addEventListener('mouseleave', () => {
            // Smoothly reset rotation
            heroText.style.transform = `rotateX(0deg) rotateY(0deg)`;
        });
    }
});
