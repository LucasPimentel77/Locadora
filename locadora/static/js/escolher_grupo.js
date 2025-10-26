// static/js/escolher_grupo.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ escolher_grupo.js carregado!");

    // Elementos do DOM
    const formasPagamento = document.querySelectorAll('input[name="forma_pagamento"]');
    const descontoPixDiv = document.getElementById('desconto-pix');
    const valorDescontoSpan = document.getElementById('valor-desconto');
    const totalFinalSpan = document.getElementById('total-final');
    const formPagamento = document.getElementById('form-pagamento');
    
    // Valores fixos
    const diaria = parseFloat(document.getElementById('diaria-value').dataset.value);
    const taxas = 25; // Taxas fixas
    const totalSemDesconto = diaria + taxas;

    // Inicializar
    initFormaPagamento();
    initEfeitosVisuais();
    initValidacaoFormulario();

    // Função para inicializar o comportamento das formas de pagamento
    function initFormaPagamento() {
        formasPagamento.forEach(forma => {
            forma.addEventListener('change', function() {
                console.log(`🎯 Forma de pagamento selecionada: ${this.value}`);
                atualizarTotal(this.value);
                highlightOpcaoSelecionada(this);
            });
        });

        // Calcular total inicial
        const formaSelecionada = document.querySelector('input[name="forma_pagamento"]:checked');
        if (formaSelecionada) {
            atualizarTotal(formaSelecionada.value);
        }
    }

    // Função para atualizar o total baseado na forma de pagamento
    function atualizarTotal(formaPagamento) {
        let total = totalSemDesconto;
        let desconto = 0;

        switch(formaPagamento) {
            case 'pix':
                // 5% de desconto para PIX
                desconto = totalSemDesconto * 0.05;
                total = totalSemDesconto - desconto;
                
                // Mostrar desconto
                descontoPixDiv.classList.remove('d-none');
                valorDescontoSpan.textContent = `-R$ ${desconto.toFixed(2).replace('.', ',')}`;
                break;
                
            case 'cartao':
                // Sem desconto, mas mostrar opções de parcelamento
                descontoPixDiv.classList.add('d-none');
                // Aqui você pode adicionar lógica de parcelamento se quiser
                break;
                
            case 'local':
                // Sem desconto
                descontoPixDiv.classList.add('d-none');
                break;
        }

        // Atualizar total na tela
        totalFinalSpan.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
        
        console.log(`💰 Total atualizado: R$ ${total.toFixed(2)} (Desconto: R$ ${desconto.toFixed(2)})`);
    }

    // Função para efeitos visuais nas opções de pagamento
    function initEfeitosVisuais() {
        const opcoesPagamento = document.querySelectorAll('.forma-pagamento-option');
        
        opcoesPagamento.forEach(opcao => {
            // Efeito hover
            opcao.addEventListener('mouseenter', function() {
                if (!this.querySelector('input').checked) {
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                    this.style.transition = 'all 0.3s ease';
                }
            });
            
            opcao.addEventListener('mouseleave', function() {
                if (!this.querySelector('input').checked) {
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '';
                }
            });
            
            // Efeito ao clicar
            opcao.addEventListener('click', function() {
                // Remover destaque de todas as opções
                opcoesPagamento.forEach(opt => {
                    opt.style.background = '';
                    opt.style.borderColor = '#dee2e6';
                });
                
                // Destacar opção selecionada
                this.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
                this.style.borderColor = '#007bff';
            });
        });

        // Destacar opção inicial selecionada
        const opcaoInicial = document.querySelector('.forma-pagamento-option input:checked');
        if (opcaoInicial) {
            highlightOpcaoSelecionada(opcaoInicial);
        }
    }

    // Função para destacar opção selecionada
    function highlightOpcaoSelecionada(input) {
        const opcao = input.closest('.forma-pagamento-option');
        document.querySelectorAll('.forma-pagamento-option').forEach(opt => {
            opt.style.background = '';
            opt.style.borderColor = '#dee2e6';
        });
        
        if (opcao) {
            opcao.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
            opcao.style.borderColor = '#007bff';
        }
    }

    // Função para validação do formulário
    function initValidacaoFormulario() {
        if (formPagamento) {
            formPagamento.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formaSelecionada = document.querySelector('input[name="forma_pagamento"]:checked');
                
                if (!formaSelecionada) {
                    showAlert('Por favor, selecione uma forma de pagamento.', 'warning');
                    return;
                }
                
                // Mostrar loading
                const btnSubmit = this.querySelector('button[type="submit"]');
                const originalText = btnSubmit.innerHTML;
                btnSubmit.innerHTML = '<div class="spinner-border spinner-border-sm me-2"></div> Processando...';
                btnSubmit.disabled = true;
                
                console.log(`🚀 Enviando reserva com pagamento: ${formaSelecionada.value}`);
                
                // Simular processamento (substituir pelo envio real)
                setTimeout(() => {
                    // Aqui você enviaria o formulário para o Django
                    // this.submit(); // Descomente esta linha para enviar realmente
                    
                    // Por enquanto, vamos apenas mostrar sucesso
                    showAlert('Reserva confirmada com sucesso! Redirecionando...', 'success');
                    
                    // Restaurar botão (em produção, remover isso)
                    setTimeout(() => {
                        btnSubmit.innerHTML = originalText;
                        btnSubmit.disabled = false;
                    }, 2000);
                    
                }, 2000);
            });
        }
    }

    // Função para mostrar alertas
    function showAlert(message, type) {
        // Remove alertas anteriores
        const existingAlert = document.querySelector('.custom-alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show custom-alert mt-3`;
        alert.innerHTML = `
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Inserir após o formulário de pagamento
        const cardBody = document.querySelector('.card-body');
        if (cardBody) {
            cardBody.appendChild(alert);
        }
        
        // Scroll suave para o alerta
        alert.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Auto-remover após 5 segundos (exceto para sucesso)
        if (type !== 'success') {
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 5000);
        }
    }

    // Função para obter ícone baseado no tipo de alerta
    function getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'warning': 'exclamation-triangle',
            'danger': 'times-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // Efeito de contagem regressiva para oferta especial (opcional)
    function initContadorOferta() {
        const contadorElement = document.getElementById('contador-oferta');
        if (contadorElement) {
            let tempoRestante = 900; // 15 minutos em segundos
            
            const intervalo = setInterval(() => {
                const minutos = Math.floor(tempoRestante / 60);
                const segundos = tempoRestante % 60;
                
                contadorElement.textContent = `${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;
                
                if (tempoRestante <= 0) {
                    clearInterval(intervalo);
                    contadorElement.textContent = '00:00';
                    showAlert('Oferta especial expirada!', 'warning');
                }
                
                tempoRestante--;
            }, 1000);
        }
    }

    // Inicializar contador de oferta (se existir)
    initContadorOferta();

    console.log("🎯 JavaScript do escolher_grupo configurado com sucesso!");
});