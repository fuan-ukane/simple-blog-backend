// 辅助函数
function getToken() {
    return localStorage.getItem('access_token');
}

function setToken(token) {
    localStorage.setItem('access_token', token);
}

function clearToken() {
    localStorage.removeItem('access_token');
}

async function apiFetch(url, method = 'GET', body = null, auth = true) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth && getToken()) {
        headers['Authorization'] = `Bearer ${getToken()}`;
    }
    const config = { method, headers };
    if (body) {
        config.body = JSON.stringify(body);
    }
    const response = await fetch(url, config);
    if (response.status === 204) return null;
    const data = await response.json();
    if (response.ok) {
        return data;
    } else {
        throw new Error(data.detail || '请求失败');
    }
}

async function login() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    if (!username || !password) {
        document.getElementById('message').innerText = '用户名和密码不能为空';
        return;
    }

    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        const response = await fetch('/api/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            setToken(data.access_token);
            window.location.href = '/';
        } else {
            document.getElementById('message').innerText = data.detail || '登录失败';
        }
    } catch (e) {
        document.getElementById('message').innerText = e.message;
    }
}

async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    try {
        const data = await apiFetch('/api/register', 'POST', { username, password }, false);
        alert('注册成功，请登录');
    } catch (e) {
        document.getElementById('message').innerText = e.message;
    }
}

// 文章列表加载（索引页）
async function loadArticles(page = 1) {
    try {
        const data = await apiFetch(`/api/articles?page=${page}&page_size=5`, 'GET', null, false);
        const container = document.getElementById('articles');
        container.innerHTML = '';
        data.items.forEach(article => {
            const div = document.createElement('div');
            div.className = 'article';
            div.innerHTML = `<h3>${article.title}</h3><p>${article.tags.join(', ')}</p>`;
            div.onclick = () => location.href = `/article.html?id=${article.id}`;
            container.appendChild(div);
        });
        // 简单分页
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';
        for (let i = 1; i <= Math.ceil(data.total / data.page_size); i++) {
            const btn = document.createElement('button');
            btn.innerText = i;
            btn.onclick = () => loadArticles(i);
            pagination.appendChild(btn);
        }
    } catch (e) {
        console.error(e);
    }
}

// 文章保存（新建或编辑）
async function saveArticle() {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const tags = document.getElementById('tags').value.split(',').map(t => t.trim()).filter(t => t);
    const articleId = new URLSearchParams(window.location.search).get('id');
    try {
        if (articleId) {
            await apiFetch(`/api/articles/${articleId}`, 'PUT', { title, content, tags });
        } else {
            await apiFetch('/api/articles', 'POST', { title, content, tags });
        }
        alert('保存成功');
        window.location.href = '/';
    } catch (e) {
        alert(e.message);
    }
}

// 页面加载时执行
if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
    loadArticles();
} else if (window.location.pathname === '/article.html') {
    const id = new URLSearchParams(window.location.search).get('id');
    if (id) {
        // 加载文章详情填充表单
        apiFetch(`/api/articles/${id}`, 'GET', null, false)
            .then(data => {
                document.getElementById('formTitle').innerText = '编辑文章';
                document.getElementById('title').value = data.title;
                document.getElementById('content').value = data.content;
                document.getElementById('tags').value = data.tags.join(', ');
            })
            .catch(err => alert(err.message));
    }
}