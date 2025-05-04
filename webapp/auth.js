// Configurações dos provedores de autenticação
const config = {
    google: {
        clientId: 'SEU_CLIENT_ID_GOOGLE',
        redirectUri: 'http://localhost:5000/auth/google/callback'
    },
    facebook: {
        appId: 'SEU_APP_ID_FACEBOOK',
        redirectUri: 'http://localhost:5000/auth/facebook/callback'
    },
    twitter: {
        clientId: 'SEU_CLIENT_ID_TWITTER',
        redirectUri: 'http://localhost:5000/auth/twitter/callback'
    }
};

// Função para autenticação com Google
function loginWithGoogle() {
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${config.google.clientId}&redirect_uri=${config.google.redirectUri}&response_type=code&scope=email profile&access_type=offline&prompt=consent`;
    window.location.href = authUrl;
}

// Função para autenticação com Facebook
function loginWithFacebook() {
    const authUrl = `https://www.facebook.com/v12.0/dialog/oauth?client_id=${config.facebook.appId}&redirect_uri=${config.facebook.redirectUri}&scope=email,public_profile`;
    window.location.href = authUrl;
}

// Função para autenticação com Twitter
function loginWithTwitter() {
    const authUrl = `https://twitter.com/i/oauth2/authorize?response_type=code&client_id=${config.twitter.clientId}&redirect_uri=${config.twitter.redirectUri}&scope=tweet.read users.read&state=state&code_challenge=challenge&code_challenge_method=plain`;
    window.location.href = authUrl;
}

// Função para processar o callback de autenticação
async function handleAuthCallback(provider, code) {
    try {
        const response = await fetch(`/auth/${provider}/callback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });

        if (response.ok) {
            const data = await response.json();
            // ARMAZENAMENTO COMPLETO DOS DADOS (modificação importante)
            localStorage.setItem('authToken', data.access_token);
            localStorage.setItem('userData', JSON.stringify({
                id: data.user.id,
                name: data.user.username,
                username: data.user.username,
                email: data.user.email,
                provider: provider
            }));
            
            window.location.href = '/feed';
        } else {
            throw new Error('Falha na autenticação');
        }
    } catch (error) {
        console.error('Erro na autenticação:', error);
        alert('Erro ao fazer login. Por favor, tente novamente.');
    }
}

// Verificar se estamos na página de callback
if (window.location.pathname.includes('/auth/')) {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const provider = window.location.pathname.split('/')[2];
    
    if (code) {
        handleAuthCallback(provider, code);
    }
}

// Função para verificar se o usuário está autenticado
function isAuthenticated() {
    return !!localStorage.getItem('authToken');
}

// Função para fazer logout
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    window.location.href = '/index.html';
}

// Função para fazer login com email e senha
async function loginWithEmailAndPassword(email, password) {
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // ARMAZENE TODOS OS DADOS NECESSÁRIOS (modificação importante)
            localStorage.setItem('userData', JSON.stringify({
                id: data.user.id,
                name: data.user.username,
                username: data.user.username,
                email: data.user.email
            }));
            
            // Redirecionar para a página de chat
            window.location.href = '/chat';
        } else {
            throw new Error(data.error || 'Erro ao fazer login');
        }
    } catch (error) {
        console.error('Erro no login:', error);
        alert(error.message || 'Erro ao fazer login. Por favor, tente novamente.');
    }
}

// Adicionar event listener para o formulário de login
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginWithEmailAndPassword(email, password);
        });
    }
}); 