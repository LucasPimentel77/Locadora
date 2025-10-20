// Funções JavaScript para sua locadora
document.addEventListener('DOMContentLoaded', function() {
    console.log('Locadora SpeedCar carregada!');
    
    // Animação suave para scroll
    const smoothScroll = (target) => {
        const element = document.querySelector(target);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    };
    
    // Contador de carros disponíveis (exemplo)
    const updateCarCount = () => {
        const countElement = document.getElementById('car-count');
        if (countElement) {
            // Simulação - depois substitua por dados reais
            countElement.textContent = '42';
        }
    };
    
    // Inicializar funções
    updateCarCount();
    
    // Botão de voltar ao topo
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});