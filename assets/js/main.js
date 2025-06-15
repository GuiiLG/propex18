// Set today's date as default
document.getElementById('dataInicio').value = new Date().toISOString().split('T')[0];

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// File upload handling
const fileInput = document.getElementById('planilhaORSE');
const fileLabel = document.getElementById('fileLabel');
const originalFileLabel = fileLabel.innerHTML;

fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const fileSize = (file.size / 1024 / 1024).toFixed(2); // Size in MB
        fileLabel.innerHTML = `
            <i class="fas fa-file-check file-upload-icon"></i>
            <div>
                <div><strong>${file.name}</strong></div>
                <div class="file-info">Tamanho: ${fileSize} MB</div>
            </div>
        `;
        fileLabel.classList.add('has-file');
    } else {
        fileLabel.innerHTML = originalFileLabel;
        fileLabel.classList.remove('has-file');
    }
});

// Form submission
document.getElementById('cronogramaForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const generateBtn = document.getElementById('generateBtn');
    const loading = document.getElementById('loading');
    const successMessage = document.getElementById('successMessage');
    
    // Get form data
    const formData = new FormData();
    const nomeObra = document.getElementById('nomeObra').value;
    const dataInicio = document.getElementById('dataInicio').value;
    const duracao = document.getElementById('duracao').value;
    const planilhaORSE = document.getElementById('planilhaORSE').files[0];
    const informacoesAdicionais = document.getElementById('informacoesAdicionais').value;

    // Validate required fields
    if (!nomeObra || !dataInicio || !duracao || !planilhaORSE) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Prepare form data
    formData.append('nomeObra', nomeObra);
    formData.append('dataInicio', dataInicio);
    formData.append('duracao', duracao);
    formData.append('planilhaORSE', planilhaORSE);
    formData.append('informacoesAdicionais', informacoesAdicionais);

    // Show loading state
    generateBtn.disabled = true;
    loading.classList.add('active');
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';

        // <<< É ESTA PARTE QUE ENVIA A REQUISIÇÃO >>>
    try {
        const apiUrl = "https://eo8abjs7tdfkhjk.m.pipedream.net/"; // Sua URL do Pipedream

        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData, // O corpo da requisição são os dados do seu formulário
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || 'Ocorreu um erro no servidor.');
        }
        
        // Se chegou aqui, deu tudo certo!
        successMessage.textContent = result.message; // Mostra a mensagem de sucesso vinda do Pipedream
        successMessage.classList.add('active');
        e.target.reset(); // Limpa o formulário
        // Reseta o label do arquivo para o estado inicial
        fileLabel.innerHTML = originalFileLabel;
        fileLabel.classList.remove('has-file');

    } catch (error) {
        // Se deu algum erro na comunicação ou no Pipedream
        console.error("Erro ao enviar formulário:", error);
        alert(`Falha ao gerar cronograma: ${error.message}`);
    } finally {
        // Este bloco executa sempre, dando certo ou errado
        // Esconde o spinner e reativa o botão
        generateBtn.disabled = false;
        loading.classList.remove('active');
        generateBtn.innerHTML = 'CRIAR CRONOGRAMA AGORA';
    }
});

// Header scroll effect
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.98)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
    }
});


  

