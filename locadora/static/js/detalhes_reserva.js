// static/js/detalhes_reserva.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ detalhes_reserva.js carregado!");

    // Elementos do DOM
    const btnImprimir = document.getElementById('btn-imprimir');
    const btnCompartilhar = document.getElementById('btn-compartilhar');
    const btnCheckin = document.getElementById('btn-checkin');
    const btnCheckout = document.getElementById('btn-checkout');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');
    const btnSuporte = document.getElementById('btn-suporte');

    // Inicializar funcionalidades
    initBotoesAcao();
    initContadorTempo();
    initAnimacoes();

    // Função para inicializar botões de ação
    function initBotoesAcao() {
        // Botão Imprimir
        if (btnImprimir) {
            btnImprimir.addEventListener('click', function() {
                console.log("🖨️ Imprimindo reserva...");
                window.print();
                showToast('Preparando para impressão...', 'info');
            });
        }

        // Botão Compartilhar
        if (btnCompartilhar) {
            btnCompartilhar.addEventListener('click', function() {
                console.log("📤 Compartilhando reserva...");
                compartilharReserva();
            });
        }

        // Botão Check-in
        if (btnCheckin) {
            btnCheckin.addEventListener('click', function() {
                console.log("✅ Iniciando check-in...");
                confirmarAcao(
                    'Check-in', 
                    'Deseja confirmar o check-in para esta reserva?',
                    realizarCheckin
                );
            });
        }

        // Botão Check-out
        if (btnCheckout) {
            btnCheckout.addEventListener('click', function() {
                console.log("🚗 Iniciando check-out...");
                confirmarAcao(
                    'Check-out', 
                    'Deseja confirmar o check-out para esta reserva?',
                    realizarCheckout
                );
            });
        }

        // Botão Alterar
        if (btnAlterar) {
            btnAlterar.addEventListener('click', function() {
                console.log("✏️ Solicitando alteração...");
                showToast('Redirecionando para alteração...', 'info');
                // Aqui você redirecionaria para uma página de alteração
                setTimeout(() => {
                    window.location.href = `/alterar-reserva/{{ reserva.id }}/`;
                }, 1000);
            });
        }

        // Botão Cancelar
        if (btnCancelar) {
            btnCancelar.addEventListener('click', function() {
                console.log("❌ Solicitando cancelamento...");
                confirmarAcao(
                    'Cancelar Reserva', 
                    'Tem certeza que deseja cancelar esta reserva? Esta ação não pode ser desfeita.',
                    cancelarReserva,
                    'danger'
                );
            });
        }

        // Botão Suporte
        if (btnSuporte) {
            btnSuporte.addEventListener('click', function() {
                console.log("📞 Abrindo suporte...");
                abrirSuporte();
            });
        }
    }

    // Função para compartilhar reserva
    function compartilharReserva() {
        const dadosCompartilhamento = {
            title: 'Minha Reserva - SpeedCar',
            text: `Confira minha reserva #{{ reserva.id }} na SpeedCar - {{ reserva.grupo.nome }}`,
            url: window.location.href
        };

        if (navigator.share) {
            navigator.share(dadosCompartilhamento)
                .then(() => showToast('Reserva compartilhada com sucesso!', 'success'))
                .catch(error => {
                    console.log('Erro ao compartilhar:', error);
                    copiarParaAreaTransferencia();
                });
        } else {
            copiarParaAreaTransferencia();
        }
    }

    // Função para copiar link para área de transferência
    function copiarParaAreaTransferencia() {
        navigator.clipboard.writeText(window.location.href)
            .then(() => showToast('Link copiado para área de transferência!', 'success'))
            .catch(err => {
                console.error('Erro ao copiar:', err);
                showToast('Erro ao copiar link', 'error');
            });
    }

    // Função para confirmar ações
    function confirmarAcao(titulo, mensagem, callback, tipo = 'warning') {
        // Usando SweetAlert2 ou confirm nativo
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                title: titulo,
                text: mensagem,
                icon: tipo,
                showCancelButton: true,
                confirmButtonColor: tipo === 'danger' ? '#d33' : '#3085d6',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Confirmar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    callback();
                }
            });
        } else {
            if (confirm(mensagem)) {
                callback();
            }
        }
    }

    // Funções de ação
    function realizarCheckin() {
        showLoading('Realizando check-in...');
        
        // Simular API call
        setTimeout(() => {
            hideLoading();
            showToast('Check-in realizado com sucesso!', 'success');
            // Atualizar página ou status
            setTimeout(() => {
                location.reload();
            }, 2000);
        }, 2000);
    }

    function realizarCheckout() {
        showLoading('Realizando check-out...');
        
        setTimeout(() => {
            hideLoading();
            showToast('Check-out realizado com sucesso!', 'success');
            setTimeout(() => {
                location.reload();
            }, 2000);
        }, 2000);
    }

    function cancelarReserva() {
        showLoading('Cancelando reserva...');
        
        setTimeout(() => {
            hideLoading();
            showToast('Reserva cancelada com sucesso!', 'success');
            setTimeout(() => {
                window.location.href = "{% url 'alugar' %}";
            }, 2000);
        }, 2000);
    }

    function abrirSuporte() {
        const numeroSuporte = "5511999999999";
        const mensagem = `Olá, preciso de ajuda com a reserva #{{ reserva.id }}`;
        const urlWhatsapp = `https://wa.me/${numeroSuporte}?text=${encodeURIComponent(mensagem)}`;
        
        window.open(urlWhatsapp, '_blank');
    }

    // Contador de tempo até a retirada
    function initContadorTempo() {
        const dataRetirada = new Date("{{ reserva.data_retirada|date:'c' }}");
        const agora = new Date();
        
        if (dataRetirada > agora && "{{ reserva.status }}" === 'confirmada') {
            iniciarContadorRegressivo(dataRetirada);
        }
    }

    function iniciarContadorRegressivo(dataAlvo) {
        const contadorElement = document.createElement('div');
        contadorElement.className = 'alert alert-info mt-3';
        contadorElement.innerHTML = `
            <i class="fas fa-clock me-2"></i>
            <strong>Retirada em: </strong>
            <span id="contador-tempo"></span>
        `;
        
        document.querySelector('.status-card .card-body').appendChild(contadorElement);
        
        const intervalo = setInterval(() => {
            const agora = new Date();
            const diferenca = dataAlvo - agora;
            
            if (diferenca <= 0) {
                clearInterval(intervalo);
                contadorElement.innerHTML = '<i class="fas fa-check-circle me-2"></i><strong>Horário de retirada chegou!</strong>';
                contadorElement.className = 'alert alert-success mt-3';
                return;
            }
            
            const dias = Math.floor(diferenca / (1000 * 60 * 60 * 24));
            const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
            
            let textoContador = '';
            if (dias > 0) textoContador += `${dias}d `;
            textoContador += `${horas.toString().padStart(2, '0')}h ${minutos.toString().padStart(2, '0')}m`;
            
            document.getElementById('contador-tempo').textContent = textoContador;
        }, 1000);
    }

    // Animações
    function initAnimacoes() {
        // Efeito de digitação no número da reserva
        const numeroReserva = document.querySelector('.h3.fw-bold');
        if (numeroReserva) {
            numeroReserva.style.opacity = '0';
            setTimeout(() => {
                numeroReserva.style.transition = 'opacity 0.5s ease';
                numeroReserva.style.opacity = '1';
            }, 300);
        }

        // Efeito de pulse no status
        const statusBadge = document.querySelector('.status-badge');
        if (statusBadge) {
            setInterval(() => {
                statusBadge.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    statusBadge.style.transform = 'scale(1)';
                }, 500);
            }, 3000);
        }
    }

    // Utilitários
    function showToast(mensagem, tipo = 'info') {
        // Usando Toastify ou similar
        if (typeof Toastify !== 'undefined') {
            Toastify({
                text: mensagem,
                duration: 3000,
                gravity: "top",
                position: "right",
                backgroundColor: tipo === 'success' ? '#28a745' : 
                               tipo === 'error' ? '#dc3545' : 
                               tipo === 'warning' ? '#ffc107' : '#17a2b8',
            }).showToast();
        } else {
            alert(mensagem);
        }
    }

    function showLoading(mensagem) {
        // Implementar loading overlay
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading-overlay';
        loadingDiv.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
                <p class="mt-2">${mensagem}</p>
            </div>
        `;
        loadingDiv.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            color: white;
        `;
        document.body.appendChild(loadingDiv);
    }

    function hideLoading() {
        const loadingDiv = document.getElementById('loading-overlay');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

    console.log("🎯 JavaScript do detalhes_reserva configurado com sucesso!");
});