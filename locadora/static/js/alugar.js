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
    document.getElementById('btn-verificar-cupom').addEventListener('click', function() {
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

        // Cupons válidos estáticos
        const cuponsValidos = ['SPEED10', 'PRIMEIRALOCACAO', 'DESCONTO15'];
        
        // Simular verificação
        setTimeout(function() {
            if (cuponsValidos.includes(cupom.toUpperCase())) {
                mensagem.innerHTML = '<small class="text-success"><i class="fas fa-check me-1"></i>Cupom válido! Desconto aplicado.</small>';
            } else {
                mensagem.innerHTML = '<small class="text-danger"><i class="fas fa-times me-1"></i>Cupom inválido</small>';
            }
            
            // Restaurar botão
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 1000);
    });

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

    // Função para mostrar alertas
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
        
        document.getElementById('form-datas').prepend(alert);
        
        // Scroll para o alerta
        alert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

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

// REMOVA ESTA PARTE DUPLICADA:
// document.addEventListener('DOMContentLoaded', function() {
//     // Configurações básicas...
//     const hoje = new Date().toISOString().split('T')[0];
//     document.getElementById('data_retirada').min = hoje;
//     document.getElementById('data_devolucao').min = hoje;
//
//     // Resto do código permanece igual...
//     // (validações, cupom, etc.)
// });