# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Banco de dados unificado - SEM menção à Bucket Eventos e com links de imagens corrigidos
PACOTES = [
    {
        "id": 1,
        "destino": "Ouro Preto, MG",
        "categoria": "Excursão Feminina • Histórica",
        "diarias": "2 diárias",
        "embarque": "Belo Horizonte, Contagem",
        "descricao": "Descubra o charme das ladeiras históricas, igrejas barrocas e a rica gastronomia mineira em uma viagem inesquecível.",
        "detalhes_longos": "Uma imersão profunda na história colonial do Brasil, com roteiros focados em arte, arquitetura barroca e culinária típica mineira.",
        "hotel": "Pousada das Artes (Centro Histórico)",
        "seguro_valor": "15.000,00",
        "organizadora": "Luana Lage",
        "reputacao_estrelas": 5,
        "reputacao_pct": "98%",
        "atividades": "Tour guiado pelas igrejas históricas, visita a antigas minas de ouro, jantar temático tradicional e feira de pedra sabão.",
        "passeio_grupo": "Sim (Acompanhamento de Guia de Turismo credenciado pelo Ministério do Turismo)",
        "preco": "240,00",
        "imagem": "https://images.unsplash.com/photo-1626082929543-5bab0f090c42?w=600&q=80"
    },
    {
        "id": 2,
        "destino": "São Thomé das Letras, MG",
        "categoria": "Ecoturismo • Misticismo",
        "diarias": "3 diárias",
        "embarque": "Belo Horizonte, Betim",
        "descricao": "Jornada energética pelas cachoeiras de quartzito, grutas e o pôr do sol inesquecível na Casa da Pirâmide. Ambiente seguro.",
        "detalhes_longos": "Ideal para quem busca renovação energética, trilhas ecológicas integradas e contato direto com a natureza mística da região.",
        "hotel": "Eco-Pousada do Gnomo (Verificado)",
        "seguro_valor": "10.000,00",
        "organizadora": "Mariana Trips",
        "reputacao_estrelas": 4,
        "reputacao_pct": "95%",
        "atividades": "Complexo da Cachoeira da Eubiose, Pôr do sol na Casa da Pirâmide, Luau feminino integrado na fogueira.",
        "passeio_grupo": "Sim (Lotação máxima de 25 pessoas para manter o clima intimista e seguro)",
        "preco": "280,00",
        "imagem": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&q=80"
    },
    {
        "id": 3,
        "destino": "Arraial do Cabo, RJ",
        "categoria": "Praia • Lazer Feminino",
        "diarias": "4 diárias",
        "embarque": "Belo Horizonte, Juiz de Fora",
        "descricao": "O Caribe brasileiro aguarda nosso bando! Passeio de escuna exclusivo, praias de águas cristalinas e momentos únicos.",
        "detalhes_longos": "Foco total em relaxamento, banhos de mar revigorantes e diversão nas praias de areia branca mais famosas do Rio de Janeiro.",
        "hotel": "Hotel Mar dos Anjos (Frente Mar)",
        "seguro_valor": "20.000,00",
        "organizadora": "Clara Viagens",
        "reputacao_estrelas": 5,
        "reputacao_pct": "109%",  # Mantendo fidelidade à visualização de alta aprovação
        "atividades": "Passeio de Escuna privativo, Mergulho de batismo guiado, Trilhas leves pelas praias preservadas.",
        "passeio_grupo": "Sim (Transporte em van privativa exclusiva do bando do início ao fim)",
        "preco": "450,00",
        "imagem": "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=600&q=80"
    }
]

# Template Base - Cores 100% corrigidas para a paleta Terracota (#E35336) e Salmão (#FF7E70)
# Azul completamente eliminado da interface
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vacare - Plataforma de Experiências Femininas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <style>
        :root {
            --terracota: #E35336;
            --terracota-hover: #c84126;
            --salmon: #FF7E70;
            --salmon-hover: #e5695c;
            --dark-text: #2d3748;
            --light-gray: #f7fafc;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--light-gray);
            color: var(--dark-text);
        }

        /* Top Utility Bar & Header */
        .top-bar {
            background-color: #ffffff;
            border-bottom: 1px solid #edf2f7;
            font-size: 13px;
        }
        .top-link {
            color: #718096;
            text-decoration: none;
            margin-left: 20px;
            transition: color 0.2s;
            font-weight: 600;
        }
        .top-link:hover {
            color: var(--salmon);
        }

        .main-header {
            background-color: #ffffff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
            padding: 15px 0;
        }
        .brand-logo {
            font-size: 28px;
            font-weight: 800;
            color: var(--terracota) !important;
            text-decoration: none;
            letter-spacing: -0.5px;
        }
        
        /* Hero / Caixa de Busca CVC Style em Tons Terracota */
        .hero-section {
            background: linear-gradient(135deg, #fdfbf7 0%, #f9f1e6 100%);
            padding: 40px 0;
            border-bottom: 4px solid var(--terracota);
        }
        .search-container {
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(227, 83, 54, 0.06);
            padding: 25px;
        }
        .search-title {
            color: var(--terracota);
            font-weight: 700;
            font-size: 22px;
            margin-bottom: 20px;
        }
        .form-control-custom {
            border: 1px solid #cbd5e0;
            padding: 12px 15px;
            border-radius: 8px;
        }
        .form-control-custom:focus {
            border-color: var(--terracota);
            box-shadow: 0 0 0 0.25rem rgba(227, 83, 54, 0.15);
        }
        .btn-search {
            background-color: var(--terracota);
            color: #ffffff;
            padding: 12px 30px;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            width: 100%;
            transition: background 0.2s;
        }
        .btn-search:hover {
            background-color: var(--terracota-hover);
        }

        /* Cards Worldpackers Style totalmente clicáveis */
        .wp-card {
            background: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.01);
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 25px;
            cursor: pointer;
        }
        .wp-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(227, 83, 54, 0.08);
        }
        .wp-img-container { position: relative; height: 220px; }
        .wp-img { width: 100%; height: 100%; object-fit: cover; }
        
        .badge-category {
            position: absolute;
            top: 15px;
            left: 15px;
            background-color: rgba(45, 55, 72, 0.9);
            color: #fff;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-duration {
            position: absolute;
            bottom: 15px;
            right: 15px;
            background-color: var(--salmon);
            color: #fff;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 700;
        }
        .wp-content { padding: 20px; }
        .wp-destino { font-size: 20px; font-weight: 700; color: var(--terracota); margin-bottom: 6px; }
        .wp-embarque { font-size: 13px; color: #718096; margin-bottom: 12px; }
        .wp-description { font-size: 14px; color: #4a5568; line-height: 1.6; margin-bottom: 20px; }
        .wp-footer { border-top: 1px solid #edf2f7; padding-top: 15px; display: flex; justify-content: space-between; align-items: center; }
        .wp-price { font-size: 22px; font-weight: 800; color: var(--terracota); }

        /* Custom Modal de Detalhes em Tons de Salmão e Terracota */
        .modal-header-custom { background: var(--terracota); color: white; border: none; }
        .detail-icon { color: var(--salmon); margin-right: 10px; font-size: 18px; }
        .reputation-bar { background: #e2e8f0; height: 8px; border-radius: 4px; margin: 10px 0; }
        .reputation-fill { background: var(--salmon); height: 100%; border-radius: 4px; }
        .btn-reserve { background-color: var(--salmon); color: white; font-weight: bold; padding: 12px; border: none; border-radius: 8px; width: 100%; transition: 0.2s; }
        .btn-reserve:hover { background-color: var(--salmon-hover); color: white; }

        /* Footer com Layout CVC limpo pedido */
        .main-footer { background-color: #ffffff; border-top: 1px solid #e2e8f0; padding: 40px 0 20px 0; margin-top: 60px; }
        .footer-link { color: #4a5568; text-decoration: none; font-size: 14px; transition: color 0.2s; }
        .footer-link:hover { color: var(--salmon); }
        .footer-heading { font-size: 16px; font-weight: 700; color: var(--terracota); margin-bottom: 15px; }
    </style>
</head>
<body>

    <div class="top-bar py-2 d-none d-md-block">
        <div class="container d-flex justify-content-end">
            <a href="/sobre" class="top-link">Sobre Nós</a>
            <a href="/contato" class="top-link">Contato</a>
        </div>
    </div>

    <header class="main-header">
        <div class="container d-flex justify-content-between align-items-center">
            <a href="/" class="brand-logo">Vacare</a>
            <div class="d-flex align-items-center">
                <a href="/sobre" class="top-link d-inline d-md-none me-3">Sobre</a>
                <a href="/contato" class="top-link d-inline d-md-none">Contato</a>
                <span class="text-muted small d-none d-md-inline fw-semibold" style="color: #718096 !important;">
                    <i class="bi bi-shield-check" style="color: var(--salmon);"></i> Sistema de Viagens Coletivas Verificadas
                </span>
            </div>
        </div>
    </header>

    {% block content %}{% endblock %}

    <footer class="main-footer">
        <div class="container">
            <div class="row g-4 mb-4">
                <div class="col-6 col-md-3">
                    <h5 class="footer-heading">Institucional</h5>
                    <ul class="list-unstyled">
                        <li><a href="/termos" class="footer-link">Termos de Serviço</a></li>
                        <li><a href="/faq" class="footer-link">Dúvidas Frequentes</a></li>
                    </ul>
                </div>
                <div class="col-6 col-md-3">
                    <h5 class="footer-heading">Parcerias</h5>
                    <ul class="list-unstyled">
                        <li><a href="/organizador" class="footer-link fw-bold" style="color: var(--salmon);"><i class="bi bi-plus-circle-fill"></i> Seja um Organizador</a></li>
                    </ul>
                </div>
                <div class="col-6 col-md-3">
                    <h5 class="footer-heading">Atendimento</h5>
                    <ul class="list-unstyled">
                        <li><a href="/contato" class="footer-link">Contato</a></li>
                    </ul>
                </div>
                <div class="col-6 col-md-3 text-md-end">
                    <span class="brand-logo fs-4">Vacare</span>
                    <p class="text-muted small mt-2">Tecnologia para aproximar pessoas e destinos com total segurança.</p>
                </div>
            </div>
            <hr style="border-color: #edf2f7;">
            <div class="row">
                <div class="col-md-12 text-center text-muted small">
                    <p>© 2026 Vacare Tech. Todos os direitos reservados.</p>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
def index():
    content = """
    <section class="hero-section">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-10">
                    <div class="search-container">
                        <h2 class="search-title"><i class="bi bi-search"></i> Encontre sua próxima jornada coletiva</h2>
                        <form action="/" method="GET">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-secondary">Cidade de Embarque</label>
                                    <select class="form-select form-control-custom" name="origem">
                                        <option value="">Todas as cidades</option>
                                        <option value="Belo Horizonte">Belo Horizonte, MG</option>
                                        <option value="Contagem">Contagem, MG</option>
                                    </select>
                                </div>
                                <div class="col-md-5">
                                    <label class="form-label small fw-bold text-secondary">Para onde você quer ir?</label>
                                    <input type="text" class="form-control form-control-custom" name="destino" placeholder="Ex: Ouro Preto, São Thomé, Praias...">
                                </div>
                                <div class="col-md-3 d-flex align-items-end">
                                    <button type="submit" class="btn-search shadow-sm"><i class="bi bi-sliders me-2"></i>Filtrar</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <main class="container my-5">
        <h3 class="fw-bold text-dark mb-4">Experiências Disponíveis ({{ pacotes|length }})</h3>
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            {% for pacote in pacotes %}
            <div class="col">
                <div class="wp-card" data-bs-toggle="modal" data-bs-target="#modal{{ pacote.id }}">
                    <div class="wp-img-container">
                        <img src="{{ pacote.imagem }}" class="wp-img" alt="{{ pacote.destino }}">
                        <span class="badge-category">{{ pacote.categoria }}</span>
                        <span class="badge-duration"><i class="bi bi-moon-stars me-1"></i>{{ pacote.diarias }}</span>
                    </div>
                    <div class="wp-content">
                        <h4 class="wp-destino">{{ pacote.destino }}</h4>
                        <div class="wp-embarque">
                            <i class="bi bi-geo-alt-fill" style="color: var(--salmon);"></i>
                            <span>Embarques: <strong>{{ pacote.embarque }}</strong></span>
                        </div>
                        <p class="wp-description">{{ pacote.descricao }}</p>
                        <div class="wp-footer">
                            <div>
                                <span class="text-muted small d-block" style="font-size:11px; font-weight:700;">PACOTE COMPLETO</span>
                                <span class="wp-price">R$ {{ pacote.preco }}</span>
                            </div>
                            <span class="btn btn-sm btn-outline-secondary px-3 py-2 rounded-pill fw-bold">Ver Detalhes</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal fade" id="modal{{ pacote.id }}" tabindex="-1">
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content border-0 rounded-4 overflow-hidden shadow-lg">
                        <div class="modal-header modal-header-custom p-4">
                            <h5 class="modal-title fw-bold fs-4"><i class="bi bi-compass me-2"></i> Roteiro Detalhado: {{ pacote.destino }}</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body p-4 bg-white">
                            <div class="row g-4">
                                <div class="col-md-6">
                                    <h5 class="fw-bold text-dark mb-3" style="font-size:16px;"><i class="bi bi-info-circle-fill detail-icon"></i>SOBRE A VIAGEM</h5>
                                    <ul class="list-unstyled small text-secondary">
                                        <li class="mb-2"><strong>Duração:</strong> {{ pacote.diarias }}</li>
                                        <li class="mb-2"><strong>Hospedagem:</strong> {{ pacote.hotel }}</li>
                                        <li class="mb-2"><strong>Passeio em Grupo:</strong> {{ pacote.passeio_grupo }}</li>
                                        <li class="mb-2"><strong>Seguro Viagem Incluso:</strong> Cobertura de despesas médicas até <span class="text-dark fw-bold">R$ {{ pacote.seguro_valor }}</span></li>
                                    </ul>
                                    <hr class="my-3">
                                    <h5 class="fw-bold text-dark mb-2" style="font-size:16px;"><i class="bi bi-suit-heart-fill detail-icon"></i>O QUE FAREMOS NO LOCAL</h5>
                                    <p class="small text-muted mb-0">{{ pacote.atividades }}</p>
                                </div>
                                <div class="col-md-6 border-start">
                                    <h5 class="fw-bold text-dark mb-3" style="font-size:16px;"><i class="bi bi-person-badge-fill detail-icon"></i>ANFITRIÃ / ORGANIZADORA</h5>
                                    <p class="mb-1 fw-bold text-dark">{{ pacote.organizadora }}</p>
                                    
                                    <div class="reputation-bar"><div class="reputation-fill" style="width: {{ pacote.reputacao_pct }}"></div></div>
                                    <div class="d-flex justify-content-between align-items-center small mb-3">
                                        <span class="text-secondary">Avaliações Positivas: <strong>{{ pacote.reputacao_pct }}</strong></span>
                                        <span class="text-warning">
                                            {% for i in range(pacote.reputacao_estrelas) %}<i class="bi bi-star-fill"></i>{% endfor %}
                                        </span>
                                    </div>
                                    <div class="p-3 rounded-3 small text-muted border bg-light">
                                        <i class="bi bi-shield-check text-success"></i> Organizadora com identidade e histórico validados pelo ecossistema Vacare Tech.
                                    </div>
                                    <button class="btn-reserve w-100 mt-4 shadow" onclick="alert('Inscrição simulada com sucesso! Vaga pré-reservada no bando.')">Reservar minha Vaga</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </main>
    """
    
    destino_query = request.args.get('destino', '').lower()
    origem_query = request.args.get('origem', '').lower()
    
    pacotes_filtrados = PACOTES
    if destino_query:
        pacotes_filtrados = [p for p in pacotes_filtrados if destino_query in p['destino'].lower()]
    if origem_query:
        pacotes_filtrados = [p for p in pacotes_filtrados if origem_query in p['embarque'].lower()]
        
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content), pacotes=pacotes_filtrados)

# Páginas Institucionais do Header Ativas
@app.route('/sobre')
def sobre():
    content = """
    <div class="container my-5" style="max-width: 800px;">
        <div class="bg-white p-5 rounded-4 shadow-sm border-top border-4" style="border-color: var(--terracota) !important;">
            <h1 class="fw-bold text-terracota mb-4">Sobre Nós</h1>
            <p class="lead">A <strong>Vacare</strong> nasceu para transformar a forma como mulheres se conectam a momentos inesquecíveis.</p>
            <p>Nossa missão inicial é fornecer um ambiente digital totalmente seguro, transparente e de ponta para que organizadoras independentes gerenciem suas excursões, combatendo a informalidade do mercado de turismo.</p>
            <p>Focamos em combinar segurança técnica extrema (como check-in inteligente via QR Code e auditoria de hotéis) com o empoderamento de coletivos e jornadas exclusivas para o público feminino.</p>
            <a href="/" class="btn btn-outline-secondary mt-3"><i class="bi bi-arrow-left me-2"></i>Voltar para o Início</a>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content))

@app.route('/contato')
def contato():
    content = """
    <div class="container my-5" style="max-width: 600px;">
        <div class="bg-white p-5 rounded-4 shadow-sm">
            <h1 class="fw-bold text-dark mb-4"><i class="bi bi-envelope-at" style="color:var(--salmon)"></i> Fale Conosco</h1>
            <form action="#" method="POST" onclick="event.preventDefault(); alert('Mensagem enviada com sucesso no ambiente simulado!');">
                <div class="mb-3">
                    <label class="form-label small fw-bold">Nome</label>
                    <input type="text" class="form-control form-control-custom" placeholder="Seu nome completo" required>
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">E-mail</label>
                    <input type="email" class="form-control form-control-custom" placeholder="seuemail@exemplo.com" required>
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Mensagem</label>
                    <textarea class="form-control form-control-custom" rows="4" placeholder="Como podemos te ajudar?" required></textarea>
                </div>
                <button type="submit" class="btn-search shadow-sm" style="background-color: var(--terracota)">Enviar Mensagem</button>
            </form>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content))

@app.route('/termos')
def termos():
    content = """
    <div class="container my-5" style="max-width: 800px;">
        <div class="bg-white p-5 rounded-4 shadow-sm">
            <h1 class="fw-bold text-dark mb-4">Termos de Serviço</h1>
            <p class="text-muted small">Última atualização: Maio de 2026</p>
            <hr>
            <h5>1. Natureza da Plataforma</h5>
            <p>A Vacare atua estritamente como provedora de tecnologia e intermediadora de anúncios e pagamentos (Marketplace). A execução logística, as reservas de hospedagem e a contratação de transporte rodoviário são de responsabilidade exclusiva da Organizadora independente listada em cada anúncio.</p>
            <h5>2. Proteção e Segurança</h5>
            <p>Exigimos transparência total das organizadoras e fazemos a verificação cadastral de pousadas e roteiros parceiros para mitigar riscos operacionais nas jornadas coletivas.</p>
            <a href="/" class="btn btn-outline-secondary mt-4">Entendi e Aceito</a>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content))

@app.route('/faq')
def faq():
    content = """
    <div class="container my-5" style="max-width: 800px;">
        <h1 class="fw-bold text-dark mb-4 text-center">Dúvidas Frequentes (FAQ)</h1>
        <div class="accordion shadow-sm rounded-3 overflow-hidden" id="accordionFaq">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#faq1">
                        Como a Vacare garante a segurança das excursões exclusivas para mulheres?
                    </button>
                </h2>
                <div id="faq1" class="accordion-collapse collapse show" data-bs-parent="#accordionFaq">
                    <div class="accordion-body">
                        Nós checamos manualmente a existência e idoneidade dos hotéis parceiros, exigimos rastreamento de placa do veículo rodoviário fretado pelas organizadoras e disponibilizamos um painel de check-in em tempo real via QR Code.
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq2">
                        O que está incluso no preço do pacote mostrado no card?
                    </button>
                </h2>
                <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#accordionFaq">
                    <div class="accordion-body">
                        Geralmente inclui transporte executivo ida e volta a partir das cidades de embarque informadas, hospedagem correspondente ao número de diárias e seguro-viagem nominal com cobertura para despesas médicas urgentes.
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content))

@app.route('/organizador')
def organizador():
    content = """
    <div class="container my-5" style="max-width: 700px;">
        <div class="bg-white p-5 rounded-4 shadow-sm text-center">
            <div class="display-4 mb-3" style="color: var(--salmon);"><i class="bi bi-rocket-takeoff-fill"></i></div>
            <h1 class="fw-bold text-dark mb-3">Tire sua excursão do WhatsApp</h1>
            <p class="lead text-muted mb-4">Cadastre suas viagens, use nossa precificação automatizada por lotes, emita QR Codes para check-in e ofereça segurança de verdade para suas passageiras.</p>
            <div class="p-4 bg-light rounded-3 mb-4 text-start">
                <h6 class="fw-bold text-dark"><i class="bi bi-check-circle-fill text-success me-2"></i>O que você ganha entrando para a plataforma:</h6>
                <ul class="mb-0 mt-2 small text-secondary">
                    <li>Sistema automático de cobrança via PIX e Cartão de Crédito.</li>
                    <li>Selo de Hotel Verificado pela nossa auditoria manual avançada.</li>
                    <li>Painel de bordo mobile com sistema integrado de leitura de QR Code.</li>
                </ul>
            </div>
            <button class="btn btn-lg rounded-pill shadow px-5" style="background-color: var(--terracota); color: white; font-weight: bold;" onclick="alert('Inscrições para Organizadores serão integradas com o formulário do Edital Inova UFMG em breve!')">Quero me Cadastrar Gratuitamente</button>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content))

if __name__ == '__main__':
    app.run(debug=True)