// static/js/admin_reservas.js

class AdminReservasManager {
    constructor() {
        this.csrfToken = this.getCSRFToken();
        this.init();
    }

    init() {
        console.log('🎯 Admin Reservas Manager inicializado');
        this.setupEventListeners();
        this.setupTooltips();
        this.setupAutoRefresh();
    }

    setupEventListeners() {
        // Filtro por status
        const statusSelect = document.querySelector('select[name="status"]');
        if (statusSelect) {
            statusSelect.addEventListener('change', () => {
                this.submitFilterForm();
            });
        }

        // Botão exportar
        const exportBtn = document.querySelector('button[onclick*="exportarParaCSV"]');
        if (exportBtn) {
            exportBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.exportarParaCSV();
            });
        }

        // Clique em cards para ver detalhes
        const cards = document.querySelectorAll('.admin-reserva-card');
        cards.forEach(card => {
            card.addEventListener('click', (e) => {
                // Evita abrir detalhes quando clicar em botões
                if (!e.target.closest('button, a')) {
                    const reservaId = card.id.split('-')[1];
                    this.verDetalhes(reservaId);
                }
            });
        });

        // Observar mudanças nos filtros de data
        const dateInputs = document.querySelectorAll('input[type="date"]');
        dateInputs.forEach(input => {
            input.addEventListener('change', () => {
                setTimeout(() => this.submitFilterForm(), 300);
            });
        });
    }

    setupTooltips() {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip, {
                trigger: 'hover',
                placement: 'top'
            });
        });
    }

    setupAutoRefresh() {
        // Auto-refresh a cada 30 segundos se houver reservas ativas/pendentes
        const hasActiveReservas = document.querySelectorAll('.admin-reserva-card').length > 0;
        
        if (hasActiveReservas) {
            setInterval(() => {
                this.checkForUpdates();
            }, 30000); // 30 segundos
        }
    }

    submitFilterForm() {
        document.getElementById('filtroForm').submit();
    }




    carregarDetalhesModal(reservaId) {
        // Implementar carregamento de modal com detalhes
        console.log(`Carregando detalhes da reserva ${reservaId} em modal`);
        // TODO: Implementar modal de detalhes
        window.open(`/admin/reservas/${reservaId}/detalhes/`, '_blank');
    }

    exportarParaCSV() {
        const params = new URLSearchParams(window.location.search);
        const url = `/api/admin/reservas/exportar/?${params.toString()}`;
        
        this.mostrarLoading('Gerando arquivo CSV...');
        
        fetch(url, {
            headers: {
                'X-CSRFToken': this.csrfToken
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Erro ao exportar');
            return response.blob();
        })
        .then(blob => {
            this.esconderLoading();
            
            // Criar link de download
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `reservas_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            this.mostrarMensagem('Arquivo CSV baixado com sucesso!', 'success');
        })
        .catch(error => {
            this.esconderLoading();
            this.mostrarMensagem(`Erro ao exportar: ${error.message}`, 'error');
        });
    }

    checkForUpdates() {
        // Verificar se há novas reservas sem recarregar toda a página
        fetch(window.location.href, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const newDoc = parser.parseFromString(html, 'text/html');
            const newCount = newDoc.querySelector('.badge.bg-primary')?.textContent;
            const currentCount = document.querySelector('.badge.bg-primary')?.textContent;
            
            if (newCount && newCount !== currentCount) {
                this.mostrarMensagem(`Atualização: ${newCount} reservas disponíveis`, 'info');
            }
        })
        .catch(error => console.log('Erro ao verificar atualizações:', error));
    }

    // Utilitários
    mostrarLoading(mensagem) {
        // Remover loading anterior se existir
        this.esconderLoading();
        
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'admin-loading-overlay';
        loadingDiv.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
                <p class="mt-2">${mensagem}</p>
            </div>
        `;
        loadingDiv.id = 'admin-loading';
        document.body.appendChild(loadingDiv);
    }

    esconderLoading() {
        const loadingDiv = document.getElementById('admin-loading');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

    mostrarMensagem(mensagem, tipo = 'info') {
        // Usar Toastify se disponível
        if (typeof Toastify !== 'undefined') {
            Toastify({
                text: mensagem,
                duration: 3000,
                gravity: "top",
                position: "right",
                backgroundColor: this.getCorMensagem(tipo),
            }).showToast();
        } else {
            // Fallback para alerta Bootstrap
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${tipo} alert-dismissible fade show position-fixed admin-alert`;
            alertDiv.style.cssText = `
                top: 20px;
                right: 20px;
                z-index: 9999;
                min-width: 300px;
            `;
            alertDiv.innerHTML = `
                <i class="fas fa-${this.getIconeMensagem(tipo)} me-2"></i>
                ${mensagem}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(alertDiv);
            
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 3000);
        }
    }

    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    getCorMensagem(tipo) {
        const cores = {
            'success': '#28a745',
            'error': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8'
        };
        return cores[tipo] || '#17a2b8';
    }

    getIconeMensagem(tipo) {
        const icones = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icones[tipo] || 'info-circle';
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    window.adminReservas = new AdminReservasManager();
});