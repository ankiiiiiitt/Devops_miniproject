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

    // 2. CHAT CONTAINER TILT (Modern Bubble Version)
    const chatContainer = document.querySelector('.chat-container');

    if (chatContainer) {
        let cX = 0, cY = 0, tX = 0, tY = 0;

        chatContainer.addEventListener('mousemove', (e) => {
            const rect = chatContainer.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            tX = ((y - centerY) / centerY) * -5; // Subtler tilt for chat
            tY = ((x - centerX) / centerX) * 5;
        });

        chatContainer.addEventListener('mouseleave', () => {
            tX = 0;
            tY = 0;
        });

        function animateChat3D() {
            cX += (tX - cX) * 0.1;
            cY += (tY - cY) * 0.1;

            chatContainer.style.transform = `rotateX(${cX}deg) rotateY(${cY}deg)`;
            requestAnimationFrame(animateChat3D);
        }

        animateChat3D();
    }

    // 4. HOME HUB TILT (Dashboard Home)
    const homeHub = document.getElementById('homeHub');
    if (homeHub) {
        let hX = 0, hY = 0, htX = 0, htY = 0;

        document.addEventListener('mousemove', (e) => {
            const x = e.clientX;
            const y = e.clientY;
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;

            htX = ((y - centerY) / centerY) * -3; // Very subtle scene tilt
            htY = ((x - centerX) / centerX) * 3;
        });

        function animateHome3D() {
            hX += (htX - hX) * 0.05;
            hY += (htY - hY) * 0.05;
            homeHub.style.transform = `rotateX(${hX}deg) rotateY(${hY}deg)`;
            requestAnimationFrame(animateHome3D);
        }
        animateHome3D();
    }

    // 5. HUB CARDS TILT (Features Grid)
    const hubCards = document.querySelectorAll('.hub-card');
    hubCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -15; // Aggressive card tilt
            const rotateY = ((x - centerX) / centerX) * 15;

            card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = `rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        });
    });

    // 7. SIDEBAR 3D TILT (Floating Blade)
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        let sX = 0, sY = 0, stX = 0, stY = 0;

        document.addEventListener('mousemove', (e) => {
            const x = e.clientX;
            const y = e.clientY;
            
            // Check if mouse is on the left side of the screen
            if (x < 400) {
                const centerX = 150; // Sidebar center approx
                const centerY = window.innerHeight / 2;

                stX = ((y - centerY) / centerY) * -5; 
                stY = ((x - centerX) / centerX) * 5;
            } else {
                stX = 0; stY = 0; // Reset when mouse leaves sidebar area
            }
        });

        function animateSidebar3D() {
            sX += (stX - sX) * 0.05;
            sY += (stY - sY) * 0.05;
            sidebar.style.transform = `rotateX(${sX}deg) rotateY(${sY}deg)`;
            requestAnimationFrame(animateSidebar3D);
        }
        animateSidebar3D();
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