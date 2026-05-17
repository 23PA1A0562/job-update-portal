document.addEventListener('DOMContentLoaded', () => {
    let currentUser = null;

    // Elements
    const employeeSelect = document.getElementById('employee-select');
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    const pageTitle = document.getElementById('page-title');
    const toast = document.getElementById('toast');

    // Forms & Inputs
    const leaveForm = document.getElementById('leave-form');
    const laptopForm = document.getElementById('laptop-form');
    const idCardForm = document.getElementById('id-card-form');
    
    const leaveTypeSelect = document.getElementById('leave-type');
    const maternityOption = document.getElementById('maternity-option');
    const doctorDescGroup = document.getElementById('doctor-desc-group');
    const doctorDescInput = document.getElementById('doctor-desc');
    const leaveDaysInput = document.getElementById('leave-days');
    const leaveStartDateInput = document.getElementById('leave-start-date');
    const leaveEndDateInput = document.getElementById('leave-end-date');
    const pdfUploadGroup = document.getElementById('pdf-upload-group');
    const medicalPdfInput = document.getElementById('medical-pdf');
    const fileNameDisplay = document.getElementById('file-name-display');
    const submitLeaveBtn = document.getElementById('submit-leave-btn');

    // AI Verification Elements
    const aiVerificationBox = document.getElementById('ai-verification-box');
    const aiLoader = document.getElementById('ai-loader');
    const aiResult = document.getElementById('ai-result');

    // HR Modal Elements
    const hrModal = document.getElementById('hr-modal');
    const hrRequestForm = document.getElementById('hr-request-form');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const hrReqType = document.getElementById('hr-req-type');
    const hrReqDays = document.getElementById('hr-req-days');

    // Password Toggle
    const togglePasswordBtn = document.getElementById('toggle-password');
    const wifiPasswordSpan = document.getElementById('wifi-password');

    let pdfVerified = false; // State flag

    // Initialize Application
    function init() {
        populateEmployeeDropdown();
        
        if (appState.employees.length > 0) {
            employeeSelect.value = appState.employees[0].id;
            loadEmployee(appState.employees[0].id);
        }

        setupEventListeners();
    }

    function populateEmployeeDropdown() {
        employeeSelect.innerHTML = '';
        appState.employees.forEach(emp => {
            const option = document.createElement('option');
            option.value = emp.id;
            option.textContent = emp.name;
            employeeSelect.appendChild(option);
        });
    }

    function loadEmployee(id) {
        currentUser = appState.employees.find(emp => emp.id === id);
        if (!currentUser) return;

        // Reset Leave Form States
        leaveForm.reset();
        doctorDescGroup.style.display = 'none';
        pdfUploadGroup.style.display = 'none';
        aiVerificationBox.classList.add('hidden');
        submitLeaveBtn.disabled = false;
        pdfVerified = false;

        // Header & Dashboard
        document.getElementById('header-name').textContent = currentUser.name;
        document.getElementById('header-avatar').src = currentUser.avatar;
        document.getElementById('welcome-name').textContent = currentUser.name.split(' ')[0];
        
        document.getElementById('profile-name').textContent = currentUser.name;
        document.getElementById('profile-role').textContent = currentUser.role;
        document.getElementById('profile-id').textContent = currentUser.id;
        document.getElementById('profile-avatar').src = currentUser.avatar;
        
        // Gender specific UI
        document.getElementById('profile-gender').textContent = currentUser.gender;
        if (currentUser.gender === 'Female') {
            maternityOption.style.display = 'block';
            document.getElementById('maternity-balance-container').style.display = 'flex';
        } else {
            maternityOption.style.display = 'none';
            document.getElementById('maternity-balance-container').style.display = 'none';
        }

        document.getElementById('wifi-network').textContent = currentUser.credentials.wifi;
        document.getElementById('wifi-password').textContent = currentUser.credentials.wifiPass;
        wifiPasswordSpan.classList.add('blurred');
        wifiPasswordSpan.classList.remove('unblurred');
        togglePasswordBtn.innerHTML = '<i class="fa-solid fa-eye"></i>';

        updateLeaveUI();
        updatePerformanceUI();
    }

    function updateLeaveUI() {
        const { paid, casual, maternity } = currentUser.leaveBalance;
        
        document.getElementById('paid-balance').textContent = paid;
        document.getElementById('casual-balance').textContent = casual;

        setProgress('paid-progress', paid, 20);
        setProgress('casual-progress', casual, 10);

        if (currentUser.gender === 'Female') {
            document.getElementById('maternity-balance').textContent = maternity;
            setProgress('maternity-progress', maternity, 180);
        }

        const historyList = document.getElementById('leave-history');
        historyList.innerHTML = '';
        if (currentUser.leaveRecord.length === 0) {
            historyList.innerHTML = '<li class="text-muted">No recent leave applications.</li>';
        } else {
            currentUser.leaveRecord.slice().reverse().forEach(record => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div>
                        <strong>${record.type.charAt(0).toUpperCase() + record.type.slice(1)} Leave</strong>
                        <div class="text-muted" style="font-size: 0.8rem;">Date: ${record.date} • Days: ${record.days}</div>
                    </div>
                    <span class="badge ${record.status}">${record.status.replace('-', ' ')}</span>
                `;
                historyList.appendChild(li);
            });
        }
    }

    function setProgress(circleId, value, max) {
        const circle = document.getElementById(circleId);
        if(!circle) return;
        const radius = circle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;
        
        // Avoid division by zero, max should be > 0
        const displayMax = max > 0 ? max : 1;
        const percent = (value / displayMax) * 100;
        const offset = circumference - (percent / 100) * circumference;
        
        circle.style.strokeDashoffset = offset;
    }

    function updatePerformanceUI() {
        const perf = currentUser.performance;
        document.getElementById('rating-score').textContent = perf.rating;
        document.getElementById('completed-projects').textContent = perf.completedProjects;
        
        const starsContainer = document.getElementById('rating-stars');
        starsContainer.innerHTML = '';
        const fullStars = Math.floor(perf.rating);
        const hasHalf = perf.rating % 1 !== 0;
        
        for(let i=0; i<5; i++) {
            if (i < fullStars) {
                starsContainer.innerHTML += '<i class="fa-solid fa-star"></i>';
            } else if (i === fullStars && hasHalf) {
                starsContainer.innerHTML += '<i class="fa-solid fa-star-half-stroke"></i>';
            } else {
                starsContainer.innerHTML += '<i class="fa-regular fa-star"></i>';
            }
        }

        document.getElementById('project-name').textContent = perf.currentProject.name;
        document.getElementById('project-deadline').textContent = perf.currentProject.deadline;
        document.getElementById('project-progress-text').textContent = `${perf.currentProject.progress}%`;
        document.getElementById('project-progress-bar').style.width = `${perf.currentProject.progress}%`;
    }

    function setupEventListeners() {
        // Employee switch
        employeeSelect.addEventListener('change', (e) => {
            loadEmployee(e.target.value);
        });

        // Navigation
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                navItems.forEach(n => n.classList.remove('active'));
                item.classList.add('active');

                const targetId = item.getAttribute('data-target');
                sections.forEach(s => s.classList.remove('active'));
                document.getElementById(targetId).classList.add('active');
                pageTitle.textContent = item.textContent.trim();
            });
        });

        // Password Toggle
        togglePasswordBtn.addEventListener('click', () => {
            if (wifiPasswordSpan.classList.contains('blurred')) {
                wifiPasswordSpan.classList.remove('blurred');
                wifiPasswordSpan.classList.add('unblurred');
                togglePasswordBtn.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
            } else {
                wifiPasswordSpan.classList.add('blurred');
                wifiPasswordSpan.classList.remove('unblurred');
                togglePasswordBtn.innerHTML = '<i class="fa-solid fa-eye"></i>';
            }
        });

        // Leave Logic & UI switching
        leaveTypeSelect.addEventListener('change', (e) => {
            const type = e.target.value;
            pdfVerified = false;
            submitLeaveBtn.disabled = false;
            
            // Reset fields
            aiVerificationBox.classList.add('hidden');
            aiLoader.classList.add('hidden');
            aiResult.classList.add('hidden');
            fileNameDisplay.textContent = 'Choose a PDF file...';
            medicalPdfInput.value = '';

            if (type === 'paid') {
                doctorDescGroup.style.display = 'block';
                doctorDescInput.setAttribute('required', 'true');
                pdfUploadGroup.style.display = 'none';
                medicalPdfInput.removeAttribute('required');
            } else if (type === 'maternity') {
                doctorDescGroup.style.display = 'none';
                doctorDescInput.removeAttribute('required');
                pdfUploadGroup.style.display = 'block';
                medicalPdfInput.setAttribute('required', 'true');
                submitLeaveBtn.disabled = true; // Wait for PDF verification
            } else {
                doctorDescGroup.style.display = 'none';
                doctorDescInput.removeAttribute('required');
                pdfUploadGroup.style.display = 'none';
                medicalPdfInput.removeAttribute('required');
            }
        });

        // Calculate End Date
        function calculateEndDate() {
            const days = parseInt(leaveDaysInput.value);
            const startDateStr = leaveStartDateInput.value;
            
            if (days && startDateStr && days > 0) {
                const startDate = new Date(startDateStr);
                startDate.setDate(startDate.getDate() + (days - 1));
                const options = { day: 'numeric', month: 'short', year: 'numeric' };
                leaveEndDateInput.value = startDate.toLocaleDateString('en-GB', options);
            } else {
                leaveEndDateInput.value = '';
            }
        }

        leaveDaysInput.addEventListener('input', calculateEndDate);
        leaveStartDateInput.addEventListener('change', calculateEndDate);

        // AI Verification Simulation for File Upload
        medicalPdfInput.addEventListener('change', (e) => {
            if(e.target.files.length > 0) {
                fileNameDisplay.textContent = e.target.files[0].name;
                
                // Start AI verification
                submitLeaveBtn.disabled = true;
                aiVerificationBox.classList.remove('hidden');
                aiLoader.classList.remove('hidden');
                aiResult.classList.add('hidden');
                
                setTimeout(() => {
                    aiLoader.classList.add('hidden');
                    aiResult.classList.remove('hidden');
                    
                    // Simulate random pass/fail for demo (90% pass rate)
                    const isAuthentic = Math.random() > 0.1;
                    
                    if (isAuthentic) {
                        aiResult.innerHTML = '<i class="fa-solid fa-circle-check"></i> Verification Successful: Authentic medical document.';
                        aiResult.className = 'ai-result success';
                        pdfVerified = true;
                        submitLeaveBtn.disabled = false;
                    } else {
                        aiResult.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Verification Failed: Invalid or blurry seals detected.';
                        aiResult.className = 'ai-result error';
                        pdfVerified = false;
                        submitLeaveBtn.disabled = true;
                    }
                }, 2500); // 2.5 second simulated processing time
            }
        });

        // Submit Leave Form
        leaveForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const type = leaveTypeSelect.value;
            const days = parseInt(document.getElementById('leave-days').value);
            
            if (type === 'maternity' && !pdfVerified) {
                showToast('Please upload a verified medical PDF.', 'error');
                return;
            }

            // Check Balance
            if (currentUser.leaveBalance[type] < days) {
                // Insufficient Balance - Show HR Modal
                hrReqType.value = type;
                hrReqDays.value = days;
                hrModal.classList.remove('hidden');
                return;
            }

            // Deduct and Save normally
            currentUser.leaveBalance[type] -= days;
            
            const startDateFormatted = leaveStartDateInput.value;
            const endDateFormatted = leaveEndDateInput.value;
            const dateDisplay = startDateFormatted ? `${startDateFormatted} to ${endDateFormatted}` : new Date().toISOString().split('T')[0];

            currentUser.leaveRecord.push({
                type: type,
                date: dateDisplay,
                days: days,
                status: 'approved'
            });

            saveState();
            updateLeaveUI();
            leaveForm.reset();
            doctorDescGroup.style.display = 'none';
            pdfUploadGroup.style.display = 'none';
            aiVerificationBox.classList.add('hidden');
            showToast('Leave applied successfully!');
        });

        // HR Request Modal Handlers
        closeModalBtn.addEventListener('click', () => {
            hrModal.classList.add('hidden');
            hrRequestForm.reset();
        });

        hrRequestForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const type = hrReqType.value;
            const days = parseInt(hrReqDays.value);
            const reason = document.getElementById('hr-req-reason').value;
            
            const startDateFormatted = leaveStartDateInput.value;
            const endDateFormatted = leaveEndDateInput.value;
            const dateDisplay = startDateFormatted ? `${startDateFormatted} to ${endDateFormatted}` : new Date().toISOString().split('T')[0];
            
            // Push an "HR Review" record without deducting balance yet
            currentUser.leaveRecord.push({
                type: type,
                date: dateDisplay,
                days: days,
                status: 'hr-review'
            });

            saveState();
            updateLeaveUI();
            
            hrModal.classList.add('hidden');
            hrRequestForm.reset();
            leaveForm.reset();
            doctorDescGroup.style.display = 'none';
            pdfUploadGroup.style.display = 'none';
            
            showToast('Extension request sent to HR successfully.');
        });

        // IT Forms
        laptopForm.addEventListener('submit', (e) => {
            e.preventDefault();
            showToast('Laptop request submitted successfully to IT dept.');
            laptopForm.reset();
        });

        idCardForm.addEventListener('submit', (e) => {
            e.preventDefault();
            showToast('ID Card application submitted successfully.');
        });
    }

    function showToast(message, type = 'success') {
        toast.textContent = message;
        toast.className = `toast show ${type === 'error' ? 'error' : ''}`;
        
        const icon = type === 'success' ? '<i class="fa-solid fa-check-circle"></i> ' : '<i class="fa-solid fa-circle-exclamation"></i> ';
        toast.innerHTML = icon + message;

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    // Start App
    init();
});
