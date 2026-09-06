document.addEventListener('DOMContentLoaded', () => {
    const studentForm = document.getElementById('student-form');
    const studentNameInput = document.getElementById('student-name');
    const studentRegdInput = document.getElementById('student-regd');
    const studentList = document.getElementById('student-list');
    
    const totalStudentsEl = document.getElementById('total-students');
    const presentStudentsEl = document.getElementById('present-students');
    const absentStudentsEl = document.getElementById('absent-students');

    let students = [];
    let nextId = 1;

    // Load from local storage if available
    const savedStudents = localStorage.getItem('attendanceStudents');
    if (savedStudents) {
        students = JSON.parse(savedStudents);
        if (students.length > 0) {
            nextId = Math.max(...students.map(s => s.id)) + 1;
        }
        renderStudents();
    }

    studentForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = studentNameInput.value.trim();
        const regd = studentRegdInput.value.trim();
        
        if (name && regd) {
            addStudent(name, regd);
            studentNameInput.value = '';
            studentRegdInput.value = '';
            studentNameInput.focus();
        }
    });

    function addStudent(name, regd) {
        const student = {
            id: nextId++,
            regd: regd,
            name: name,
            status: 'Pending' // Pending, Present, Absent
        };
        students.push(student);
        saveAndRender();
    }

    function updateStatus(id, status) {
        const studentIndex = students.findIndex(s => s.id === id);
        if (studentIndex !== -1) {
            students[studentIndex].status = status;
            saveAndRender();
        }
    }

    function deleteStudent(id) {
        students = students.filter(s => s.id !== id);
        // Re-assign IDs sequentially
        students.forEach((student, index) => {
            student.id = index + 1;
        });
        nextId = students.length + 1;
        saveAndRender();
    }

    function saveAndRender() {
        localStorage.setItem('attendanceStudents', JSON.stringify(students));
        renderStudents();
    }

    function renderStudents() {
        studentList.innerHTML = '';
        
        let presentCount = 0;
        let absentCount = 0;

        students.forEach(student => {
            const tr = document.createElement('tr');
            
            // Determine status badge class
            let statusClass = 'status-pending';
            if (student.status === 'Present') {
                statusClass = 'status-present';
                presentCount++;
            } else if (student.status === 'Absent') {
                statusClass = 'status-absent';
                absentCount++;
            }

            tr.innerHTML = `
                <td>#${student.id}</td>
                <td>${student.regd || 'N/A'}</td>
                <td><strong>${student.name}</strong></td>
                <td><span class="status-badge ${statusClass}">${student.status}</span></td>
                <td class="action-btns">
                    <button class="btn-present" onclick="updateStudentStatus(${student.id}, 'Present')">Present</button>
                    <button class="btn-absent" onclick="updateStudentStatus(${student.id}, 'Absent')">Absent</button>
                    <button class="btn-delete" onclick="removeStudent(${student.id})">Delete</button>
                </td>
            `;
            studentList.appendChild(tr);
        });

        // Update Summary
        totalStudentsEl.textContent = students.length;
        presentStudentsEl.textContent = presentCount;
        absentStudentsEl.textContent = absentCount;
    }

    // Expose functions to global scope for inline event handlers
    window.updateStudentStatus = updateStatus;
    window.removeStudent = deleteStudent;
});
