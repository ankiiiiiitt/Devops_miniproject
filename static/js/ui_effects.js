/**
 * FocusVault Premium UI Effects
 * Handles 3D Tilt interaction and Particles background
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. HERO TILT (UPGRADED 3D VERSION)
    const heroHeading = document.getElementById('heroHeading');
    const heroText = document.querySelector('.hero-3d-text');

    if (heroHeading && heroText) {

        let currentX = 0;
        let currentY = 0;
        let targetX = 0;
        let targetY = 0;

        heroHeading.addEventListener('mousemove', (e) => {
            const rect = heroHeading.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            targetX = ((y - centerY) / centerY) * -15;
            targetY = ((x - centerX) / centerX) * 15;
        });

        heroHeading.addEventListener('mouseleave', () => {
            targetX = 0;
            targetY = 0;
        });

        function animate3D() {
            // smooth interpolation (VERY IMPORTANT 🔥)
            currentX += (targetX - currentX) * 0.1;
            currentY += (targetY - currentY) * 0.1;

            heroText.style.transform = `
            rotateX(${currentX}deg)
            rotateY(${currentY}deg)
            translateZ(40px)
        `;

            requestAnimationFrame(animate3D);
        }

        animate3D();
    }

    // 2. CHAT DESK TILT (Chat Page)
    const chatDesk = document.getElementById('chatDesk');
    if (chatDesk) {
        document.addEventListener('mousemove', (e) => {
            const x = e.clientX;
            const y = e.clientY;
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;

            // Subtle rotation for the whole desk (max 5 degrees)
            const rotateX = ((y - centerY) / centerY) * -5;
            const rotateY = ((x - centerX) / centerX) * 5;

            chatDesk.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
    }

    // 3. PARTICLES INITIALIZATION
    if (document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            "particles": {
                "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#38bdf8" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.2, "random": false },
                "size": { "value": 3, "random": true },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#38bdf8",
                    "opacity": 0.1,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 1.5,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": { "enable": true, "mode": "grab" },
                    "onclick": { "enable": true, "mode": "push" },
                    "resize": true
                },
                "modes": {
                    "grab": { "distance": 140, "line_linked": { "opacity": 0.5 } },
                    "push": { "particles_nb": 4 }
                }
            },
            "retina_detect": true
        });
    }
});

// LIGHT PARALLAX EFFECT
document.addEventListener('mousemove', (e) => {
    const glow = document.querySelector('.bg-glow.blue');

    if (glow) {
        const x = (e.clientX / window.innerWidth) * 30;
        const y = (e.clientY / window.innerHeight) * 30;

        glow.style.transform = `translate(${x}px, ${y}px)`;
    }
});