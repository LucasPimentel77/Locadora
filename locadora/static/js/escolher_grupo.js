// static/js/escolher_grupo.js - VERSÃO SEM VALIDAÇÃO

document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ escolher_grupo.js carregado!");

    // Apenas para cálculos de desconto (opcional)
    const metodosPagamento = document.querySelectorAll('input[name="metodo_pagamento"]');
    const diaria = parseFloat(document.getElementById('diaria-value').dataset.value);
    const totalSemDesconto = diaria;

    // Atualizar totais quando método mudar
    metodosPagamento.forEach(metodo => {
        metodo.addEventListener('change', function() {
            atualizarTotal(this);
        });
    });

    // Calcular total inicial
    const metodoSelecionado = document.querySelector('input[name="metodo_pagamento"]:checked');
    if (metodoSelecionado) {
        atualizarTotal(metodoSelecionado);
    }

    function atualizarTotal(metodoInput) {
        const descontoPercentual = parseFloat(metodoInput.dataset.desconto) || 0;
        let total = totalSemDesconto;

        if (descontoPercentual > 0) {
            const desconto = totalSemDesconto * (descontoPercentual / 100);
            total = totalSemDesconto - desconto;
            
            const descontoContainer = document.getElementById('desconto-container');
            const valorDescontoSpan = document.getElementById('valor-desconto');
            
            if (descontoContainer && valorDescontoSpan) {
                descontoContainer.classList.remove('d-none');
                valorDescontoSpan.textContent = desconto.toFixed(2).replace('.', ',');
            }
        } else {
            const descontoContainer = document.getElementById('desconto-container');
            if (descontoContainer) {
                descontoContainer.classList.add('d-none');
            }
        }

        const totalFinalSpan = document.getElementById('total-final');
        if (totalFinalSpan) {
            totalFinalSpan.textContent = total.toFixed(2).replace('.', ',');
        }
    }
});