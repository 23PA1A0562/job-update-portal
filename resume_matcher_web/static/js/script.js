document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('matcher-form');
    const fileInput = document.getElementById('resume_file');
    const fileLabel = document.querySelector('.file-label');
    const fileNameDisplay = document.getElementById('file-name');
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = analyzeBtn.querySelector('span');
    const loader = document.getElementById('btn-loader');
    
    const resultsSection = document.getElementById('results-section');
    const errorToast = document.getElementById('error-message');
    
    // File upload UI update
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const fileName = e.target.files[0].name;
            fileNameDisplay.textContent = fileName;
            fileLabel.classList.add('has-file');
            
            // Clear textarea if file is uploaded
            document.getElementById('resume_text').value = '';
        } else {
            fileNameDisplay.textContent = 'Choose a file or drag it here';
            fileLabel.classList.remove('has-file');
        }
    });
    
    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Basic validation
        const resumeFile = fileInput.files[0];
        const resumeText = document.getElementById('resume_text').value.trim();
        const jobText = document.getElementById('job_description').value.trim();
        
        if (!resumeFile && !resumeText) {
            showError('Please upload a resume file or paste your resume text.');
            return;
        }
        
        if (!jobText) {
            showError('Please paste the job description.');
            return;
        }
        
        // UI Loading state
        setLoading(true);
        resultsSection.classList.add('hidden');
        
        try {
            const formData = new FormData(form);
            
            const response = await fetch('/api/match', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'An error occurred during analysis.');
            }
            
            displayResults(data);
            
        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(false);
        }
    });
    
    function displayResults(data) {
        // Show results section
        resultsSection.classList.remove('hidden');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Update Score Circular Progress
        const scoreCircle = document.getElementById('score-path');
        const scoreText = document.getElementById('score-text');
        
        // Math for circle animation: 2 * pi * r (where r = 45) = 282.74
        const circumference = 283;
        const offset = circumference - (data.score / 100) * circumference;
        
        // Trigger animation
        setTimeout(() => {
            scoreCircle.style.strokeDashoffset = offset;
            
            // Color based on score
            if (data.score >= 70) {
                scoreCircle.style.stroke = 'var(--success)';
                scoreText.style.color = 'var(--success)';
            } else if (data.score >= 45) {
                scoreCircle.style.stroke = 'var(--warning)';
                scoreText.style.color = 'var(--warning)';
            } else {
                scoreCircle.style.stroke = 'var(--error)';
                scoreText.style.color = 'var(--error)';
            }
        }, 100);
        
        // Animate counter
        animateValue(scoreText, 0, data.score, 1500);
        
        // Update Verdict Badge
        const verdictBadge = document.getElementById('verdict-badge');
        verdictBadge.textContent = data.verdict;
        verdictBadge.className = 'badge'; // reset
        if (data.score >= 70) verdictBadge.classList.add('success');
        else if (data.score >= 45) verdictBadge.classList.add('warning');
        else verdictBadge.classList.add('error');
        
        // Update Keywords Lists
        const missingContainer = document.getElementById('missing-tags');
        const matchedContainer = document.getElementById('matched-tags');
        
        document.getElementById('missing-count').textContent = data.missing.length;
        document.getElementById('matched-count').textContent = data.matched.length;
        
        // Clear old tags
        missingContainer.innerHTML = '';
        matchedContainer.innerHTML = '';
        
        // Inject Missing Keywords
        if (data.missing.length === 0) {
            missingContainer.innerHTML = '<span class="text-muted">None found! Great job.</span>';
        } else {
            data.missing.forEach((word, index) => {
                // Staggered animation delay
                const delay = index * 0.05;
                const tag = document.createElement('div');
                tag.className = 'tag missing';
                tag.textContent = word;
                tag.style.animation = `slideUp 0.3s ease ${delay}s both`;
                missingContainer.appendChild(tag);
            });
        }
        
        // Inject Matched Keywords
        if (data.matched.length === 0) {
            matchedContainer.innerHTML = '<span class="text-muted">No keywords matched.</span>';
        } else {
            data.matched.forEach((word, index) => {
                const delay = index * 0.05;
                const tag = document.createElement('div');
                tag.className = 'tag matched';
                tag.textContent = word;
                tag.style.animation = `slideUp 0.3s ease ${delay}s both`;
                matchedContainer.appendChild(tag);
            });
        }
    }
    
    function setLoading(isLoading) {
        if (isLoading) {
            analyzeBtn.disabled = true;
            btnText.style.display = 'none';
            loader.style.display = 'block';
        } else {
            analyzeBtn.disabled = false;
            btnText.style.display = 'block';
            loader.style.display = 'none';
        }
    }
    
    function showError(message) {
        errorToast.textContent = message;
        errorToast.classList.remove('hidden');
        
        setTimeout(() => {
            errorToast.classList.add('hidden');
        }, 4000);
    }
    
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start) + '%';
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                // Make sure final value can have decimals if needed, but floor is cleaner for UI
                obj.innerHTML = end + '%';
            }
        };
        window.requestAnimationFrame(step);
    }
});
