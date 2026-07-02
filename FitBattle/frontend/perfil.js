
        const sidebar = document.getElementById('configSidebar');
        const toggleBtn = document.getElementById('toggleMenuBtn');
        const closeBtn = document.getElementById('closeMenuBtn');

        // Alterna visibilidade se clicado na engrenagem
        toggleBtn.addEventListener('click', () => {
            if (sidebar.style.display === 'none') {
                sidebar.style.display = 'flex';
                document.querySelector('.main-content').style.paddingRight = '350px';
            } else {
                sidebar.style.display = 'none';
                document.querySelector('.main-content').style.paddingRight = '0';
            }
        });

        // Fecha no botão X
        closeBtn.addEventListener('click', () => {
            sidebar.style.display = 'none';
            document.querySelector('.main-content').style.paddingRight = '0';
        });
    