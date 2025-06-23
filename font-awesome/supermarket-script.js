// API配置
const API_BASE_URL = 'http://localhost:8000';
const API_TOKEN = 'admin123'; // 简单的认证token

// API请求函数
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${API_TOKEN}`
        }
    };
    
    try {
        const response = await fetch(url, { ...defaultOptions, ...options });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API请求失败:', error);
        showNotification('网络请求失败，请检查后端服务是否运行', 'error');
        throw error;
    }
}

// 全局变量
let currentPage = 'dashboard';
let cartItems = [];
let currentMember = null;

// 模拟数据
const sampleProducts = [
    { id: 'P001', name: '可口可乐', category: 'drink', price: 3.50, stock: 100, status: 'active' },
    { id: 'P002', name: '薯片', category: 'food', price: 8.90, stock: 50, status: 'active' },
    { id: 'P003', name: '牛奶', category: 'drink', price: 6.80, stock: 30, status: 'active' },
    { id: 'P004', name: '面包', category: 'food', price: 5.50, stock: 25, status: 'active' },
    { id: 'P005', name: '洗发水', category: 'household', price: 25.00, stock: 15, status: 'active' }
];

const sampleEmployees = [
    { id: 'E001', name: '张三', position: '收银员', status: 'active', phone: '13800138001' },
    { id: 'E002', name: '李四', position: '理货员', status: 'active', phone: '13800138002' },
    { id: 'E003', name: '王五', position: '店长', status: 'active', phone: '13800138003' }
];

const sampleMembers = [
    { id: 'M001', name: '赵六', phone: '13900139001', level: '黄金会员', points: 1250, joinDate: '2023-01-15' },
    { id: 'M002', name: '钱七', phone: '13900139002', level: '白银会员', points: 680, joinDate: '2023-03-20' },
    { id: 'M003', name: '孙八', phone: '13900139003', level: '普通会员', points: 320, joinDate: '2023-06-10' }
];

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    setupNavigation();
    setupEventListeners();
    await loadDashboardData();
    await loadProductsTable();
    loadInventoryTable();
    loadMembersTable();
    setupPOS();
}

// 导航功能
function setupNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const page = this.dataset.page;
            switchPage(page);
        });
    });
}

function switchPage(page) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // 显示目标页面
    document.getElementById(page).classList.add('active');
    
    // 更新菜单状态
    document.querySelectorAll('.menu-item').forEach(item => item.classList.remove('active'));
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    
    // 更新页面标题
    document.getElementById('page-title').textContent = getPageTitle(page);
    
    currentPage = page;
}

function getPageTitle(page) {
    const titles = {
        dashboard: '仪表板',
        pos: '收银台',
        products: '商品管理',
        inventory: '库存管理',
        employees: '员工管理',
        members: '会员管理',
        reports: '报表统计',
        settings: '系统设置'
    };
    return titles[page] || '页面';
}

// 事件监听器设置
function setupEventListeners() {
    // 菜单切换
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // 模态框关闭
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal-overlay')) {
            closeModal();
        }
    });
    
    // 搜索功能
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            handleGlobalSearch(this.value);
        });
    }
}

// 仪表板数据加载
async function loadDashboardData() {
    try {
        // 从后端API获取统计数据
        const stats = await apiRequest('/stats');
        updateDashboardStats(stats);
    } catch (error) {
        console.error('加载仪表板数据失败:', error);
        // 使用模拟数据作为备用
        updateDashboardStats({
            total_products: sampleProducts.length,
            total_orders: 0,
            total_stock: sampleProducts.reduce((sum, p) => sum + p.stock, 0),
            low_stock_products: sampleProducts.filter(p => p.stock < 10).length
        });
    }
}

function updateDashboardStats(stats) {
    // 更新统计卡片数据
    const statCards = document.querySelectorAll('.stat-card .stat-number');
    if (statCards.length >= 4) {
        statCards[0].textContent = `¥${stats.total_orders * 100 || 12580}`; // 今日销售额
        statCards[1].textContent = stats.total_orders + 1247 || 1247; // 今日客流量
        statCards[2].textContent = stats.total_products || sampleProducts.length; // 商品总数
        statCards[3].textContent = stats.low_stock_products || sampleProducts.filter(p => p.stock < 20).length; // 库存预警
    }
}

// 商品管理功能
async function loadProductsTable() {
    const tbody = document.getElementById('products-table-body');
    if (!tbody) return;
    
    try {
        // 从后端API获取商品数据
        const products = await apiRequest('/products');
        
        tbody.innerHTML = '';
        products.forEach(product => {
            const row = createProductRow(product);
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('加载商品数据失败:', error);
        // 如果API失败，使用模拟数据作为备用
        tbody.innerHTML = '';
        sampleProducts.forEach(product => {
            const row = createProductRow(product);
            tbody.appendChild(row);
        });
    }
}

function createProductRow(product) {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${product.id}</td>
        <td><div class="product-image"><i class="fas fa-box"></i></div></td>
        <td>${product.name}</td>
        <td>${getCategoryName(product.category)}</td>
        <td>¥${product.price.toFixed(2)}</td>
        <td>${product.stock}</td>
        <td><span class="status-badge ${product.status}">${product.status === 'active' ? '在售' : '停售'}</span></td>
        <td>
            <button class="btn-icon" onclick="editProduct('${product.id}')" title="编辑">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon" onclick="deleteProduct('${product.id}')" title="删除">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    `;
    return row;
}

function getCategoryName(category) {
    const categories = {
        food: '食品',
        drink: '饮料',
        household: '日用品'
    };
    return categories[category] || category;
}

// 库存管理功能
function loadInventoryTable() {
    const tbody = document.getElementById('inventory-table-body');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    sampleProducts.forEach(product => {
        const row = createInventoryRow(product);
        tbody.appendChild(row);
    });
}

function createInventoryRow(product) {
    const safetyStock = 20;
    const status = product.stock === 0 ? '缺货' : 
                   product.stock < safetyStock ? '库存不足' : '库存充足';
    const statusClass = product.stock === 0 ? 'out-of-stock' : 
                       product.stock < safetyStock ? 'low-stock' : 'sufficient';
    
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${product.id}</td>
        <td>${product.name}</td>
        <td>${product.stock}</td>
        <td>${safetyStock}</td>
        <td><span class="status-badge ${statusClass}">${status}</span></td>
        <td>${new Date().toLocaleDateString()}</td>
        <td>
            <button class="btn-icon" onclick="adjustStock('${product.id}')" title="调整库存">
                <i class="fas fa-edit"></i>
            </button>
        </td>
    `;
    return row;
}

// 会员管理功能
function loadMembersTable() {
    const tbody = document.getElementById('members-table-body');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    sampleMembers.forEach(member => {
        const row = createMemberRow(member);
        tbody.appendChild(row);
    });
}

function createMemberRow(member) {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${member.id}</td>
        <td>${member.name}</td>
        <td>${member.phone}</td>
        <td>${member.level}</td>
        <td>${member.points}</td>
        <td>${member.joinDate}</td>
        <td>
            <button class="btn-icon" onclick="editMember('${member.id}')" title="编辑">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon" onclick="viewMemberDetails('${member.id}')" title="查看详情">
                <i class="fas fa-eye"></i>
            </button>
        </td>
    `;
    return row;
}

// 收银台功能
function setupPOS() {
    const barcodeInput = document.getElementById('barcode-input');
    if (barcodeInput) {
        barcodeInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addProductToCart(this.value);
                this.value = '';
            }
        });
    }
    
    // 支付方式选择
    const paymentMethods = document.querySelectorAll('.payment-method');
    paymentMethods.forEach(method => {
        method.addEventListener('click', function() {
            paymentMethods.forEach(m => m.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function addProductToCart(barcode) {
    const product = sampleProducts.find(p => p.id === barcode);
    if (!product) {
        showNotification('商品不存在', 'error');
        return;
    }
    
    const existingItem = cartItems.find(item => item.id === product.id);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cartItems.push({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: 1
        });
    }
    
    updateCartDisplay();
    showNotification(`已添加 ${product.name}`, 'success');
}

function updateCartDisplay() {
    const cartContainer = document.getElementById('cart-items');
    if (!cartContainer) return;
    
    cartContainer.innerHTML = '';
    cartItems.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div>
                <h4>${item.name}</h4>
                <p>¥${item.price.toFixed(2)} × ${item.quantity}</p>
            </div>
            <div>
                <span>¥${(item.price * item.quantity).toFixed(2)}</span>
                <button class="btn-icon" onclick="removeFromCart('${item.id}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        cartContainer.appendChild(cartItem);
    });
    
    updateCartSummary();
}

function updateCartSummary() {
    const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const discount = currentMember ? subtotal * 0.05 : 0; // 5% 会员折扣
    const total = subtotal - discount;
    
    document.getElementById('subtotal').textContent = `¥${subtotal.toFixed(2)}`;
    document.getElementById('discount').textContent = `-¥${discount.toFixed(2)}`;
    document.getElementById('total').textContent = `¥${total.toFixed(2)}`;
}

function removeFromCart(productId) {
    cartItems = cartItems.filter(item => item.id !== productId);
    updateCartDisplay();
}

function clearCart() {
    cartItems = [];
    currentMember = null;
    updateCartDisplay();
    document.getElementById('member-info').innerHTML = '<p>请搜索会员信息</p>';
    showNotification('购物车已清空', 'info');
}

function processPayment() {
    if (cartItems.length === 0) {
        showNotification('购物车为空', 'error');
        return;
    }
    
    const total = parseFloat(document.getElementById('total').textContent.replace('¥', ''));
    const paymentMethod = document.querySelector('.payment-method.active').dataset.method;
    
    // 模拟支付处理
    showNotification('支付处理中...', 'info');
    
    setTimeout(() => {
        showNotification('支付成功！', 'success');
        clearCart();
        // 这里可以添加打印小票、更新库存等逻辑
    }, 2000);
}

// 会员搜索功能
function searchMember(query) {
    const member = sampleMembers.find(m => 
        m.phone.includes(query) || m.id.includes(query)
    );
    
    const memberInfo = document.getElementById('member-info');
    if (member) {
        currentMember = member;
        memberInfo.innerHTML = `
            <div class="member-details">
                <h4>${member.name}</h4>
                <p>${member.level}</p>
                <p>积分: ${member.points}</p>
            </div>
        `;
        updateCartSummary();
        showNotification(`欢迎 ${member.name}！`, 'success');
    } else {
        memberInfo.innerHTML = '<p>会员不存在</p>';
        currentMember = null;
        updateCartSummary();
    }
}

// 模态框功能
function showModal(title, content) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-body').innerHTML = content;
    document.getElementById('modal-overlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.remove('active');
}

// 商品管理模态框
function showAddProductModal() {
    const content = `
        <form id="add-product-form">
            <div class="form-group">
                <label>商品名称</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>价格</label>
                <input type="number" name="price" step="0.01" required>
            </div>
            <div class="form-group">
                <label>库存</label>
                <input type="number" name="stock" required>
            </div>
            <div class="form-group">
                <label>分类</label>
                <select name="category" required>
                    <option value="水果">水果</option>
                    <option value="乳制品">乳制品</option>
                    <option value="烘焙">烘焙</option>
                    <option value="饮料">饮料</option>
                    <option value="日用品">日用品</option>
                </select>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn-primary">添加商品</button>
                <button type="button" class="btn-secondary" onclick="closeModal()">取消</button>
            </div>
        </form>
    `;
    
    showModal('添加商品', content);
    
    // 添加表单提交事件
    document.getElementById('add-product-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const productData = {
            name: formData.get('name'),
            price: parseFloat(formData.get('price')),
            stock: parseInt(formData.get('stock')),
            category: formData.get('category')
        };
        
        try {
            await addProduct(productData);
            closeModal();
        } catch (error) {
            console.error('添加商品失败:', error);
        }
    });
}

// 员工管理模态框
function showAddEmployeeModal() {
    const content = `
        <form id="add-employee-form">
            <div class="form-group">
                <label>员工姓名</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>职位</label>
                <select name="position" required>
                    <option value="收银员">收银员</option>
                    <option value="理货员">理货员</option>
                    <option value="店长">店长</option>
                </select>
            </div>
            <div class="form-group">
                <label>手机号</label>
                <input type="tel" name="phone" required>
            </div>
            <div class="form-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">取消</button>
                <button type="submit" class="btn-primary">保存</button>
            </div>
        </form>
    `;
    
    showModal('添加员工', content);
}

// 会员管理模态框
function showAddMemberModal() {
    const content = `
        <form id="add-member-form">
            <div class="form-group">
                <label>会员姓名</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>手机号</label>
                <input type="tel" name="phone" required>
            </div>
            <div class="form-group">
                <label>会员等级</label>
                <select name="level" required>
                    <option value="普通会员">普通会员</option>
                    <option value="白银会员">白银会员</option>
                    <option value="黄金会员">黄金会员</option>
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">取消</button>
                <button type="submit" class="btn-primary">保存</button>
            </div>
        </form>
    `;
    
    showModal('添加会员', content);
}

// 库存管理模态框
function showStockInModal() {
    const content = `
        <form id="stock-in-form">
            <div class="form-group">
                <label>选择商品</label>
                <select name="productId" required>
                    ${sampleProducts.map(p => `<option value="${p.id}">${p.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>入库数量</label>
                <input type="number" name="quantity" required>
            </div>
            <div class="form-group">
                <label>备注</label>
                <textarea name="note"></textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">取消</button>
                <button type="submit" class="btn-primary">确认入库</button>
            </div>
        </form>
    `;
    
    showModal('商品入库', content);
}

function showStockOutModal() {
    const content = `
        <form id="stock-out-form">
            <div class="form-group">
                <label>选择商品</label>
                <select name="productId" required>
                    ${sampleProducts.map(p => `<option value="${p.id}">${p.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>出库数量</label>
                <input type="number" name="quantity" required>
            </div>
            <div class="form-group">
                <label>出库原因</label>
                <select name="reason" required>
                    <option value="销售">销售</option>
                    <option value="损坏">损坏</option>
                    <option value="过期">过期</option>
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">取消</button>
                <button type="submit" class="btn-primary">确认出库</button>
            </div>
        </form>
    `;
    
    showModal('商品出库', content);
}

// 通知系统
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${colors[type]};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 全局搜索功能
function handleGlobalSearch(query) {
    if (query.length < 2) return;
    
    const results = [];
    
    // 搜索商品
    const productResults = sampleProducts.filter(p => 
        p.name.toLowerCase().includes(query.toLowerCase()) ||
        p.id.toLowerCase().includes(query.toLowerCase())
    );
    
    // 搜索员工
    const employeeResults = sampleEmployees.filter(e => 
        e.name.toLowerCase().includes(query.toLowerCase()) ||
        e.id.toLowerCase().includes(query.toLowerCase())
    );
    
    // 搜索会员
    const memberResults = sampleMembers.filter(m => 
        m.name.toLowerCase().includes(query.toLowerCase()) ||
        m.phone.includes(query)
    );
    
    results.push(...productResults, ...employeeResults, ...memberResults);
    
    if (results.length > 0) {
        showSearchResults(results, query);
    }
}

function showSearchResults(results, query) {
    // 这里可以实现搜索结果的显示
    console.log(`搜索 "${query}" 的结果:`, results);
}

// 编辑和删除功能
function editProduct(productId) {
    const product = sampleProducts.find(p => p.id === productId);
    if (product) {
        showNotification(`编辑商品: ${product.name}`, 'info');
    }
}

function deleteProduct(productId) {
    if (confirm('确定要删除这个商品吗？')) {
        showNotification('商品删除成功', 'success');
        loadProductsTable();
    }
}

function editMember(memberId) {
    const member = sampleMembers.find(m => m.id === memberId);
    if (member) {
        showNotification(`编辑会员: ${member.name}`, 'info');
    }
}

function viewMemberDetails(memberId) {
    const member = sampleMembers.find(m => m.id === memberId);
    if (member) {
        const content = `
            <div class="member-detail">
                <h4>${member.name}</h4>
                <p><strong>会员卡号:</strong> ${member.id}</p>
                <p><strong>手机号:</strong> ${member.phone}</p>
                <p><strong>会员等级:</strong> ${member.level}</p>
                <p><strong>积分:</strong> ${member.points}</p>
                <p><strong>注册时间:</strong> ${member.joinDate}</p>
            </div>
        `;
        showModal('会员详情', content);
    }
}

function adjustStock(productId) {
    const product = sampleProducts.find(p => p.id === productId);
    if (product) {
        const content = `
            <form id="adjust-stock-form">
                <div class="form-group">
                    <label>商品名称</label>
                    <input type="text" value="${product.name}" readonly>
                </div>
                <div class="form-group">
                    <label>当前库存</label>
                    <input type="number" value="${product.stock}" readonly>
                </div>
                <div class="form-group">
                    <label>调整数量</label>
                    <input type="number" name="adjustment" required>
                </div>
                <div class="form-group">
                    <label>调整原因</label>
                    <textarea name="reason" required></textarea>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn-secondary" onclick="closeModal()">取消</button>
                    <button type="submit" class="btn-primary">确认调整</button>
                </div>
            </form>
        `;
        showModal('调整库存', content);
    }
}

// 商品管理API函数
async function addProduct(productData) {
    try {
        const newProduct = await apiRequest('/products', {
            method: 'POST',
            body: JSON.stringify(productData)
        });
        showNotification('商品添加成功', 'success');
        await loadProductsTable(); // 重新加载商品列表
        return newProduct;
    } catch (error) {
        showNotification('添加商品失败', 'error');
        throw error;
    }
}

async function updateProduct(productId, productData) {
    try {
        const updatedProduct = await apiRequest(`/products/${productId}`, {
            method: 'PUT',
            body: JSON.stringify(productData)
        });
        showNotification('商品更新成功', 'success');
        await loadProductsTable(); // 重新加载商品列表
        return updatedProduct;
    } catch (error) {
        showNotification('更新商品失败', 'error');
        throw error;
    }
}

async function deleteProduct(productId) {
    if (!confirm('确定要删除这个商品吗？')) {
        return;
    }
    
    try {
        await apiRequest(`/products/${productId}`, {
            method: 'DELETE'
        });
        showNotification('商品删除成功', 'success');
        await loadProductsTable(); // 重新加载商品列表
    } catch (error) {
        showNotification('删除商品失败', 'error');
        throw error;
    }
}

// 导出函数供HTML使用
window.showAddProductModal = showAddProductModal;
window.showAddEmployeeModal = showAddEmployeeModal;
window.showAddMemberModal = showAddMemberModal;
window.showStockInModal = showStockInModal;
window.showStockOutModal = showStockOutModal;
window.closeModal = closeModal;
window.clearCart = clearCart;
window.processPayment = processPayment;
window.editProduct = editProduct;
window.deleteProduct = deleteProduct;
window.editMember = editMember;
window.viewMemberDetails = viewMemberDetails;
window.adjustStock = adjustStock;