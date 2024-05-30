function addExperience() {
    var experienceFields = document.getElementById("experience_fields");
    var newExperience = document.createElement("div");
    newExperience.innerHTML = `
        <div class="experience">
            <input type="text" name="experience_job_title" placeholder="Job Title">
            <input type="text" name="experience_duration" placeholder="Duration">
            <input type="text" name="experience_work_summary" placeholder="Work Summary">
        </div>
    `;
    experienceFields.appendChild(newExperience);
}

function removeLastExperience() {
    var experienceFields = document.getElementById("experience_fields");
    var lastExperience = experienceFields.lastElementChild;
    if (lastExperience) {
        experienceFields.removeChild(lastExperience);
    }
}


function addEducation() {
    var educationFields = document.getElementById("education_fields");
    var newEducation = document.createElement("div");
    newEducation.innerHTML = `
        <div class="education">
             <input type="text" name="education_institution" placeholder="Institution">
             <input type="text" name="education_degree" placeholder="Degree">
             <input type="text" name="education_field" placeholder="Field of Study">
             <input type="text" name="education_duration" placeholder="Duration">
        </div>
    `;
   educationFields.appendChild(newEducation);
}

function removeLastEducation() {
    var educationFields = document.getElementById("education_fields");
    var lasteducation = educationFields.lastElementChild;
    if (lasteducation) {
        educationFields.removeChild(lasteducation);
    }
}



function addCertification() {
    var certificationFields = document.getElementById("certification_fields");
    var newCertification = document.createElement("div");
    newCertification.innerHTML = `
        <div class="certification">
            <input type="text" name="certification_name" placeholder="Certification Name">
            <input type="text" name="certification_source" placeholder="From Where">
            <input type="text" name="certification_field" placeholder="Field of Study">
        </div>
    `;
    certificationFields.appendChild(newCertification);
}

function removeLastCertification() {
    var certificationFields = document.getElementById("certification_fields");
    var lastcertification = certificationFields.lastElementChild;
    if (lastcertification) {
        certificationFields.removeChild(lastcertification);
    }
}

var count = 4
function addSkill() {
    var skillsContainer = document.getElementById("skills_container");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "skills[]";
    input.placeholder = "Skill"+ " "+ count++;
    skillsContainer.appendChild(document.createElement("br"));
    skillsContainer.appendChild(input);
}