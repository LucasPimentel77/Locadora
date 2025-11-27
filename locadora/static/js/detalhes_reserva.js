// static/js/detalhes_reserva.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ detalhes_reserva.js carregado!");

    // OBTER DADOS DO TEMPLATE
    const reservaData = document.getElementById('reserva-data');
    const RESERVA_ID = reservaData ? reservaData.getAttribute('data-reserva-id') : null;
    const CSRF_TOKEN = reservaData ? reservaData.getAttribute('data-csrf-token') : '';

    console.log(`📋 Reserva ID: ${RESERVA_ID}`);

    // Elementos do DOM
    const btnImprimir = document.getElementById('btn-imprimir');
    const btnCompartilhar = document.getElementById('btn-compartilhar');
    const btnPagamento = document.getElementById('btn-pagamento');
    const btnCheckin = document.getElementById('btn-checkin');
    const btnCheckout = document.getElementById('btn-checkout');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');
    const btnSuporte = document.getElementById('btn-suporte');

    // PRIMEIRO: DEFINIR AS FUNÇÕES UTILITÁRIAS
    function showToast(mensagem, tipo = 'info') {
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

    function confirmarAcao(titulo, mensagem, callback, tipo = 'warning') {
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

    function copiarParaAreaTransferencia() {
        navigator.clipboard.writeText(window.location.href)
            .then(() => showToast('Link copiado para área de transferência!', 'success'))
            .catch(err => {
                console.error('Erro ao copiar:', err);
                showToast('Erro ao copiar link', 'error');
            });
    }

    function abrirSuporte() {
        const numeroSuporte = "5511999999999";
        const mensagem = `Olá, preciso de ajuda com a reserva #{{ reserva.id }}`;
        const urlWhatsapp = `https://wa.me/${numeroSuporte}?text=${encodeURIComponent(mensagem)}`;
        
        window.open(urlWhatsapp, '_blank');
    }

    // FUNÇÕES PARA ATUALIZAR STATUS
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    function atualizarStatusReserva(novoStatus) {
        return new Promise((resolve, reject) => {
             if (!RESERVA_ID) {
                reject('ID da reserva não encontrado');
                return;
            }
            
            fetch(`/api/reservas/${RESERVA_ID}/atualizar-status/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    'status': novoStatus
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta do servidor: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    resolve(data);
                } else {
                    reject(data.error || 'Erro desconhecido no servidor');
                }
            })
            .catch(error => {
                reject('Erro de conexão: ' + error.message);
            });
        });
    }

    function getStatusDescription(status) {
        const descricoes = {
            'pendente': 'Aguardando confirmação de pagamento',
            'confirmada': 'Reserva confirmada - Aguardando retirada',
            'ativa': 'Veículo em uso',
            'concluida': 'Reserva finalizada com sucesso',
            'cancelada': 'Reserva cancelada'
        };
        return descricoes[status] || 'Status desconhecido';
    }

    function atualizarInterfaceStatus(novoStatus) {
        console.log(`🔄 Atualizando interface para status: ${novoStatus}`);
        
        const statusBadge = document.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.classList.remove('bg-warning', 'bg-success', 'bg-primary', 'bg-secondary', 'bg-danger');
            
            const classesStatus = {
                'pendente': 'bg-warning',
                'confirmada': 'bg-success', 
                'ativa': 'bg-primary',
                'concluida': 'bg-secondary',
                'cancelada': 'bg-danger'
            };
            
            statusBadge.className = `badge ${classesStatus[novoStatus] || 'bg-secondary'} status-badge`;
            statusBadge.textContent = novoStatus.toUpperCase();
        }

        const statusText = document.querySelector('.status-text');
        if (statusText) {
            statusText.textContent = getStatusDescription(novoStatus);
        }

        setTimeout(() => {
            location.reload();
        }, 1500);
    }

    // FUNÇÕES PRINCIPAIS DE MUDANÇA DE STATUS
    function realizarPagamento() {
        showLoading('Processando pagamento...');
        
        atualizarStatusReserva('confirmada')
            .then(() => {
                hideLoading();
                showToast('Pagamento confirmado! Status atualizado para CONFIRMADA.', 'success');
                atualizarInterfaceStatus('confirmada');
            })
            .catch(error => {
                hideLoading();
                showToast('Erro ao processar pagamento: ' + error, 'error');
            });
    }

    function realizarCheckin() {
        showLoading('Realizando check-in...');
        
        atualizarStatusReserva('ativa')
            .then(() => {
                hideLoading();
                showToast('Check-in realizado com sucesso! Status atualizado para ATIVA.', 'success');
                atualizarInterfaceStatus('ativa');
            })
            .catch(error => {
                hideLoading();
                showToast('Erro ao realizar check-in: ' + error, 'error');
            });
    }

    function realizarCheckout() {
        showLoading('Realizando check-out...');
        
        atualizarStatusReserva('concluida')
            .then(() => {
                hideLoading();
                showToast('Check-out realizado com sucesso! Status atualizado para CONCLUÍDA.', 'success');
                atualizarInterfaceStatus('concluida');
            })
            .catch(error => {
                hideLoading();
                showToast('Erro ao realizar check-out: ' + error, 'error');
            });
    }

    function cancelarReserva() {
        showLoading('Cancelando reserva...');
        
        atualizarStatusReserva('cancelada')
            .then(() => {
                hideLoading();
                showToast('Reserva cancelada com sucesso!', 'success');
                atualizarInterfaceStatus('cancelada');
                
                setTimeout(() => {
                    window.location.href = "{% url 'minhas_reservas' %}";
                }, 3000);
            })
            .catch(error => {
                hideLoading();
                showToast('Erro ao cancelar reserva: ' + error, 'error');
            });
    }

    // DEPOIS: INICIALIZAR OS BOTÕES
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

        // Botão Pagamento
        if (btnPagamento) {
            btnPagamento.addEventListener('click', function() {
                console.log("💳 Iniciando pagamento...");
                confirmarAcao(
                    'Confirmar Pagamento', 
                    'Deseja confirmar o pagamento desta reserva?',
                    realizarPagamento
                );
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
                setTimeout(() => {
                    window.location.href = `/reserva/alterar/{{ reserva.id }}/`;
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

    // FINALMENTE: INICIALIZAR TUDO
    initBotoesAcao();

    console.log("🎯 JavaScript do detalhes_reserva configurado com sucesso!");
});