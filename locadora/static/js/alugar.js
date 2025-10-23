// static/js/alugar.js

document.addEventListener('DOMContentLoaded', function() {
    // Configurar data mínima como hoje
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('data_retirada').min = hoje;
    document.getElementById('data_devolucao').min = hoje;

    // Validar datas
    document.getElementById('data_retirada').addEventListener('change', function() {
        const dataDevolucao = document.getElementById('data_devolucao');
        dataDevolucao.min = this.value;
        
        if (dataDevolucao.value && dataDevolucao.value < this.value) {
            dataDevolucao.value = this.value;
        }
    });

    // Verificar cupom
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
        
        // Simular delay de rede
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

    // VALIDAÇÃO ANTES DO ENVIO DO FORMULÁRIO
    document.getElementById('form-datas').addEventListener('submit', function(e) {
        const dataRetirada = document.getElementById('data_retirada').value;
        const dataDevolucao = document.getElementById('data_devolucao').value;
        const horaRetirada = document.getElementById('hora_retirada').value;
        const horaDevolucao = document.getElementById('hora_devolucao').value;

        // Validações
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

        // Validar se não é no passado
        const agora = new Date();
        agora.setHours(0, 0, 0, 0); // Considera apenas a data, não a hora
        
        if (dtRetirada < agora) {
            e.preventDefault();
            showAlert('A data de retirada não pode ser no passado.', 'warning');
            return;
        }

        // Se todas as validações passarem, mostrar loading
        const btn = document.getElementById('btn-verificar-disponibilidade');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<div class="spinner-border spinner-border-sm me-2"></div> Verificando...';
        btn.disabled = true;

        // O formulário será enviado normalmente (POST para o Django)
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
    }

    // Mostrar/ocultar resultados baseado no conteúdo da página
    function checkAndShowResults() {
        const resultadosDiv = document.getElementById('resultados');
        const semResultadosDiv = document.getElementById('sem-resultados');
        
        // Verifica se há cards de resultados visíveis
        const temResultados = resultadosDiv.querySelector('.card') || 
                             resultadosDiv.querySelector('.alert-warning');
        
        if (temResultados) {
            resultadosDiv.classList.remove('d-none');
            semResultadosDiv.classList.add('d-none');
        } else {
            resultadosDiv.classList.add('d-none');
            semResultadosDiv.classList.remove('d-none');
        }
    }

    // Efeito hover nos cards disponíveis
    document.querySelectorAll('.disponivel').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Formatação automática de datas
    function formatarDataParaExibicao(dataString) {
        const data = new Date(dataString);
        return data.toLocaleDateString('pt-BR');
    }

    // Atualizar preview das datas selecionadas
    function atualizarPreviewDatas() {
        const dataRetirada = document.getElementById('data_retirada').value;
        const dataDevolucao = document.getElementById('data_devolucao').value;
        
        if (dataRetirada && dataDevolucao) {
            console.log('Período selecionado:', {
                retirada: formatarDataParaExibicao(dataRetirada),
                devolucao: formatarDataParaExibicao(dataDevolucao)
            });
        }
    }

    // Ouvir mudanças nas datas
    document.getElementById('data_retirada').addEventListener('change', atualizarPreviewDatas);
    document.getElementById('data_devolucao').addEventListener('change', atualizarPreviewDatas);

    // Verificar e mostrar resultados ao carregar a página
    checkAndShowResults();
});