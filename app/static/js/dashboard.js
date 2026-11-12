/**
 * Employee Data Management — Enterprise Dashboard Client
 * With Full Session Authentication & User Profile Management
 */

(function () {
  // Application State
  const state = {
    currentUser: null,
    search: '',
    dept: 'ALL',
    gender: 'ALL',
    sortBy: 'Emp_no',
    sortOrder: 'ASC',
    page: 1,
    pageSize: 10,
    totalRecords: 0,
    totalPages: 1,
    activeEmployeeId: null,
  };

  // DOM Elements
  const dom = {
    // Views
    loginView: document.getElementById('login-view'),
    appView: document.getElementById('app-view'),

    // Login Form Elements
    formLogin: document.getElementById('form-login'),
    loginUsername: document.getElementById('login-username'),
    loginPassword: document.getElementById('login-password'),
    loginErrorAlert: document.getElementById('login-error-alert'),
    btnTogglePassword: document.getElementById('btn-toggle-password'),
    btnSubmitLogin: document.getElementById('btn-submit-login'),

    // Header User Elements
    btnOpenProfile: document.getElementById('btn-open-profile'),
    headerUserAvatar: document.getElementById('header-user-avatar'),
    headerUserName: document.getElementById('header-user-name'),
    headerUserBadge: document.getElementById('header-user-badge'),
    btnLogout: document.getElementById('btn-logout'),

    // Profile Modal Elements
    modalProfile: document.getElementById('modal-profile'),
    profileAvatar: document.getElementById('profile-avatar'),
    profileFullName: document.getElementById('profile-fullname'),
    profileRoleTitle: document.getElementById('profile-role-title'),
    profileBadge: document.getElementById('profile-badge'),
    profileUsername: document.getElementById('profile-username'),
    profileDept: document.getElementById('profile-dept'),
    profileEmail: document.getElementById('profile-email'),
    profilePermissions: document.getElementById('profile-permissions-container'),
    btnProfileLogout: document.getElementById('btn-profile-logout'),

    // System Status & KPIs
    dbStatusPill: document.getElementById('db-status-pill'),
    dbBackendLabel: document.getElementById('db-backend-label'),
    kpiHeadcount: document.getElementById('kpi-headcount'),
    kpiPayroll: document.getElementById('kpi-payroll'),
    kpiAvgSalary: document.getElementById('kpi-avg-salary'),
    kpiDepts: document.getElementById('kpi-depts'),
    deptBreakdownList: document.getElementById('department-breakdown-list'),
    genderPills: document.getElementById('gender-distribution-pills'),
    salaryTierPills: document.getElementById('salary-tier-pills'),

    // Table & Filters
    filterSearch: document.getElementById('filter-search'),
    filterDept: document.getElementById('filter-dept'),
    filterGender: document.getElementById('filter-gender'),
    pageSizeSelect: document.getElementById('page-size-select'),
    btnResetFilters: document.getElementById('btn-reset-filters'),
    employeeTableBody: document.getElementById('employee-table-body'),
    recordSummaryText: document.getElementById('record-summary-text'),
    pageIndicatorText: document.getElementById('page-indicator-text'),
    btnPrevPage: document.getElementById('btn-prev-page'),
    btnNextPage: document.getElementById('btn-next-page'),

    // Notification
    toastContainer: document.getElementById('toast-container'),

    // Modals
    modalAdd: document.getElementById('modal-add'),
    modalEdit: document.getElementById('modal-edit'),
    modalLookup: document.getElementById('modal-lookup'),
    modalDelete: document.getElementById('modal-delete'),
    formAdd: document.getElementById('form-add-employee'),
    formEdit: document.getElementById('form-edit-employee'),
    btnOpenAdd: document.getElementById('btn-open-add'),
    btnOpenLookup: document.getElementById('btn-open-lookup'),
    btnExportCsv: document.getElementById('btn-export-csv'),
    btnConfirmDelete: document.getElementById('btn-confirm-delete'),
    deleteEmpNo: document.getElementById('delete-emp-no'),
    deleteEmpLabel: document.getElementById('delete-emp-label'),
    lookupInput: document.getElementById('lookup-emp-no-input'),
    btnPerformLookup: document.getElementById('btn-perform-lookup'),
    lookupResultContainer: document.getElementById('lookup-result-container'),
  };

  // Formatters
  const currencyFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  });

  const numberFormatter = new Intl.NumberFormat('en-US');

  // Toast System
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    dom.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(8px)';
      toast.style.transition = 'all 0.2s ease-out';
      setTimeout(() => toast.remove(), 200);
    }, 3200);
  }

  // API Client
  async function apiFetch(endpoint, options = {}) {
    options.credentials = 'include'; // Ensure cookies are sent
    try {
      const response = await fetch(endpoint, options);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Request failed with status ${response.status}`);
      }
      return await response.json();
    } catch (err) {
      console.error(`API Error on ${endpoint}:`, err);
      throw err;
    }
  }

  // =========================================================================
  // AUTHENTICATION LOGIC
  // =========================================================================

  async function checkAuth() {
    try {
      const user = await apiFetch('/api/auth/me');
      setAuthenticated(user);
    } catch (err) {
      setUnauthenticated();
    }
  }

  function setAuthenticated(user) {
    state.currentUser = user;
    dom.loginView.style.display = 'none';
    dom.appView.style.display = 'flex';

    // Update Header Profile Badge
    dom.headerUserName.textContent = user.username;
    dom.headerUserBadge.textContent = user.badge;
    dom.headerUserAvatar.textContent = user.name ? user.name.charAt(0).toUpperCase() : 'U';

    refreshAll();
  }

  function setUnauthenticated() {
    state.currentUser = null;
    dom.appView.style.display = 'none';
    dom.loginView.style.display = 'flex';
  }

  // Login Submit
  dom.formLogin.addEventListener('submit', async (e) => {
    e.preventDefault();
    dom.loginErrorAlert.style.display = 'none';
    dom.btnSubmitLogin.disabled = true;
    dom.btnSubmitLogin.textContent = 'Verifying...';

    const username = dom.loginUsername.value.trim();
    const password = dom.loginPassword.value.trim();

    try {
      const data = await apiFetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      setAuthenticated(data.user);
      showToast(`Welcome back, ${data.user.name}!`);
    } catch (err) {
      dom.loginErrorAlert.textContent = err.message || 'Invalid username or password';
      dom.loginErrorAlert.style.display = 'block';
    } finally {
      dom.btnSubmitLogin.disabled = false;
      dom.btnSubmitLogin.textContent = 'Sign In';
    }
  });

  // Quick fill credential chips
  document.querySelectorAll('.btn-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      dom.loginUsername.value = chip.dataset.user;
      dom.loginPassword.value = chip.dataset.pass;
      dom.loginErrorAlert.style.display = 'none';
    });
  });

  // Password visibility toggle
  dom.btnTogglePassword.addEventListener('click', () => {
    if (dom.loginPassword.type === 'password') {
      dom.loginPassword.type = 'text';
      dom.btnTogglePassword.textContent = '🔒';
    } else {
      dom.loginPassword.type = 'password';
      dom.btnTogglePassword.textContent = '👁️';
    }
  });

  // Logout Actions
  async function performLogout() {
    try {
      await apiFetch('/api/auth/logout', { method: 'POST' });
    } catch (err) {
      console.warn('Logout notification error:', err);
    }
    closeModal(dom.modalProfile);
    setUnauthenticated();
    showToast('Signed out successfully.');
  }

  dom.btnLogout.addEventListener('click', performLogout);
  dom.btnProfileLogout.addEventListener('click', performLogout);

  // Profile Modal
  dom.btnOpenProfile.addEventListener('click', () => {
    if (!state.currentUser) return;
    const u = state.currentUser;
    dom.profileAvatar.textContent = u.name ? u.name.charAt(0).toUpperCase() : 'U';
    dom.profileFullName.textContent = u.name;
    dom.profileRoleTitle.textContent = u.role;
    dom.profileBadge.textContent = u.badge;
    dom.profileUsername.textContent = u.username;
    dom.profileDept.textContent = u.department;
    dom.profileEmail.textContent = u.email;

    // Render permissions
    const permHtml = (u.permissions || []).map((perm) => `
      <div class="demographic-pill" style="font-size: 0.78rem;">
        <span style="color: var(--success); font-weight: bold;">✔</span>
        <strong>${escapeHtml(perm)}</strong>
      </div>
    `).join('');
    dom.profilePermissions.innerHTML = permHtml;

    openModal(dom.modalProfile);
  });

  // =========================================================================
  // DASHBOARD DATA LOGIC
  // =========================================================================

  // Check Database Status
  async function fetchHealth() {
    try {
      const health = await apiFetch('/api/health');
      dom.dbBackendLabel.textContent = `${health.database_backend} (${health.status})`;
      dom.dbStatusPill.className = `db-pill connected-${health.database_backend.toLowerCase()}`;
    } catch (err) {
      dom.dbBackendLabel.textContent = 'DATABASE OFFLINE';
      dom.dbStatusPill.className = 'db-pill';
    }
  }

  // Fetch KPIs
  async function fetchStats() {
    try {
      const stats = await apiFetch('/api/stats');
      dom.kpiHeadcount.textContent = numberFormatter.format(stats.total_employees);
      dom.kpiPayroll.textContent = currencyFormatter.format(stats.total_payroll);
      dom.kpiAvgSalary.textContent = currencyFormatter.format(stats.average_salary);
      dom.kpiDepts.textContent = stats.departments_count;

      renderDepartmentBreakdown(stats.department_distribution, stats.total_employees);
      renderDemographics(stats.gender_distribution, stats.salary_ranges);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  }

  function renderDepartmentBreakdown(departments, totalEmployees) {
    if (!departments || departments.length === 0) {
      dom.deptBreakdownList.innerHTML = '<div class="text-muted text-sm">No department data available.</div>';
      return;
    }

    const html = departments.map((dept) => {
      const percentage = totalEmployees > 0 ? Math.round((dept.count / totalEmployees) * 100) : 0;
      return `
        <div class="dept-bar-row">
          <div class="dept-bar-info">
            <span class="dept-bar-name">${escapeHtml(dept.Dept)}</span>
            <span class="dept-bar-meta">
              ${dept.count} emp (${percentage}%) &bull; Avg: ${currencyFormatter.format(dept.avg_salary)}
            </span>
          </div>
          <div class="dept-progress-track">
            <div class="dept-progress-fill" style="width: ${percentage}%"></div>
          </div>
        </div>
      `;
    }).join('');

    dom.deptBreakdownList.innerHTML = html;
  }

  function renderDemographics(genderDist, salaryRanges) {
    const genderLabels = { M: 'Male (M)', F: 'Female (F)', O: 'Other (O)' };
    const genderHtml = Object.entries(genderDist).map(([key, count]) => `
      <div class="demographic-pill">
        <span>${genderLabels[key] || key}:</span>
        <strong>${count}</strong>
      </div>
    `).join('');
    dom.genderPills.innerHTML = genderHtml || '<span class="text-muted text-sm">None</span>';

    const salaryHtml = Object.entries(salaryRanges).map(([tier, count]) => `
      <div class="demographic-pill">
        <span>${tier}:</span>
        <strong>${count}</strong>
      </div>
    `).join('');
    dom.salaryTierPills.innerHTML = salaryHtml || '<span class="text-muted text-sm">None</span>';
  }

  // Load Departments for Filter Dropdown
  async function fetchDepartments() {
    try {
      const data = await apiFetch('/api/departments');
      const currentSelected = dom.filterDept.value;
      let optionsHtml = '<option value="ALL">All Departments</option>';
      data.departments.forEach((dept) => {
        optionsHtml += `<option value="${escapeHtml(dept)}">${escapeHtml(dept)}</option>`;
      });
      dom.filterDept.innerHTML = optionsHtml;
      if (data.departments.includes(currentSelected)) {
        dom.filterDept.value = currentSelected;
      }
    } catch (err) {
      console.error('Failed to load departments:', err);
    }
  }

  // Fetch Employee Table
  async function fetchEmployees() {
    const params = new URLSearchParams({
      search: state.search,
      dept: state.dept,
      gender: state.gender,
      sort_by: state.sortBy,
      sort_order: state.sortOrder,
      page: state.page,
      page_size: state.pageSize,
    });

    try {
      const data = await apiFetch(`/api/employees?${params.toString()}`);
      state.totalRecords = data.total;
      state.totalPages = data.total_pages;

      renderTable(data.items);
      renderPagination(data);
    } catch (err) {
      dom.employeeTableBody.innerHTML = `
        <tr><td colspan="8" class="text-center text-danger py-4">Failed to load employee records.</td></tr>
      `;
    }
  }

  function renderTable(items) {
    if (!items || items.length === 0) {
      dom.employeeTableBody.innerHTML = `
        <tr><td colspan="8" class="text-center text-muted py-4">No employees matching criteria.</td></tr>
      `;
      return;
    }

    const html = items.map((emp) => `
      <tr>
        <td><span class="emp-id-badge">#${emp.Emp_no}</span></td>
        <td><strong>${escapeHtml(emp.Name)}</strong></td>
        <td><span class="gender-tag gender-${emp.Gender}">${emp.Gender}</span></td>
        <td>${emp.Age}</td>
        <td>${escapeHtml(emp.Role)}</td>
        <td>${escapeHtml(emp.Dept)}</td>
        <td class="salary-cell">${currencyFormatter.format(emp.Salary)}</td>
        <td>
          <div class="table-actions">
            <button class="btn btn-secondary btn-sm action-view" data-id="${emp.Emp_no}" title="View Record">View</button>
            <button class="btn btn-secondary btn-sm action-edit" data-id="${emp.Emp_no}" title="Configure Record">Edit</button>
            <button class="btn btn-ghost btn-sm text-danger action-delete" data-id="${emp.Emp_no}" data-name="${escapeHtml(emp.Name)}" title="Remove Record">Delete</button>
          </div>
        </td>
      </tr>
    `).join('');

    dom.employeeTableBody.innerHTML = html;
    updateSortIndicators();
  }

  function renderPagination(data) {
    const start = data.total === 0 ? 0 : (data.page - 1) * data.page_size + 1;
    const end = Math.min(data.page * data.page_size, data.total);
    dom.recordSummaryText.textContent = `Showing ${start}-${end} of ${data.total} employees`;
    dom.pageIndicatorText.textContent = `Page ${data.page} of ${Math.max(1, data.total_pages)}`;

    dom.btnPrevPage.disabled = data.page <= 1;
    dom.btnNextPage.disabled = data.page >= data.total_pages;
  }

  function updateSortIndicators() {
    document.querySelectorAll('.data-table th.sortable').forEach((th) => {
      const col = th.dataset.sort;
      const indicator = th.querySelector('.sort-indicator');
      if (col === state.sortBy) {
        indicator.textContent = state.sortOrder === 'ASC' ? ' ↑' : ' ↓';
      } else {
        indicator.textContent = '';
      }
    });
  }

  // Modals Logic
  function openModal(modalEl) {
    modalEl.classList.add('active');
  }

  function closeModal(modalEl) {
    modalEl.classList.remove('active');
  }

  document.querySelectorAll('[data-close]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const targetId = e.currentTarget.dataset.close;
      const modalEl = document.getElementById(targetId);
      if (modalEl) closeModal(modalEl);
    });
  });

  window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-backdrop')) {
      closeModal(e.target);
    }
  });

  // Modal Open Triggers
  dom.btnOpenAdd.addEventListener('click', () => {
    dom.formAdd.reset();
    openModal(dom.modalAdd);
  });

  dom.btnOpenLookup.addEventListener('click', () => {
    dom.lookupInput.value = '';
    dom.lookupResultContainer.innerHTML = '<div class="empty-state text-muted text-center py-4">Enter an ID above to view details.</div>';
    openModal(dom.modalLookup);
  });

  // Table Row Actions
  dom.employeeTableBody.addEventListener('click', async (e) => {
    const target = e.target.closest('button');
    if (!target) return;

    const empId = target.dataset.id;
    if (target.classList.contains('action-view')) {
      openLookupProfile(empId);
    } else if (target.classList.contains('action-edit')) {
      openEditModal(empId);
    } else if (target.classList.contains('action-delete')) {
      const empName = target.dataset.name;
      openDeleteConfirmation(empId, empName);
    }
  });

  // Lookup / Profile
  async function openLookupProfile(empId) {
    openModal(dom.modalLookup);
    dom.lookupInput.value = empId;
    await performLookup(empId);
  }

  dom.btnPerformLookup.addEventListener('click', () => {
    const id = dom.lookupInput.value.trim();
    if (id) performLookup(id);
  });

  dom.lookupInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const id = dom.lookupInput.value.trim();
      if (id) performLookup(id);
    }
  });

  async function performLookup(empId) {
    dom.lookupResultContainer.innerHTML = '<div class="text-center py-4 text-muted">Searching database...</div>';
    try {
      const emp = await apiFetch(`/api/employees/${empId}`);
      dom.lookupResultContainer.innerHTML = `
        <div class="profile-card">
          <div class="profile-header">
            <div>
              <h4 style="font-size: 1.15rem; font-weight: 700;">${escapeHtml(emp.Name)}</h4>
              <span class="text-muted text-sm">${escapeHtml(emp.Role)} &bull; ${escapeHtml(emp.Dept)}</span>
            </div>
            <span class="emp-id-badge">ID: #${emp.Emp_no}</span>
          </div>
          <div class="profile-details-grid">
            <div>
              <div class="profile-item-label">Gender</div>
              <div class="profile-item-value">${emp.Gender === 'M' ? 'Male (M)' : emp.Gender === 'F' ? 'Female (F)' : 'Other (O)'}</div>
            </div>
            <div>
              <div class="profile-item-label">Age</div>
              <div class="profile-item-value">${emp.Age} years old</div>
            </div>
            <div>
              <div class="profile-item-label">Department</div>
              <div class="profile-item-value">${escapeHtml(emp.Dept)}</div>
            </div>
            <div>
              <div class="profile-item-label">Annual Salary</div>
              <div class="profile-item-value text-success" style="font-family: var(--font-mono);">${currencyFormatter.format(emp.Salary)}</div>
            </div>
          </div>
        </div>
      `;
    } catch (err) {
      dom.lookupResultContainer.innerHTML = `
        <div class="text-center py-4 text-danger font-medium">Employee ID #${empId} not found in database.</div>
      `;
    }
  }

  // Edit Modal
  async function openEditModal(empId) {
    try {
      const emp = await apiFetch(`/api/employees/${empId}`);
      document.getElementById('edit-emp-no').value = emp.Emp_no;
      document.getElementById('edit-emp-no-label').textContent = `#${emp.Emp_no}`;
      document.getElementById('edit-name').value = emp.Name;
      document.getElementById('edit-gender').value = emp.Gender;
      document.getElementById('edit-age').value = emp.Age;
      document.getElementById('edit-role').value = emp.Role;
      document.getElementById('edit-dept').value = emp.Dept;
      document.getElementById('edit-salary').value = emp.Salary;
      openModal(dom.modalEdit);
    } catch (err) {
      showToast('Could not load employee details for editing', 'error');
    }
  }

  dom.formEdit.addEventListener('submit', async (e) => {
    e.preventDefault();
    const empNo = document.getElementById('edit-emp-no').value;
    const payload = {
      Name: document.getElementById('edit-name').value.trim(),
      Gender: document.getElementById('edit-gender').value,
      Age: parseInt(document.getElementById('edit-age').value, 10),
      Role: document.getElementById('edit-role').value.trim(),
      Dept: document.getElementById('edit-dept').value.trim(),
      Salary: parseFloat(document.getElementById('edit-salary').value),
    };

    try {
      await apiFetch(`/api/employees/${empNo}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      closeModal(dom.modalEdit);
      showToast(`Employee #${empNo} updated successfully!`);
      refreshAll();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Add Modal
  dom.formAdd.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      Emp_no: parseInt(document.getElementById('add-emp-no').value, 10),
      Name: document.getElementById('add-name').value.trim(),
      Gender: document.getElementById('add-gender').value,
      Age: parseInt(document.getElementById('add-age').value, 10),
      Role: document.getElementById('add-role').value.trim(),
      Dept: document.getElementById('add-dept').value.trim(),
      Salary: parseFloat(document.getElementById('add-salary').value),
    };

    try {
      await apiFetch('/api/employees', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      closeModal(dom.modalAdd);
      dom.formAdd.reset();
      showToast(`Employee #${payload.Emp_no} (${payload.Name}) added successfully!`);
      refreshAll();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Delete Confirmation
  function openDeleteConfirmation(empId, empName) {
    dom.deleteEmpNo.value = empId;
    dom.deleteEmpLabel.textContent = `#${empId} (${empName})`;
    openModal(dom.modalDelete);
  }

  dom.btnConfirmDelete.addEventListener('click', async () => {
    const empId = dom.deleteEmpNo.value;
    try {
      await apiFetch(`/api/employees/${empId}`, { method: 'DELETE' });
      closeModal(dom.modalDelete);
      showToast(`Employee #${empId} removed from database.`);
      refreshAll();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Filter & Search Handlers
  let searchTimeout;
  dom.filterSearch.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      state.search = e.target.value.trim();
      state.page = 1;
      fetchEmployees();
    }, 250);
  });

  dom.filterDept.addEventListener('change', (e) => {
    state.dept = e.target.value;
    state.page = 1;
    fetchEmployees();
  });

  dom.filterGender.addEventListener('change', (e) => {
    state.gender = e.target.value;
    state.page = 1;
    fetchEmployees();
  });

  dom.pageSizeSelect.addEventListener('change', (e) => {
    state.pageSize = parseInt(e.target.value, 10);
    state.page = 1;
    fetchEmployees();
  });

  dom.btnResetFilters.addEventListener('click', () => {
    state.search = '';
    state.dept = 'ALL';
    state.gender = 'ALL';
    state.page = 1;
    dom.filterSearch.value = '';
    dom.filterDept.value = 'ALL';
    dom.filterGender.value = 'ALL';
    fetchEmployees();
  });

  document.querySelectorAll('.data-table th.sortable').forEach((th) => {
    th.addEventListener('click', () => {
      const col = th.dataset.sort;
      if (state.sortBy === col) {
        state.sortOrder = state.sortOrder === 'ASC' ? 'DESC' : 'ASC';
      } else {
        state.sortBy = col;
        state.sortOrder = 'ASC';
      }
      fetchEmployees();
    });
  });

  dom.btnPrevPage.addEventListener('click', () => {
    if (state.page > 1) {
      state.page--;
      fetchEmployees();
    }
  });

  dom.btnNextPage.addEventListener('click', () => {
    if (state.page < state.totalPages) {
      state.page++;
      fetchEmployees();
    }
  });

  // Export CSV
  dom.btnExportCsv.addEventListener('click', () => {
    window.location.href = '/api/export/csv';
  });

  // Refresh All
  function refreshAll() {
    fetchHealth();
    fetchStats();
    fetchDepartments();
    fetchEmployees();
  }

  // HTML Escape Helper
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // Start by checking authentication
  checkAuth();
})();
