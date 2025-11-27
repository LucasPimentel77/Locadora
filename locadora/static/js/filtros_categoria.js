// static/js/filtros_categoria.js

class FiltrosCategoria {
    constructor() {
        this.filtrosAtivos = {
            marcas: [],
            disponibilidade: ['disponivel'],
            precoMaximo: 500
        };
        
        this.init();
    }

    init() {
        console.log('🎯 Inicializando filtros de categoria...');
        this.configurarFiltros();
        this.configurarEventos();
    }

    configurarFiltros() {
        // Inicializar checkboxes de marca
        const checkboxesMarca = document.querySelectorAll('input[type="checkbox"][id^="marca"]');
        checkboxesMarca.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.atualizarFiltroMarca(e.target);
            });
        });

        // Inicializar filtro de disponibilidade
        const checkboxesDisponibilidade = document.querySelectorAll('input[type="checkbox"][id="disponivel"], input[type="checkbox"][id="reservado"]');
        checkboxesDisponibilidade.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.atualizarFiltroDisponibilidade(e.target);
            });
        });

        // Inicializar filtro de preço
        const rangePreco = document.getElementById('precoRange');
        if (rangePreco) {
            rangePreco.addEventListener('input', (e) => {
                this.atualizarFiltroPreco(e.target.value);
            });
        }

        // Botão aplicar filtros
        const btnAplicar = document.querySelector('.btn-primary.w-100');
        if (btnAplicar) {
            btnAplicar.addEventListener('click', () => {
                this.aplicarFiltros();
            });
        }
    }

    configurarEventos() {
        // Evento para limpar filtros
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.limparFiltros();
            }
        });
    }

    atualizarFiltroMarca(checkbox) {
        const marca = checkbox.nextElementSibling.textContent.trim();
        
        if (checkbox.checked) {
            if (!this.filtrosAtivos.marcas.includes(marca)) {
                this.filtrosAtivos.marcas.push(marca);
            }
        } else {
            this.filtrosAtivos.marcas = this.filtrosAtivos.marcas.filter(m => m !== marca);
        }
        
        console.log('🚗 Marcas selecionadas:', this.filtrosAtivos.marcas);
    }

    atualizarFiltroDisponibilidade(checkbox) {
        const tipo = checkbox.id;
        
        if (checkbox.checked) {
            if (!this.filtrosAtivos.disponibilidade.includes(tipo)) {
                this.filtrosAtivos.disponibilidade.push(tipo);
            }
        } else {
            this.filtrosAtivos.disponibilidade = this.filtrosAtivos.disponibilidade.filter(d => d !== tipo);
        }
        
        console.log('📅 Disponibilidade:', this.filtrosAtivos.disponibilidade);
    }

    atualizarFiltroPreco(valor) {
        this.filtrosAtivos.precoMaximo = parseInt(valor);
        
        // Atualizar display do preço
        const precoDisplay = document.querySelector('.preco-display');
        if (precoDisplay) {
            precoDisplay.textContent = `Até R$ ${valor}`;
        }
        
        console.log('💰 Preço máximo:', this.filtrosAtivos.precoMaximo);
    }

    aplicarFiltros() {
        console.log('🎯 Aplicando filtros:', this.filtrosAtivos);
        
        // Mostrar loading
        this.mostrarLoading();
        
        // Filtrar carros
        this.filtrarCarros();
        
        // Atualizar contadores
        this.atualizarContadores();
        
        // Mostrar resultados
        setTimeout(() => {
            this.esconderLoading();
            this.mostrarMensagem(`Filtros aplicados! Encontrados ${this.contarCarrosVisiveis()} carros.`, 'success');
        }, 500);
    }

    filtrarCarros() {
        const carros = document.querySelectorAll('.car-card');
        let carrosVisiveis = 0;
        
        carros.forEach(carro => {
            const marca = carro.querySelector('.card-title').textContent.split(' ')[0];
            const precoTexto = carro.querySelector('.text-primary').textContent;
            const preco = parseInt(precoTexto.replace('R$', '').trim());
            const disponivel = !carro.classList.contains('indisponivel');
            
            const passaMarca = this.filtrosAtivos.marcas.length === 0 || 
                             this.filtrosAtivos.marcas.includes(marca);
            
            const passaPreco = preco <= this.filtrosAtivos.precoMaximo;
            
            const passaDisponibilidade = (this.filtrosAtivos.disponibilidade.includes('disponivel') && disponivel) ||
                                      (this.filtrosAtivos.disponibilidade.includes('reservado') && !disponivel);
            
            if (passaMarca && passaPreco && passaDisponibilidade) {
                carro.style.display = 'block';
                carrosVisiveis++;
            } else {
                carro.style.display = 'none';
            }
        });
        
        // Esconder subgrupos vazios
        this.filtrarSubgrupos();
    }

    filtrarSubgrupos() {
        const subgrupos = document.querySelectorAll('.card.border-0.shadow-sm.mb-5');
        
        subgrupos.forEach(subgrupo => {
            const carrosVisiveis = subgrupo.querySelectorAll('.car-card[style=""]').length + 
                                 subgrupo.querySelectorAll('.car-card:not([style*="none"])').length;
            
            if (carrosVisiveis === 0) {
                subgrupo.style.display = 'none';
            } else {
                subgrupo.style.display = 'block';
                
                // Atualizar contador do subgrupo
                const contador = subgrupo.querySelector('.text-muted');
                if (contador) {
                    contador.textContent = `${carrosVisiveis} carros disponíveis`;
                }
            }
        });
    }

    contarCarrosVisiveis() {
        return document.querySelectorAll('.car-card:not([style*="none"])').length;
    }

    atualizarContadores() {
        const totalCarros = this.contarCarrosVisiveis();
        const totalSubgrupos = document.querySelectorAll('.card.border-0.shadow-sm.mb-5[style!="none"]').length;
        
        console.log(`📊 Resultado: ${totalCarros} carros em ${totalSubgrupos} subgrupos`);
    }

    limparFiltros() {
        console.log('🔄 Limpando filtros...');
        
        // Resetar checkboxes
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Marcar disponível como padrão
        document.getElementById('disponivel').checked = true;
        
        // Resetar range de preço
        document.getElementById('precoRange').value = 500;
        
        // Resetar filtros ativos
        this.filtrosAtivos = {
            marcas: [],
            disponibilidade: ['disponivel'],
            precoMaximo: 500
        };
        
        // Mostrar todos os carros
        document.querySelectorAll('.car-card').forEach(carro => {
            carro.style.display = 'block';
        });
        
        document.querySelectorAll('.card.border-0.shadow-sm.mb-5').forEach(subgrupo => {
            subgrupo.style.display = 'block';
        });
        
        this.mostrarMensagem('Filtros limpos!', 'info');
    }

    mostrarLoading() {
        // Implementar loading overlay se necessário
        console.log('⏳ Aplicando filtros...');
    }

    esconderLoading() {
        console.log('✅ Filtros aplicados!');
    }

    mostrarMensagem(mensagem, tipo = 'info') {
        // Usar Toastify ou alert nativo
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
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    new FiltrosCategoria();
});