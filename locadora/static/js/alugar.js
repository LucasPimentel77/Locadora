// static/js/alugar.js - VERSÃO CORRIGIDA

document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ JavaScript carregado!");

    // Configurar data mínima como hoje
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('data_retirada').min = hoje;
    document.getElementById('data_devolucao').min = hoje;

    // Quando a data de retirada muda, atualiza a mínima da devolução
    document.getElementById('data_retirada').addEventListener('change', function() {
        const dataDevolucao = document.getElementById('data_devolucao');
        dataDevolucao.min = this.value;
        
        // Se a data de devolução for anterior, corrige
        if (dataDevolucao.value && dataDevolucao.value < this.value) {
            dataDevolucao.value = this.value;
        }
    });

    // Verificar cupom (funcionalidade independente)
    document.getElementById('btn-verificar-cupom').addEventListener('click', verificarCupom);

    // VALIDAÇÃO DO FORMULÁRIO ANTES DE ENVIAR
    document.getElementById('form-datas').addEventListener('submit', function(e) {
        console.log("🔄 Formulário sendo validado...");
        
        const dataRetirada = document.getElementById('data_retirada').value;
        const dataDevolucao = document.getElementById('data_devolucao').value;
        const horaRetirada = document.getElementById('hora_retirada').value;
        const horaDevolucao = document.getElementById('hora_devolucao').value;

        // Validações básicas
        if (!dataRetirada || !dataDevolucao || !horaRetirada || !horaDevolucao) {
            e.preventDefault();
            showAlert('Por favor, preencha todas as datas e horários.', 'danger');
            return;
        }

        // Validar se data devolução é depois da retirada
        const dtRetirada = new Date(dataRetirada + 'T' + horaRetirada);
        const dtDevolucao = new Date(dataDevolucao + 'T' + horaDevolucao);
        
        if (dtDevolucao <= dtRetirada) {
            e.preventDefault();
            showAlert('A data de devolução deve ser posterior à data de retirada.', 'warning');
            return;
        }

        // Se passou todas as validações, mostrar loading
        console.log("✅ Validações passadas - enviando formulário...");
        const btn = document.getElementById('btn-verificar-disponibilidade');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<div class="spinner-border spinner-border-sm me-2"></div> Verificando...';
        btn.disabled = true;

        // O formulário será enviado normalmente para o Django
    });

    // Efeito hover nos cards (se existirem)
    document.querySelectorAll('.disponivel').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Função para controle de exibição de resultados
    function checkAndShowResults() {
        const resultadosDiv = document.getElementById('resultados');
        const semResultadosDiv = document.getElementById('sem-resultados');
        
        // A lógica agora é controlada pelo Django via template
        // O JavaScript só precisa garantir o comportamento inicial
        console.log("📊 Verificando estado dos resultados...");
    }

    // Chamar a função de verificação
    checkAndShowResults();

    console.log("🎯 JavaScript configurado com sucesso!");
});

// FUNÇÕES GLOBAIS (fora do DOMContentLoaded)

function verificarCupom() {
    const cupom = document.getElementById('cupom').value;
    const mensagem = document.getElementById('mensagem-cupom');
    
    if (!cupom) {
        mensagem.innerHTML = '<small class="text-danger">Digite um cupom</small>';
        return;
    }

    // Mostrar loading
    const btn = this;
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="spinner-border spinner-border-sm me-2"></div> Verificando...';
    btn.disabled = true;

    // Fazer requisição AJAX para verificar o cupom no backend
    fetch('/reserva/api/verificar-cupom/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            'cupom': cupom
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.valido) {
            mensagem.innerHTML = `<small class="text-success"><i class="fas fa-check me-1"></i>${data.mensagem}</small>`;
            
            // Aplicar desconto no valor total
            if (data.desconto_aplicado) {
                aplicarDesconto(data.desconto_percentual, data.valor_desconto);
            }
        } else {
            mensagem.innerHTML = `<small class="text-danger"><i class="fas fa-times me-1"></i>${data.mensagem}</small>`;
        }
        
        // Restaurar botão
        btn.innerHTML = originalText;
        btn.disabled = false;
    })
    .catch(error => {
        console.error('Erro:', error);
        mensagem.innerHTML = '<small class="text-danger"><i class="fas fa-times me-1"></i>Erro ao verificar cupom</small>';
        
        // Restaurar botão
        btn.innerHTML = originalText;
        btn.disabled = false;
    });
}

// Função para aplicar o desconto na interface
function aplicarDesconto(percentual, valorDesconto) {
    const valorTotalElement = document.querySelector('.valor-total');
    if (!valorTotalElement) {
        console.warn('Elemento .valor-total não encontrado');
        return;
    }
    
    const valorOriginal = parseFloat(valorTotalElement.dataset.valorOriginal) || 
                         parseFloat(valorTotalElement.textContent.replace('R$ ', '').replace(',', '.').replace('.', ''));
    
    // Salvar valor original se não estiver salvo
    if (!valorTotalElement.dataset.valorOriginal) {
        valorTotalElement.dataset.valorOriginal = valorOriginal;
    }
    
    // Calcular novo valor
    const novoValor = valorOriginal - valorDesconto;
    
    // Atualizar interface
    valorTotalElement.innerHTML = `R$ ${novoValor.toFixed(2).replace('.', ',')}`;
    
    // Mostrar desconto aplicado
    const descontoElement = document.getElementById('desconto-aplicado');
    if (descontoElement) {
        descontoElement.innerHTML = `
            <div class="alert alert-success mt-2">
                <i class="fas fa-tag me-2"></i>
                <strong>Desconto aplicado:</strong> ${percentual}% (R$ ${valorDesconto.toFixed(2).replace('.', ',')})
            </div>
        `;
    }
    
    // Atualizar campo hidden para o formulário
    const cupomInput = document.getElementById('cupom');
    if (cupomInput) {
        cupomInput.dataset.cupomValido = 'true';
    }
}

// Função para pegar o token CSRF
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Função para mostrar alertas (tornar global)
function showAlert(message, type) {
    // Remove alertas anteriores
    const existingAlert = document.querySelector('.alert-dismissible');
    if (existingAlert) {
        existingAlert.remove();
    }

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const form = document.getElementById('form-datas');
    if (form) {
        form.prepend(alert);
        
        // Scroll para o alerta
        alert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}